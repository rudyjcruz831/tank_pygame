import pygame
import random
import math

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

    def update(self, walls, bullets):
        self.rect.x += self.direction[0] * 5
        self.rect.y += self.direction[1] * 5

        # handle wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.direction = self.get_random_direction()
                self.bounce_count += 1
                if self.bounce_count >= 6:
                    self.kill()
                break

    @staticmethod
    def get_random_direction():
        angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
        return random.choice([(math.cos(angle), math.sin(angle)) for angle in angles])
