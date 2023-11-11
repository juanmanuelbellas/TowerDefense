import pygame
import uuid

from connection import Client
from events.input import ClickEvent
from entities.enemies import EnemyFactory

class EntityToSend:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.uuid = uuid.uuid4

class Game:
    def __init__(self):
        self.running = True
        self.screen_width = 800
        self.screen_height = 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.connection = Client("167.56.242.96", 27960)
        self.events = []
        self.entities = []
        self.entities_to_send = []


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.connection.close()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                self.entities_to_send.append(EntityToSend(x,y,100,100))

    def drawRect(self, entity):
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        color = "red"
        pygame.draw.rect(self.screen, color, rect, border_radius=15)

    def render(self):
        self.screen.fill((204, 193, 163))
        for entity in self.entities:
            self.drawRect(entity)


        pygame.display.flip()


    def send(self):
        if len(self.entities_to_send) >= 1:
            for entity in self.entities_to_send:
                self.connection.send(entity)
                self.entities_to_send.remove(entity)
   

    def run(self):
        while self.running:
            self.entities = self.connection.entities
            self.handle_input()
            self.send()
            self.render()
            

if __name__ == "__main__":
   game = Game()
   game.run()
