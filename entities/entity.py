import pygame
import math
import uuid


class Entity():
    def __init__(self, hit_points, x, y, w=100, h=100):
        self.uuid = uuid.uuid4()
        self.hit_points = hit_points
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.is_new = True
        self.is_mod = False


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
