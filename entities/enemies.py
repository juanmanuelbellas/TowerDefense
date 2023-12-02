import pygame
from entities.entity import Entity


class Enemy(Entity):
    """
    A class representing enemies in the game. It inherits from the Entity
    class the position(x, y), UUID and the hit_points parameters.
    """
    def __init__(self, color, hit_points: int, speed: float, 
                range: int, ammo: str, damage: int, attack_speed: float, weakness: str,
                cost: int, x=1000, y=300, level=1):
        """
        Initialize an enemy object.

        Args:
            game (Game): The game instance.
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
            color: The color of the enemy.
            hit_points (int): The hit points of the enemy.
            speed (float): The movement speed of the enemy.
            range (int): The attack range of the enemy.
            ammo (str): The type of ammunition the enemy uses.
            damage (int): The damage dealt by the enemy.
            attack_speed (float): The attack speed of the enemy.
            weakness (str): The enemy's weakness.
            cost (int): The cost of the enemy.
            level (int): The level of the enemy (default is 1).
        """
        super().__init__(hit_points=hit_points, x=x, y=y)
        self.type = "Entities"
        self.color = color
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.speed = speed
        self.range = range
        self.ammo = ammo
        self.damage = damage
        self.attack_speed = attack_speed
        self.weakness = weakness
        self.cost = cost
        self.level = level


    def draw(self):
        """
        Draw the enemy on the game screen.
        """
        # pygame.draw.rect(self.game.screen, self.color, self.rect, border_radius=6)


class EnemyFactory:
    """
    A factory class for creating different types of enemies
    """
    @staticmethod
    def create_enemy(enemy_type, x, y):
        """
        Create an enemy of the specifier type.
        
        Args:
            game (Game): The game instance.
            enemy_type (str): The type of enemy to create.
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
            
        Returns:
            Enemy: an instance of the created enemy.
        """
        if enemy_type == "goblin":
            return Enemy(x=x, y=y, color="green", hit_points=50, speed=3.0, 
                         range=80, ammo="normal", damage=10, attack_speed=0.35, weakness="fire",
                         cost=100, level=1)
        
        elif enemy_type == "orc":
            return Enemy(x=x, y=y, color="grey", hit_points=120, speed=1.8, 
                         range=15, ammo="pierce", damage=22, attack_speed=0.20, weakness="fire",
                         cost=300, level=1)
        
        elif enemy_type == "troll":
            return Enemy(x=x, y=y, color="brown", hit_points=250, speed=1.0, 
                         range=15, ammo="blunt", damage=40, attack_speed=0.1, weakness="pierce",
                         cost=300, level=1)
