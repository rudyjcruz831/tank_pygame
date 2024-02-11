import pygame

pygame.init()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        super().__init__()
        self.color = color
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x * size, y * size))
        self.dx = 0
        self.dy = 0

    def update(self, walls, bullets):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # handle wall collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if self.dx > 0:
                    self.rect.right = wall.rect.left
                elif self.dx < 0:
                    self.rect.left = wall.rect.right
                elif self.dy > 0:
                    self.rect.bottom = wall.rect.top
                elif self.dy < 0:
                    self.rect.top = wall.rect.bottom

        # handle bullet collision
        bullet_hit = pygame.sprite.spritecollideany(self, bullets)
        if bullet_hit:
            self.kill()

    def death(self):
        # moves tank out of screen
        self.rect.topleft = (1000, 1000)
