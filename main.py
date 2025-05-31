import sys
import pygame
from player import Player
from gamestats import GameStats
from asteroid import Asteroid
from asteroidfield import AsteroidField
from projectile import Projectile
from constants import *

def draw_start_screen(screen):
    screen.fill("black")
    title_font = pygame.font.Font(None, 60)
    title_text = title_font.render("ASTEROIDS", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect.topleft)

    menu_font = pygame.font.Font(None, 36)
    start_button_text = menu_font.render("Start Game", True, (255, 255, 255))
    start_button_rect = start_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  + 100))
    screen.blit(start_button_text, start_button_rect.topleft)
    return start_button_rect

def initialize_objects():

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    GameStats.containers = (updateable ,drawable)
    game_stats = GameStats()
    
    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updateable, drawable)
    AsteroidField.containers = (updateable)
    asteroid_field = AsteroidField()
    
    projectiles = pygame.sprite.Group()
    Projectile.containers = (projectiles, updateable, drawable)

    return {
        "updateable": updateable,
        "drawable": drawable,
        "player": player,
        "game_stats": game_stats,
        "asteroids": asteroids,
        "asteroid_field": asteroid_field,
        "projectiles": projectiles
    }

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    game_clock = pygame.time.Clock()
    game_state = "start"
    running = True
    dt = 0

    objects = initialize_objects()
    updateable = objects["updateable"]
    drawable = objects["drawable"]
    asteroids = objects["asteroids"]
    player = objects["player"]
    projectiles = objects["projectiles"]
    game_stats = objects["game_stats"]

    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    if start_button_rect.collidepoint(event.pos):
                        game_state = "game"
        if game_state == "start":
            start_button_rect = draw_start_screen(screen)
        elif game_state == "game":
            screen.fill("black")
            updateable.update(dt)
            for asteroid in asteroids:
                if asteroid.check_collision(player):
                    game_stats.remove_life()
                    if game_stats.get_lives() <= 0:
                        print("Game over!")
                        running = False
            for asteroid in asteroids:
                for projectile in projectiles:
                    if asteroid.check_collision(projectile):
                        asteroid.split()
                        projectile.kill()
                        game_stats.add_score(ASTEROID_SCORE_VALUE)
            for object in drawable:
                object.draw(screen)

        tick = game_clock.tick(60)
        dt = tick / 1000    
        pygame.display.flip()

if __name__ == "__main__":
    main()
