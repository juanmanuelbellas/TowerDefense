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
        if len(self.events) >= 1:
            for event in self.events:
                self.connection.send(event)
                self.events.remove(event)
   

    def run(self):
        while self.running:
            self.handle_input()
            self.send()
            self.render()
            

if __name__ == "__main__":
   game = Game()
   game.run()
