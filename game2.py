import pygame

from connection import Client
from events.input import ClickEvent


class Game:
    def __init__(self):
        self.running = True
        self.screen_width = 800
        self.screen_height = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.connection = Client("tituela.servebeer.com", 7173)
        self.events = []
        self.entities = []


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.connection.close()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                self.events.append(ClickEvent(event.button, x,y))


    def render(self):
        self.screen.fill((204, 193, 163))
        pygame.display.flip()


    def send(self):
        if len(self.entities) >= 1:
            for entity in self.entities:
                self.connection.send(entity)
   

    def run(self):
        while self.running:
            self.handle_input()
            self.send()
            self.render()
            

if __name__ == "__main__":
   game = Game()
   game.run()
