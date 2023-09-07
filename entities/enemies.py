import pygame
import math
from entities.entity import Entity
from entities.bullet import Proyectiles


class Enemy(Entity):
    def __init__(self, color, life_points, game, x=1000, y=300):
        super().__init__(life_points=life_points, x=x, y=y)
        self.game = game
        self.id="entities"
        self.color = color
        self.width = 100
        self.height = 100
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x-self.width/2, y-self.height/2, self.width, self.height)
        self.cantupdates=0
        self.speed = 1

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
        self.cantupdates+=1
        self.x += self.vx_enemy
        self.y += self.vy_enemy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shoot()
        if self.life_points<=0:
            self.game.entities.remove(self)
        if (self.calc_distance_between(self,self.game.player))<=100:
            self.game.entities.remove(self)
        NearBullet=self.MasCercano(self,self.game.bullets)

    
    def shoot(self): 
        if (self.cantupdates%50)==0:
                bullet=Proyectiles("black",1,self.game,self.game.player,self.x+self.width/2, self.y+self.height/2)
                self.game.bullets.append(bullet)
    


