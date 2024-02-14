import pygame
import math
from sfx import damage_sound_effect

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, tank_id, obstacles):
        super().__init__()
        # design
        self.color = color
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        # physics
        self.rect = self.image.get_rect(topleft=(x * size, y * size))
        self.dx = 0
        self.dy = 0
        self.id = tank_id
        self.obstacles = obstacles
        self.rect_block = pygame.Rect(100, 200, 10, 10)
        self.block_dx = 0
        self.block_dy = 0

    def update(self, walls, bullets):
        self.rect_block.centerx = self.rect.centerx + self.block_dx
        self.rect_block.centery = self.rect.centery + self.block_dy
        # handle movement
        self.rect.x += self.dx
        self.rect.y += self.dy
        # handle collision
        self.collider_wall('horizontal')
        self.collider_wall('vertical')
        # handle bullet collision
        bullet_hit = pygame.sprite.spritecollideany(self, bullets)
        if bullet_hit:
            self.death()  # assuming death method handles tank removal
        self.move()

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
        for wall in self.obstacles:
            if self.rect.colliderect(wall):
                if direction == 'horizontal':
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                    if self.dx < 0:
                        self.rect.left = wall.rect.right
                elif direction == 'vertical':
                    if self.dy > 0:
                        self.rect.bottom = wall.rect.top
                    if self.dy < 0:
                        self.rect.top = wall.rect.bottom

    def death(self):
        # moves tank out of screen
        self.rect.topleft = (1000, 1000)
        damage_sound_effect.play()

    def draw_pointer(self, screen):
        # draws black square as a pointer of tank direction
        pygame.draw.rect(screen, (0, 0, 0), self.rect_block)

    def fire_bullet(self):
        pass
