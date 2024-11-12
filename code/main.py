import random

import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha() # convert or convert_alpha to improve performances
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_q])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_z])
        self.direction = self.direction.normalize() if self.direction != pygame.Vector2() else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("fire laser")

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'star.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))


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

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
for _ in range(20):
    star = Star(all_sprites)

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

while running:
    dt = clock.tick() / 1000
    pygame.display.set_caption("FPS = " + str(fps))
    fps = "%.2f" % clock.get_fps()

    # event lop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    # draw the game
    # fill the window with a red color
    display_surface.fill("darkgrey")
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()