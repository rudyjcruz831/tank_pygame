from sizes import BLOCK_SIZE
import pygame

pygame.init()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
