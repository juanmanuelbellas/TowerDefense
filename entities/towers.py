import pygame
from entities.entity import Entity


class MainTower(Entity):
    def __init__(self, color, x, y, life_points, game):
        super().__init__(life_points=life_points, x=x, y=y)
        self.game = game
        self.color = color
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 0

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color,
                         self.rect, border_radius=15)

    def update(self):
        pass


class Tower(Entity):
    def __init__(self,hit_points, color, x, y, width, height):
        super().__init__(hit_points=hit_points, x=x, y=y, type="tower")
        self.color = color
        self.width = width
        self.height = height
        self.hit_points = hit_points
        self.can_move = False
        self.team = 'd'

