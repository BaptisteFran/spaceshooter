import random

import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('../images', 'player.png')).convert_alpha() # convert or convert_alpha to improve performances
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 300

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_q])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_z])
        self.direction = self.direction.normalize() if self.direction != pygame.Vector2() else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, img_surf):
        super().__init__(groups)
        self.image = img_surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, img_surf, pos, groups):
        super().__init__(groups)
        self.image = img_surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, delta_time):
        self.rect.centery -= 400 * delta_time
        if self.rect.bottom < 0:
            self.kill() # destroy self, this is a pygame built-in function

class Meteor(pygame.sprite.Sprite):
    def __init__(self, img_surf, pos, groups):
        super().__init__(groups)
        self.image = img_surf
        self.rect = self.image.get_frect(center = pos)
        """
        PRACTICE TIMERS
        self.destroy_cooldown = 3000
        self.time = pygame.time.get_ticks()
        """


    def update(self, delta_time):
        self.rect.centery += 400 * delta_time
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        """
        PRACTICE TIMERS
        if pygame.time.get_ticks() - self.time > self.destroy_cooldown:
            self.kill()
        """


# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
fps = 0.0

# import
star_surf = pygame.image.load(join('../images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('../images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('../images', 'laser.png')).convert_alpha()

# sprites
all_sprites = pygame.sprite.Group()
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    pygame.display.set_caption("FPS = " + str(fps))
    fps = "%.2f" % clock.get_fps()

    # event lop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surf, (random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)), all_sprites)

    all_sprites.update(dt)

    # draw the game
    # fill the window with a color
    display_surface.fill("darkgrey")
    all_sprites.draw(display_surface)
    pygame.display.update()

pygame.quit()