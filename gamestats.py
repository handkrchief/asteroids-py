import pygame
from constants import SCREEN_WIDTH, PLAYER_DAMAGE_COOLDOWN, PLAYER_MAX_LIVES


class GameStats(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.score = 0
        self.lives = PLAYER_MAX_LIVES
        self.damage_cooldown = 0
        self.font = pygame.font.SysFont(None, 36)

    def add_score(self, points):
        self.score += points
    
    def get_score(self):
        return self.score
    
    def get_lives(self):
        return self.lives

    def add_lives(self, lives):
        self.lives = max(PLAYER_MAX_LIVES, self.lives + lives)

    def remove_life(self):
        if self.damage_cooldown == 0:
            self.lives -= 1
            self.damage_cooldown += PLAYER_DAMAGE_COOLDOWN
            
    def update(self, dt):
        if self.damage_cooldown > 0:
            self.damage_cooldown = max(0, self.damage_cooldown - dt)        

    def draw(self, screen):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        life_surface = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        surface_width = score_surface.get_width()
        surface_center = (SCREEN_WIDTH / 2) - (surface_width / 2)
        screen.blit(score_surface, (surface_center, 10))
        screen.blit(life_surface, (10, 10))
