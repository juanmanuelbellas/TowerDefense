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
        self.speed = 1


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

    

    def set_velocity(self, target):
        if self.can_move and self.speed > 0:
            self.distance_to_target = math.sqrt(
                pow((self.x - self.target.x), 2)+pow((self.y - self.target.y), 2))
            time_to_reach = self.distance_to_target / self.speed
            self.vx = (self.target.x - self.x) / time_to_reach
            self.vy = (self.target.y - self.y) / time_to_reach

    def set_target(self,target):
        if target:
            self.target = target
            self.set_velocity(self.target)
    
    def stop_movement(self):
        self.vx = 0
        self.vy = 0


    def set_no_target(self):
        self.target = None
        self.stop_movement()

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    
    def update(self):
        self.move()



class Tower(Entity):
    def __init__(self, hit_points, x, y, w=100, h=100, type="tower"):
        super.__init__(self, hit_points, x, y, w, h, type)
        self.speed = 0
