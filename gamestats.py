import pygame


class GameStats(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def add_score(self, points):
        self.score += points
    
    def draw(self, screen):
        score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
