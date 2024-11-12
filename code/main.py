import random

import pygame
from os.path import join

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
fps = 0.0

# plain surface
surf = pygame.Surface((100, 200))
surf.fill("orange")

# importing an image
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha() # convert or convert_alpha to improve performances
player_rect = player_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 20))
player_direction = pygame.Vector2(2, -1)
player_speed = 10

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_position = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(20)] # add 20 random positions in a list

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

while running:
    clock.tick(100)
    pygame.display.set_caption("FPS = " + str(fps))
    fps = "%.2f" % clock.get_fps()
    # event lop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    # fill the window with a red color
    display_surface.fill("darkgrey")

    for pos in star_position:
        display_surface.blit(star_surf, pos)

    # player movement
    player_rect.center += player_direction * player_speed

    display_surface.blit(meteor_surf, meteor_rect)
    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(player_surf, player_rect)  # put one surface on another surface (display_surface)
    pygame.display.update()

pygame.quit()