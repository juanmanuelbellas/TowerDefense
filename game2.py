import pygame
import uuid
import argparse

from connection import Client
from events.input import ClickEvent
from entities.enemies import EnemyFactory
from entities.towers import Tower


class Game:
    def __init__(self):
        self.running = True
        self.screen_width = 800
        self.screen_height = 600
        self.clock = pygame.time.Clock()

        self.parser = argparse.ArgumentParser(description="Retrieves arguments from command line.")
        self.parser.add_argument("--ip", type=str, required=True, help="The IP address")
        self.parser.add_argument("--port", type=int, required=True, help="The port number")
        self.args = self.parser.parse_args()
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.connection = Client(self.args.ip, self.args.port, clock=self.clock)
        self.entities = []
        self.entities_to_send = []



    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.connection.close()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                width=100
                height=100
                x = x - width / 2
                y = y - height / 2
                self.entities_to_send.append(Tower(width=width,height=height,x=x,y=y,hit_points=100, color="blue"))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                x, y = pygame.mouse.get_pos()
                width=50
                height=50
                x = x - width / 2
                y = y - height / 2
                self.entities_to_send.append(EnemyFactory.create_enemy('troll', x=x, y=y))


    def drawRect(self, entity):
        rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
        color = entity.color 
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
            self.clock.tick(60)
            

if __name__ == "__main__":
   game = Game()
   game.run()
