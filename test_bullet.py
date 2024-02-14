import pygame
import random
import math
from time import time
pygame.init()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.bounce_count = 0
        self.hits = 0
        self.move_x = self.direction[0]
        self.move_y = self.direction[1]
        self.colision_initial_time = time()
        self.colision_final_time = time()


    def update(self, walls, bullets):
        self.colision_final_time = time()

        self.rect.x += self.move_x * 1
        self.collision('horizontal', walls)

        self.rect.y += self.move_y * 1
        self.collision('vertical', walls)

        if self.hits >= 6:
            self.kill()

    def collision(self, direction,walls):
        if direction == 'horizontal':
            for wall in walls:
                if self.colision_final_time - self.colision_initial_time > 0.1:
                    if self.rect.colliderect(wall):
                        self.move_x *= -1
                        self.colision_initial_time = time()
                        self.hits += 1

        if direction == 'vertical':
            for wall in walls:
                if self.colision_final_time - self.colision_initial_time > 0.1:
                    if self.rect.colliderect(wall):
                        self.move_y *= -1
                        self.colision_initial_time = time()
                        self.hits += 1

    @staticmethod
    def get_random_direction():
        angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
        return random.choice([(math.cos(angle), math.sin(angle)) for angle in angles])