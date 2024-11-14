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

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        # mask
        # self.mask = pygame.mask.from_surface(self.image)
        """
        MASK IS REALLY PROCESSORVOR? IT USES A LOT THE PROCESSOR
        YOU SHOULD NOT USE IT EVERYWHERE OR YOUR PERFORMANCES WILL DROP
        BY A LOT
        HERE I COMMENTED OUT THE SELF.MASK BECAUSE PYGAME.SPRITE.COLLIDE_MASK CREATES A MASK IF THERE IS NONE
        SO IT IS NO NECESSARY
        """


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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
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
        self.original_surf = img_surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        self.rotation = 0
        self.rotation_orientation = random.choice((-50, 50))

        """
        PRACTICE TIMERS
        self.destroy_cooldown = 3000
        self.time = pygame.time.get_ticks()
        """


    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        self.rotation += self.rotation_orientation * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        """
        PRACTICE TIMERS
        if pygame.time.get_ticks() - self.time > self.destroy_cooldown:
            self.kill()
        """

def collisions():
    global running

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) # mask used for pixel perfect collision
    if collision_sprites:
        player.kill()
        running = False

    for laser in laser_sprites:
        collide = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collide:
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240, 240, 240))  # No anti alias for pixel art fonts
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240, 240 ,240), text_rect.inflate(20, 10).move(0, -8), 5, 10)


# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()
fps = 0.0

# import
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40) # none = default font


# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

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
            Meteor(meteor_surf, (random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)), (all_sprites, meteor_sprites)) # all_sprites used for update and draw method, meteor_sprites for collisions

    # update
    all_sprites.update(dt)

    # collisions
    collisions()

    # draw the game
    # fill the window with a color
    display_surface.fill("#3a2e3f")
    all_sprites.draw(display_surface)
    display_score()

    pygame.display.update()

pygame.quit()