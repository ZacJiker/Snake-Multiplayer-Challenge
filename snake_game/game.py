import pygame
from snake_game.snake import Snake
import random

# Configuration de base
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 10
BANNER_HEIGHT = 50
GAME_HEIGHT = HEIGHT - BANNER_HEIGHT

class game_play:
    def __init__(self, primary_agent, secondary_agent=None, primary_agent_name="Primary Agent", secondary_agent_name="Secondary Agent"):
        """
        Initialise le jeu avec un ou deux agents, et permet de personnaliser les noms des agents.

        Args:
            primary_agent: Le premier agent (requis).
            secondary_agent: Le deuxième agent (optionnel).
            primary_agent_name: Nom du premier agent (par défaut "Primary Agent").
            secondary_agent_name: Nom du deuxième agent (par défaut "Secondary Agent").
        """
        self.primary_agent = primary_agent
        self.secondary_agent = secondary_agent
        self.primary_agent_name = primary_agent_name
        self.secondary_agent_name = secondary_agent_name
        self.screen = None
        self.clock = None
        self.primary_snake = None
        self.secondary_snake = None
        self.food_positions = []  # Liste des positions de pommes
        self.primary_score = 0  # Score pour le premier agent
        self.secondary_score = 0  # Score pour le second agent (si applicable)
        self.winner = None  # Gagnant du match
        
        # Détecte si le jeu est solo ou multijoueur
        self.is_multiplayer = secondary_agent is not None

    def random_food_positions(self):
        """
        Génère entre 1 et 3 pommes à des positions aléatoires sur le terrain,
        sans les placer sur les serpents.
        """
        num_apples = random.randint(1, 3)  # Nombre de pommes entre 1 et 3
        food_positions = []
        while len(food_positions) < num_apples:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(BANNER_HEIGHT // BLOCK_SIZE, (GAME_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food_pos = pygame.Vector2(x, y)
            
            # Vérification que la pomme ne se génère pas sur un serpent
            if new_food_pos not in self.primary_snake.body and (not self.is_multiplayer or new_food_pos not in self.secondary_snake.body):
                food_positions.append(new_food_pos)
        return food_positions

    def setup(self):
        """
        Configure le jeu et initialise Pygame.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Multiplayer Challenge")
        self.clock = pygame.time.Clock()

        # Initialisation des serpents
        self.primary_snake = Snake(GREEN, WIDTH, GAME_HEIGHT, BLOCK_SIZE)

        if self.is_multiplayer:
            self.secondary_snake = Snake(BLUE, WIDTH, GAME_HEIGHT, BLOCK_SIZE)

        # Générer les premières pommes
        self.food_positions = self.random_food_positions()

    def draw_nfl_scores(self):
        """
        Affiche les scores des agents sur l'écran dans un style NFL (bannière en haut).
        """
        font = pygame.font.Font(None, 48)
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, BANNER_HEIGHT))  # Bannière noire pour les scores

        primary_score_text = font.render(f"{self.primary_agent_name}: {self.primary_score}", True, WHITE)
        self.screen.blit(primary_score_text, (20, 10))

        if self.is_multiplayer:
            secondary_score_text = font.render(f"{self.secondary_agent_name}: {self.secondary_score}", True, WHITE)
            self.screen.blit(secondary_score_text, (WIDTH - 300, 10))  # Affichage du score du second agent à droite

    def show_winner(self):
        """
        Affiche le gagnant et attend l'appui de la touche Q pour quitter.
        """
        if self.winner is None:
            if self.primary_score > self.secondary_score:
                self.winner = self.primary_agent_name
            elif self.primary_score < self.secondary_score:
                self.winner = self.secondary_agent_name
            else:
                self.winner = "Match nul !"
        
        font = pygame.font.Font(None, 72)
        winner_text = font.render(f"Gagnant: {self.winner}", True, WHITE)
        self.screen.fill(BLACK)
        self.screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 50))
        
        pygame.display.update()

        # Attendre que l'utilisateur appuie sur 'Q' pour quitter
        waiting_for_exit = True
        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_exit = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    waiting_for_exit = False

        pygame.quit()

    def play(self):
        """
        Méthode principale pour jouer au jeu. Les agents doivent implémenter leur logique ici.
        """
        self.setup()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Informations à transmettre aux agents
            primary_info = {
                "snake": self.primary_snake.body,
                "opponent_snake": self.secondary_snake.body if self.is_multiplayer else None,
                "food_positions": self.food_positions
            }
            
            # Agent du serpent principal
            new_direction_primary = self.primary_agent(primary_info)
            self.primary_snake.change_direction(new_direction_primary)

            if self.is_multiplayer:
                secondary_info = {
                    "snake": self.secondary_snake.body,
                    "opponent_snake": self.primary_snake.body,
                    "food_positions": self.food_positions
                }
                # Agent du second serpent
                new_direction_secondary = self.secondary_agent(secondary_info)
                self.secondary_snake.change_direction(new_direction_secondary)

            # Déplacement des serpents
            self.primary_snake.move(BLOCK_SIZE)
            if self.is_multiplayer:
                self.secondary_snake.move(BLOCK_SIZE)

            # Vérification des collisions et des pommes
            if not self.check_collisions_and_food():  # Si une collision ou sortie de zone est détectée, arrêter le jeu
                running = False

            # Mise à jour de l'affichage
            self.screen.fill(BLACK)
            self.primary_snake.draw(self.screen, BLOCK_SIZE)

            # Dessiner les pommes
            for food_pos in self.food_positions:
                pygame.draw.rect(self.screen, RED, (*food_pos, BLOCK_SIZE, BLOCK_SIZE))

            if self.is_multiplayer:
                self.secondary_snake.draw(self.screen, BLOCK_SIZE)

            # Affichage des scores dans la bannière
            self.draw_nfl_scores()

            pygame.display.update()
            self.clock.tick(FPS)

        # Après la fin du jeu, afficher le gagnant
        self.show_winner()

    def check_collisions_and_food(self):
        """
        Vérifie les collisions avec la nourriture, les collisions entre les serpents, 
        et la sortie du serpent hors de la zone de jeu.
        """
        # Gestion des collisions avec les pommes pour le premier agent
        for food_pos in self.food_positions[:]:  # Utilisation de copie pour éviter la modification pendant l'itération
            if self.primary_snake.body[-1] == food_pos:
                self.primary_snake.grow_snake()
                self.food_positions.remove(food_pos)
                self.primary_score += 1

        # Gestion des collisions avec les pommes pour le second agent (si multijoueur)
        if self.is_multiplayer:
            for food_pos in self.food_positions[:]:
                if self.secondary_snake.body[-1] == food_pos:
                    self.secondary_snake.grow_snake()
                    self.food_positions.remove(food_pos)
                    self.secondary_score += 1

        # Générer de nouvelles pommes si toutes ont été mangées
        if not self.food_positions:
            self.food_positions = self.random_food_positions()

        # Vérification des collisions avec soi-même et entre les serpents
        if self.primary_snake.collision_with_self() or self.primary_snake.out_of_bounds(WIDTH, GAME_HEIGHT):
            self.winner = self.secondary_agent_name if self.is_multiplayer else self.primary_agent_name
            return False  # Arrêter immédiatement le jeu

        if self.is_multiplayer:
            if self.secondary_snake.collision_with_self() or self.secondary_snake.out_of_bounds(WIDTH, GAME_HEIGHT):
                self.winner = self.primary_agent_name
                return False  # Arrêter immédiatement le jeu

            # Vérification des collisions entre les serpents
            if self.primary_snake.body[-1] in self.secondary_snake.body:
                self.winner = self.secondary_agent_name
                return False  # Arrêter immédiatement le jeu

            if self.secondary_snake.body[-1] in self.primary_snake.body:
                self.winner = self.primary_agent_name
                return False  # Arrêter immédiatement le jeu

        return True  # Le jeu continue

