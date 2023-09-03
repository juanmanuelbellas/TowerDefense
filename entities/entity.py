import pygame


class Entity():
    def __init__(self, life_points, x, y) -> None:
        self.life_points = life_points
        self.x = x
        self.y = y
