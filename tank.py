import pygame
import math
from time import time
from bullet import Bullet
from utils.colors import RED
from sfx import shoot_sound_effect

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, id, obstacles):
        super().__init__()
        self.color = color
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        # physics
        self.spawned = True
        self.rect = self.image.get_rect(topleft=(x * size, y * size))
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
        elif direction == 'down':
            self.dy = 5
            self.block_dy = 35
            self.block_dx = 0
        elif direction == 'left':
            self.dx = -5
            self.block_dy = 0
            self.block_dx = -35
        elif direction == 'right':
            self.dx = 5
            self.block_dx = 35
            self.block_dy = 0
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
        # draws black square as a tank pointer
        pygame.draw.rect(screen, (0, 0, 0), self.rect_block)

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