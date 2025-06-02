import sys
import pygame
from bombprojectile import BombProjectile
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
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - MENU_OFFSET))
    screen.blit(title_text, title_rect.topleft)

    menu_font = pygame.font.Font(None, 36)
    start_button_text = menu_font.render("Start Game", True, (255, 255, 255))
    start_button_rect = start_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  + MENU_OFFSET))
    screen.blit(start_button_text, start_button_rect.topleft)
    return start_button_rect

def draw_end_screen(screen, game_stats):
    screen.fill("black")
    end_font = pygame.font.Font(None, 60)
    end_text = end_font.render("Game Over", True, (255, 255, 255))
    end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - MENU_OFFSET))
    screen.blit(end_text, end_rect.topleft)

    menu_font = pygame.font.Font(None, 36)
    score_text = menu_font.render(f"Score: {game_stats.get_score()}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect.topleft)
    restart_button_text = menu_font.render("Restart", True, (255, 255, 255))
    restart_button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  + MENU_OFFSET))
    screen.blit(restart_button_text, restart_button_rect.topleft)
    return restart_button_rect

def initialize_objects():

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updateable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    GameStats.containers = (updateable ,drawable)
    game_stats = GameStats()
    game_stats.add_lives(PLAYER_MAX_LIVES)

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

def reinitialize_objects():
    objects = initialize_objects()
    return (
        objects["updateable"],
        objects["drawable"],
        objects["asteroids"],
        objects["player"],
        objects["projectiles"],
        objects["game_stats"],
    )

def handle_collisions(player, asteroids, projectiles, game_stats):
    for asteroid in asteroids:
        if asteroid.check_collision(player):
            game_stats.remove_life()
            if game_stats.get_lives() <= 0:
                return STATE_END
    for asteroid in asteroids:
        for projectile in projectiles:
            if asteroid.check_collision(projectile):
                if isinstance(projectile, BombProjectile):
                    projectile.explode(projectiles)
                    projectile.kill()
                else:
                    asteroid.split()
                    projectile.kill()
                    game_stats.add_score(ASTEROID_SCORE_VALUE)
    return STATE_GAME

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    icon = pygame.image.load('pixel_ship_red.png')
    pygame.display.set_icon(icon)
    game_clock = pygame.time.Clock()
    game_state = STATE_START
    running = True
    dt = 0

    updateable, drawable, asteroids, player, projectiles, game_stats = reinitialize_objects()

    while (running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == STATE_START:
                    if start_button_rect.collidepoint(event.pos):
                        game_state = STATE_GAME
                elif game_state == STATE_END:
                    if restart_button_rect.collidepoint(event.pos):
                        updateable, drawable, asteroids, player, projectiles, game_stats = reinitialize_objects()
                        game_state = STATE_GAME
        if game_state == STATE_START:
            start_button_rect = draw_start_screen(screen)
        elif game_state == STATE_GAME:
            screen.fill("black")
            updateable.update(dt)
            game_state = handle_collisions(player, asteroids, projectiles, game_stats)
            for object in drawable:
                object.draw(screen)
        elif game_state == STATE_END:
            restart_button_rect = draw_end_screen(screen, game_stats)
        tick = game_clock.tick(60)
        dt = tick / 1000    
        pygame.display.flip()

if __name__ == "__main__":
    main()
