import pygame

class ClickEvent:
    def __init__(self, mouse_button, x, y):
        self.mouse_button = mouse_button
        self.x = x
        self.y = y
