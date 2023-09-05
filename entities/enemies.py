import pygame
import math
from entities.entity import Entity


class Enemy(Entity):
    def __init__(self, color, life_points, game, x=1000, y=300):
        super().__init__(life_points=life_points, x=x, y=y)
        self.game = game
        self.color = color
        self.width = 100
        self.height = 100
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5/60
        self.dx = (self.x - game.player.x) / self.speed
        self.dy = (self.y - game.player.y) / self.speed

    def calc_direction_speed(self):
        distancia = math.sqrt(
            pow((self.x - self.game.player.x), 2)+pow((self.y - self.game.player.y), 2))
        tiempo = distancia / self.speed
        self.vx_enemy = (self.game.player.x - self.x) / tiempo
        self.vy_enemy = (self.game.player.y - self.y) / tiempo

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color,
                         self.rect, border_radius=15)

    def update(self):
        self.calc_direction_speed()

        self.x += self.vx_enemy
        self.y += self.vy_enemy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.x <= self.game.player.x + 100:
            self.game.entities.remove(self)
