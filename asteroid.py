import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def create_split_asteroid(self, angle):
        ast_velocity = self.velocity.rotate(angle)
        ast_radius = self.radius - ASTEROID_MIN_RADIUS
        ast = Asteroid(self.position.x, self.position.y, ast_radius)
        ast.velocity = ast_velocity * 1.2
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            split_angle = random.uniform(20.0, 50.0)
            self.create_split_asteroid(split_angle)
            self.create_split_asteroid(-split_angle)
