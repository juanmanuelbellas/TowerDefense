import pygame
from entities.entity import Entity

class MainTower(Entity):
    def __init__(self, color, x, y, life_points):
        super().__init__(life_points=life_points, x=x, y=y)
        self.color = color
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 0
        self.game = None  # Initialize the game attribute as None

    def set_game(self, game):
        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)

    def update(self):
        # Update logic for the main tower here
        pass

class SecondaryTower(Entity):
    def __init__(self, color, x, y, life_points):
        super().__init__(life_points=life_points, x=x, y=y)
        self.color = color
        self.width = 35
        self.height = 35
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def update(self):
        # Update logic for secondary tower here
        pass
