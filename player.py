import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN, PLAYER_BOMB_COOLDOWN, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED
from projectile import Projectile
from bombprojectile import BombProjectile

class Player(CircleShape):
    
    def __init__(self ,x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shot_cooldown = 0
        self.bomb_cooldown = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()
        
        if keys[pygame.K_b]:
            self.shoot_bomb()

        self.shot_cooldown = max(0, self.shot_cooldown - dt)
        self.bomb_cooldown = max(0, self.bomb_cooldown - dt)
    
    def shoot(self):
        if self.shot_cooldown == 0:
            new_projectile = Projectile(self.position.x, self.position.y)
            new_projectile.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_cooldown += PLAYER_SHOOT_COOLDOWN
        
    def shoot_bomb(self):
        if self.bomb_cooldown == 0:
            new_bomb = BombProjectile(self.position.x, self.position.y)
            new_bomb.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.bomb_cooldown += PLAYER_BOMB_COOLDOWN
    