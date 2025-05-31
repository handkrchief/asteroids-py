import sys
import pygame
from player import Player
from gamestats import GameStats
from asteroid import Asteroid
from asteroidfield import AsteroidField
from projectile import Projectile
from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_clock = pygame.time.Clock()
    dt = 0

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    GameStats.containers = (drawable)
    game_stats = GameStats()
    
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable)
    asteroid_field = AsteroidField()
    
    projectiles = pygame.sprite.Group()
    Projectile.containers = (projectiles, updateable, drawable)


    while (True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        tick = game_clock.tick(60)
        dt = tick / 1000
        updateable.update(dt)
        for asteroid in asteroids:
            if asteroid.check_collision(player):
                print("Game over!")
                sys.exit()
        for asteroid in asteroids:
            for projectile in projectiles:
                if asteroid.check_collision(projectile):
                    asteroid.split()
                    projectile.kill()
                    game_stats.add_score(ASTEROID_SCORE_VALUE)
        for object in drawable:
            object.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
