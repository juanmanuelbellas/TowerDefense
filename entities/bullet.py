import pygame
import math
from entities.entity import Entity


class Proyectiles(Entity):
    def __init__(self, color, damage, game,Target, xfrom=1000, yfrom=300):
        self.game = game
        self.id='bullet'
        self.damage=damage
        self.Target=Target
        self.color = color
        self.width = 5
        self.height = 5
        self.x = xfrom
        self.y = yfrom
        self.rect = pygame.Rect(xfrom, yfrom, self.width, self.height)
        self.speed = 2
        self.xtarget=Target.x
        self.ytarget=Target.y
        self.life_points=1
        self.distancia=math.sqrt(pow((self.x - self.xtarget), 2)+pow((self.y - self.ytarget), 2))
        self.tiempo = self.distancia / self.speed
        self.vx = (self.xtarget - self.x) / self.tiempo
        self.vy = (self.ytarget - self.y) / self.tiempo
        self.cantupdates=0

    def calc_direction_speed(self):
        distancia = math.sqrt(
            pow((self.x - self.Target.x), 2)+pow((self.y - self.Target.y), 2))
        tiempo = distancia / self.speed
        self.vx = (self.xtarget - self.x) / tiempo
        self.vy = (self.ytarget - self.y) / tiempo

    def draw(self):
        pygame.draw.rect(self.game.screen, self.color,
                         self.rect, border_radius=20)

    def update(self):

        self.cantupdates+=1
        self.x += self.vx
        self.y += self.vy
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
 
        if self.Target.id=="secondary_tower": 
                self.collide(self.game.secondary_towers)
        elif self.Target.id=="bullet":
                self.collide(self.game.bullets)
        elif self.Target.id=="entities":
                self.collide(self.game.entities)
        elif self.Target.id=="MainTower":
            target=self.game.player
            if (pygame.Rect.colliderect(self.rect,target.rect)):
                self.Getdamage(target,self.damage)
                self.game.bullets.remove(self)
        
        if (self.cantupdates>2000):
            self.game.bullets.remove(self)


    def collide (self,Targets):

        for target in Targets:
            if (pygame.Rect.colliderect(self.rect,target.rect)):
                self.Getdamage(target,self.damage)
                self.game.bullets.remove(self)
                break