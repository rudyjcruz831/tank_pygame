import pygame
import random
import math
from time import time
from sfx import hit_sound_effect

pygame.init()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, size=(10, 10)):
        super().__init__()
        # Load bullet image
        self.original_image = pygame.image.load("tank_bulletFly3.png").convert_alpha()
        # Create a new surface with the desired size
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # Scale the original image and blit onto the new surface
        self.image.blit(pygame.transform.scale(self.original_image, size), (0, 0))
        # Set the position
        self.rect = self.image.get_rect(center=(x, y))
        # other attributes
        self.color = color
        # actions
        self.direction = direction
        self.bounce_count = 0
        self.hits = 0
        self.move_x = self.direction[0] / 2
        self.move_y = self.direction[1] / 2
        self.collision_initial_time = time()
        self.collision_final_time = time()

    def update(self, walls):
        size = (10, 10)  # Define the desired size of the bullet
        self.collision_final_time = time()
        # handle movement
        self.rect.x += self.move_x * 1
        self.collision('horizontal', walls)
        self.rect.y += self.move_y * 1
        self.collision('vertical', walls)
        if self.hits >= 6:
            self.kill()
        # Rotate the image based on direction
        if self.move_x == 0:  # Vertical movement
            if self.move_y > 0:  # Moving down
                rotated_image = pygame.transform.rotate(pygame.transform.scale(self.original_image, size), 90)
                self.image = rotated_image
            elif self.move_y < 0:  # Moving up
                rotated_image = pygame.transform.rotate(pygame.transform.scale(self.original_image, size), -90)
                self.image = rotated_image
        elif self.move_y == 0:  # Horizontal movement
            if self.move_x > 0:  # Moving right
                self.image = pygame.transform.scale(self.original_image, size)  # No rotation needed
            elif self.move_x < 0:  # Moving left
                rotated_image = pygame.transform.rotate(pygame.transform.scale(self.original_image, size), 180)
                self.image = rotated_image

    def change_dir(self, dir):
        if dir == 'x':
            self.move_x *= -1
        else:
            self.move_y *= -1
        # Rotate the image when changing direction
        self.image = pygame.transform.rotate(self.image, 180)  # Rotate by 180 degrees
        self.collision_initial_time = time()
        self.hits += 1
        hit_sound_effect.play()

    def collision(self, direction, walls):
        for wall in walls:
            if direction == 'horizontal':
                if self.collision_final_time - self.collision_initial_time > 0.1:
                    if self.rect.colliderect(wall):
                        self.change_dir('x')
            if direction == 'vertical':
                if self.collision_final_time - self.collision_initial_time > 0.1:
                    if self.rect.colliderect(wall):
                        self.change_dir('y')

    @staticmethod
    def get_random_direction():
        angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
        return random.choice([(math.cos(angle), math.sin(angle)) for angle in angles])
