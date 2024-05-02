import pygame
import math
from time import time
from bullet import Bullet
from utils.colors import RED
from sfx import shoot_sound_effect

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, id, obstacles, scale=1):
        super().__init__()
        self.color = color
        self.size = size
        # Load sprite image
        original_image = pygame.image.load("tanks_tankGrey2.png").convert_alpha()
        # Resize the image based on the scale
        scaled_width = 1 * size * scale
        scaled_height = 1 * size * scale
        self.original_image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.image = self.original_image
        # Calculate the position of the sprite
        sprite_x = x * size  # x-coordinate in game world
        sprite_y = y * size  # y-coordinate in game world
        # Set the position of the sprite
        self.rect = self.image.get_rect(topleft=(sprite_x, sprite_y))
        # Other attributes and methods remain the same...
        self.spawned = True
        self.dx = 0
        self.dy = 0
        self.id = id
        self.obstacles = obstacles
        self.rect_block = pygame.Rect(100, 200, 10, 10)
        self.block_dx = 0
        self.block_dy = 0
        self.tank1_initial_time = time()
        self.tank1_final_time = time()
        self.tank2_initial_time = time()
        self.tank2_final_time = time()
        self.score = 0
        self.angle = 0  # Initial angle
        # bullet and sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.life = 1

    def handle_initial_dir(self):
        if self.spawned:
            if self.id == 1:
                self.go_to('right')
            else:
                self.go_to('left')
        self.spawned = False

    def update(self, walls):
        # handle initial tank position
        self.handle_initial_dir()
        self.rect_block.centerx = self.rect.centerx + self.block_dx
        self.rect_block.centery = self.rect.centery + self.block_dy
        self.rect.x += self.dx
        self.collider_wall('horizontal')
        self.rect.y += self.dy
        self.collider_wall('vertical')
        self.move()
        self.tank1_final_time = time()
        self.tank2_final_time = time()

    def go_to(self, direction):
        if direction == 'up':
            self.dy = -5
            self.block_dy = -35
            self.block_dx = 0
            self.angle = 0  # Set angle to face upward
        elif direction == 'down':
            self.dy = 5
            self.block_dy = 35
            self.block_dx = 0
            # self.angle = 180  # Set angle to face downward
        elif direction == 'left':
            self.dx = -5
            self.block_dy = 0
            self.block_dx = -35
            self.angle = -90 # Set angle to rotate 90 degrees counterclockwise
        elif direction == 'right':
            self.dx = 5
            self.block_dx = 35
            self.block_dy = 0
            self.angle = 0 # Set angle to rotate 90 degrees clockwise
        # Normalize diagonal movement
        if self.dx != 0 and self.dy != 0:
            self.dx /= math.sqrt(2)
            self.dy /= math.sqrt(2)
            self.block_dy = self.dy * 10
            self.block_dx = self.dx * 10

    def move(self):
        keys = pygame.key.get_pressed()
        if self.id == 1:
            if keys[pygame.K_w]:
                self.go_to('up')
            elif keys[pygame.K_s]:
                self.go_to('down')
            else:
                self.dy = 0
            if keys[pygame.K_a]:
                self.go_to('left')
            elif keys[pygame.K_d]:
                self.go_to('right')
            else:
                self.dx = 0
        if self.id == 2:
            if keys[pygame.K_UP]:
                self.go_to('up')
            elif keys[pygame.K_DOWN]:
                self.go_to('down')
            else:
                self.dy = 0
            if keys[pygame.K_LEFT]:
                self.go_to('left')
            elif keys[pygame.K_RIGHT]:
                self.go_to('right')
            else:
                self.dx = 0

    def collider_wall(self, direction):
        self.all_sprites.update(self.obstacles)
        for wall in self.obstacles:
            if self.rect.colliderect(wall):
                if direction == 'horizontal':
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                    if self.dx < 0:
                        self.rect.left = wall.rect.right
                if direction == 'vertical':
                    if self.rect.colliderect(wall):
                        if self.dy > 0:
                            self.rect.bottom = wall.rect.top
                        if self.dy < 0:
                            self.rect.top = wall.rect.bottom

    def respawn(self):
        self.rect.topleft = (50, 50)

    def draw_pointer(self, screen):
        # Rotate the tank image and draw
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect)

    def fire_bullet(self):
        # handle bullet dir based on tank
        if self.id == 1:
            if self.tank1_final_time - self.tank1_initial_time > 2:
                bullet_direction = (self.block_dx / 3, self.block_dy / 3)
                self.tank1_initial_time = time()
                bullet = Bullet(self.rect_block.centerx, self.rect_block.centery, bullet_direction, RED)
                shoot_sound_effect.play()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        elif self.id == 2:
            if self.tank2_final_time - self.tank2_initial_time > 2:
                bullet_direction = (self.block_dx / 3, self.block_dy / 3)
                bullet = Bullet(self.rect_block.centerx, self.rect_block.centery, bullet_direction, RED)
                self.tank2_initial_time = time()
                shoot_sound_effect.play()
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
