import pygame
import uuid

from connection import Client, EntityToSend
from events.input import ClickEvent
from entities.enemies import EnemyFactory


class Game:
    def __init__(self):
        self.running = True
        self.screen_width = 800
        self.screen_height = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.connection = Client("127.0.0.1", 1234)
        self.entities = []
        self.entities_to_send = []


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.connection.close()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                self.entities_to_send.append(EntityToSend(x,y,100,100, color="green"))

    def drawRect(self, entity):
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        color = "red"
        pygame.draw.rect(self.screen, color, rect, border_radius=15)

    def render(self):
        self.screen.fill((204, 193, 163))
        for entity in self.entities:
            self.drawRect(entity)


        pygame.display.flip()


    def send_entities(self):
        if len(self.entities_to_send) >= 1:
            for entity in self.entities_to_send:
                self.connection.send_entities(entity)
                self.entities_to_send.remove(entity)
   
    def update_from_connection(self):
        self.entities = self.connection.entities

    def run(self):
        while self.running:
            self.update_from_connection()
            self.handle_input()
            self.send_entities()
            self.render()
            

if __name__ == "__main__":
   game = Game()
   game.run()
