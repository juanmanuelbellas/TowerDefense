import pygame
from entities.entity import Entity
from entities.bullet import Proyectiles

class MainTower(Entity):
    def __init__(self, color, x, y, life_points):
        super().__init__(life_points=life_points, x=x, y=y)
        self.color = color
        self.id='MainTower'
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 0
        self.game = None  # Initialize the game attribute as None

    def set_game(self, game):
        self.game = game

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)

    def update(self):
        # Update logic for the main tower here
        pass

class SecondaryTower(Entity):
    def __init__(self, color, x, y, life_points,game):
        super().__init__(life_points=life_points, x=x, y=y)
        self.color = color
        self.id="secondary_tower"
        self.width = 35
        self.height = 35
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 0
        self.attackradius = 400
        self.cantupdates=0
        self.game=game
        self.Target=[]
        self.HasTarget=False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)

    def update(self):
        self.cantupdates+=1
        self.shoot()
        # Update logic for secondary tower here
    
    def shoot(self):
        if  self.HasTarget:
            if(self.Target.life_points<=0):
                self.HasTarget=False
            
        if ((self.cantupdates%25)==0)&(self.game.entities!=[]):
                if (not self.HasTarget):
                    self.Target=self.MasCercano(self,self.game.entities)
                    self.HasTarget=True
                bullet=Proyectiles("green",1,self.game,self.Target,self.x+self.width/2, self.y+self.height/2)
                self.game.bullets.append(bullet)

