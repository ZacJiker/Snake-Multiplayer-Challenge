import pygame
import random

class Snake:
    def __init__(self, color, screen_width, screen_height, block_size):
        self.color = color
        self.body = [self.random_start_position(screen_width, screen_height, block_size)]  # Position aléatoire de départ
        self.direction = self.random_start_direction()  # Direction aléatoire de départ
        self.grow = False

    def random_start_position(self, screen_width, screen_height, block_size):
        """
        Génère une position aléatoire pour le serpent en fonction de la taille de l'écran.
        """
        x = random.randint(0, (screen_width - block_size) // block_size) * block_size
        y = random.randint(0, (screen_height - block_size) // block_size) * block_size
        return pygame.Vector2(x, y)

    def random_start_direction(self):
        """
        Génère une direction aléatoire parmi les quatre directions possibles (haut, bas, gauche, droite).
        """
        directions = [pygame.Vector2(1, 0),  # Droite
                      pygame.Vector2(-1, 0),  # Gauche
                      pygame.Vector2(0, 1),  # Bas
                      pygame.Vector2(0, -1)]  # Haut
        return random.choice(directions)

    def move(self, block_size):
        if not self.body:  # Si le corps est vide, il y a une erreur dans l'initialisation
            raise ValueError("Le corps du serpent est vide !")

        if not self.grow and len(self.body) > 1:
            self.body.pop(0)  # Retire la queue uniquement si le serpent a plus d'une partie dans son corps
        elif self.grow:
            self.grow = False

        # Ajout de la nouvelle tête
        new_head = self.body[-1] + self.direction * block_size
        self.body.append(new_head)

    def change_direction(self, new_direction):
        if new_direction != -self.direction:  # Empêche le demi-tour
            self.direction = new_direction

    def draw(self, surface, block_size):
        for part in self.body:
            pygame.draw.rect(surface, self.color, (*part, block_size, block_size))

    def grow_snake(self):
        self.grow = True

    def collision_with_self(self):
        return any(part == self.body[-1] for part in self.body[:-1])

    def out_of_bounds(self, width, height):
        head = self.body[-1]
        return head.x < 0 or head.x >= width or head.y < 0 or head.y >= height