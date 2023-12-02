import pygame
import math
import uuid


class Entity():
    def __init__(self, hit_points, x, y, w=100, h=100, type="tower"):
        self.uuid = uuid.uuid4()
        self.hit_points = hit_points
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.is_new = True
        self.is_mod = False
        self.type = type
        self.target = None
        self.vx = 0
        self.vy = 0


    def calc_distance_between (self,A,B):
        distancia = math.sqrt(
            pow((A.x - B.x), 2)+pow((A.y - B.y), 2))
        return distancia
    
    def MasCercano(self,A,B):
        Target=Entity(hit_points=1,x=1000000,y=1000000)
        for b in B:
            if self.calc_distance_between(A,b)<self.calc_distance_between(A,Target):
                Target=b

        return Target

    def Getdamage(self,A,damage):
        A.hit_points = A.hit_points-damage

    
    def get_closer_entity(self):
        return Entity(hit_points=1,x=100,y=100)

    def set_speed(self, target):
        self.vx = 10
        self.vy = 10

    def seek_target(self):
        self.target = self.get_closer_entity()
        self.set_speed(self.target)


    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    
    def update(self):
        self.move()
        self.seek_target()
