# Snake Multiplayer Challenge

Bienvenue au **Snake Multiplayer Challenge** ! Ce projet vous offre un environnement de jeu Snake dans lequel vous pouvez créer et intégrer votre propre agent intelligent pour affronter d'autres agents. Ce guide vous aidera à comprendre comment installer l'environnement, comment développer votre agent, et comment le faire interagir avec le jeu.

## Table des matières

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Manuel de création d'un agent](#manuel-de-création-dun-agent)
- [Utilisation de l'environnement](#utilisation-de-lenvironnement)
- [Lancer une partie multijoueur](#lancer-une-partie-multijoueur)
- [Règles du jeu](#règles-du-jeu)
- [Contact](#contact)

---

## Prérequis

- Python 3.6 ou supérieur
- Pygame (`pip install pygame`)

## Installation

Vous pouvez installer l'environnement du jeu directement depuis le dépôt GitHub en utilisant `pip` :

```bash
pip install git+https://github.com/ZacJiker/Snake-Multiplayer-Challenge.git
```

## Manuel de création d'un agent

Un agent est une fonction qui détermine la prochaine direction du serpent en fonction de l'état actuel du jeu. Pour être compatible avec l'environnement, votre agent doit respecter les spécifications suivantes :

### Spécifications de l'agent

- Entrées :

    - `snake` : une instance de la classe `Snake` représentant votre serpent.
    - `food_position` : une `pygame.Vector2` représentant la position actuelle de la première pomme.

- Sortie :

    - Une `pygame.Vector2` indiquant la nouvelle direction du serpent. Les directions valides sont :

        - `pygame.Vector2(1, 0)` : droite
        - `pygame.Vector2(-1, 0)` : gauche
        - `pygame.Vector2(0, 1)` : bas
        - `pygame.Vector2(0, -1)` : haut

### Contraintes

- **Pas de demi-tour immédiat** : Votre agent ne doit pas retourner la direction opposée à celle actuelle du serpent pour éviter les demi-tours instantanés.

- **Temps de calcul** : Votre agent doit calculer la nouvelle direction rapidement pour ne pas ralentir le jeu.

### Étapes pour créer votre agent

1. Créer un fichier pour votre agent :

    Créez un nouveau fichier Python, par exemple mon_agent.py.

2. Définir votre agent :

    ```python
    import pygame

    def mon_agent(snake, food_position):
        # Votre logique pour déterminer la nouvelle direction
        # snake : instance de Snake
        # food_position : position de la première pomme
        # Retourne une direction valide
        return pygame.Vector2(1, 0)  # Exemple : toujours aller à droite
    ```

3. Implémenter la logique de votre agent :

    Utilisez les informations disponibles (position du serpent, position de la nourriture, etc.) pour déterminer la meilleure action à chaque tour.

### Informations utiles

- Accéder à la position de la tête du serpent :

    ```python
    head_position = snake.body[-1]
    ```

- Accéder à la direction actuelle du serpent :

    ```python
    current_direction = snake.direction
    ```

- Éviter les obstacles :

    Vous pouvez vérifier si la prochaine position est sûre en évitant les collisions avec le corps du serpent ou les limites du terrain

## Utilisation de l'environnement

Pour utiliser l'environnement, vous devez créer un script Python séparé qui importe l'environnement, votre(vos) agent(s), et lance le jeu.

### Étapes pour lancer le jeu avec votre agent

1. Créer un script de lancement :

    Créez un fichier Python, par exemple `lancer_jeu.py`.

2. Importer les modules nécessaires :

    ```python
    from snake_game.game import game_play
    from mon_agent import mon_agent
    ```

3. Initialiser et lancer le jeu :

    ```python
    if __name__ == "__main__":
        game = game_play(primary_agent=mon_agent, primary_agent_name="Mon Agent")
        game.play()
    ```

4. Exécuter votre script :

    ```bash
    python lancer_jeu.py
    ```

## Lancer une partie multijoueur

Pour lancer une partie avec deux agents (par exemple, votre agent contre un agent aléatoire) :

1. Créer ou importer le deuxième agent :

    ```python
    from agent_aleatoire import agent_aleatoire
    ```

2. Initialiser le jeu avec les deux agents :

    ```python
    if __name__ == "__main__":
        game = game_play(primary_agent=mon_agent,
                        secondary_agent=agent_aleatoire,
                        primary_agent_name="Mon Agent",
                        secondary_agent_name="Agent Aléatoire")
        game.play()
    ```

## Règles du jeu

- **Objectif** : Manger le plus de pommes possible sans entrer en collision avec soi-même ou sortir des limites.

- **Pommes** : Entre 1 et 3 pommes apparaissent aléatoirement sur le terrain.

- **Score** : Chaque pomme mangée augmente le score de l'agent de 1 point.

- **Conditions de fin** :
    - Collision avec soi-même.
    - Sortie des limites du terrain.

- **Détermination du gagnant** :
    - Le jeu se termine lorsque l'un des serpents perd.
    - Le serpent avec le score le plus élevé est déclaré gagnant.
    - En cas d'égalité, le jeu se termine par un match nul.

## Contact

Pour toute question ou assistance supplémentaire, veuillez me contacter.