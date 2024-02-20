import pygame
from wall import Wall

pygame.init()


class Maze:
    def __init__(self, pattern, color):
        self.pattern = pattern
        self.color = color
        self.size = 0
        self.walls = pygame.sprite.Group()
        for y, row in enumerate(pattern):
            for x, char in enumerate(row):
                if char == "#":
                    self.size += 1
                    wall = Wall(x, y, color)
                    self.walls.add(wall)

    def draw(self, screen):
        self.walls.draw(screen)
