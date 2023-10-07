import pygame
import math


class Entity():
    def __init__(self, life_points, x, y) -> None:
        self.life_points = life_points
        self.x = x
        self.y = y


    def calc_distance_between (self,A,B):
        distancia = math.sqrt(
            pow((A.x - B.x), 2)+pow((A.y - B.y), 2))
        return distancia
    
    def MasCercano(self,A,B):
        Target=Entity(life_points=1,x=1000000,y=1000000)
        for b in B:
            if self.calc_distance_between(A,b)<self.calc_distance_between(A,Target):
                Target=b

        return Target

    def Getdamage(self,A,damage):
        A.life_points = A.life_points-damage