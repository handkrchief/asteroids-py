
import math
import pygame
from projectile import Projectile
from constants import BOMB_RADIUS, PLAYER_SHOOT_SPEED

class BombProjectile(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.radius = BOMB_RADIUS
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)
    
    def explode(self, screen):
        for i in range(10):
            angle = i * (360 / 10)
            new_projectile = Projectile(self.position.x, self.position.y)
            angle_radians = math.radians(angle)
            vx = PLAYER_SHOOT_SPEED * math.cos(angle_radians)
            vy = PLAYER_SHOOT_SPEED * math.sin(angle_radians)
            new_projectile.velocity = pygame.math.Vector2(vx, vy)
