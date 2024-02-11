import pygame
import sys
import random
from test_maze import Maze
from maze_list import MAZE_LIST
from test_bullet import Bullet
from test_tank import Tank
from fonts import hud_font, screen_font, screen_font_bold
from sfx import hit_sound_effect, scoring_sound_effect, damage_sound_effect, shoot_sound_effect
from colors import BLACK, WHITE, RED, COLORS
from sizes import BLOCK_SIZE, MAZE_WIDTH, MAZE_HEIGHT

pygame.init()
# maze pattern
pattern = random.choice(MAZE_LIST)
# map color
maze_color = random.choice(COLORS)
bg_color = random.choice(COLORS)

while bg_color == maze_color:
    bg_color = random.choice(COLORS)


def quit_game():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        self.width = MAZE_WIDTH * BLOCK_SIZE
        self.mid_w = self.width // 2
        self.height = MAZE_HEIGHT * BLOCK_SIZE
        self.mid_h = self.height // 2
        self.game_start = False
        self.show_credits = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank Maze - Atari 2600")
        self.clock = pygame.time.Clock()
        self.maze = Maze(pattern, maze_color)
        self.tank1 = Tank(1, 1, WHITE, BLOCK_SIZE)
        self.tank2 = Tank(MAZE_WIDTH - 2, MAZE_HEIGHT - 2, WHITE, BLOCK_SIZE)
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank1, self.tank2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit_game()
                # handle game events
                if self.game_start:
                    if event.key == pygame.K_SPACE:
                        self.fire_bullet(self.tank1)
                    elif event.key == pygame.K_RETURN:
                        self.fire_bullet(self.tank2)
                # handle menu screen events
                elif not self.game_start:
                    if event.key == pygame.K_SPACE and not self.show_credits:
                        self.game_start = True
                    elif event.key == pygame.K_RETURN:
                        self.show_credits = not self.show_credits

    def update(self):
        self.tank1.dx, self.tank1.dy = 0, 0
        self.tank2.dx, self.tank2.dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.tank1.dx = -5
        elif keys[pygame.K_RIGHT]:
            self.tank1.dx = 5
        elif keys[pygame.K_UP]:
            self.tank1.dy = -5
        elif keys[pygame.K_DOWN]:
            self.tank1.dy = 5
        if keys[pygame.K_a]:
            self.tank2.dx = -5
        elif keys[pygame.K_d]:
            self.tank2.dx = 5
        elif keys[pygame.K_w]:
            self.tank2.dy = -5
        elif keys[pygame.K_s]:
            self.tank2.dy = 5
        self.all_sprites.update(self.maze.walls, self.bullets)

    def draw_game(self):
        self.screen.fill(bg_color)
        self.maze.draw(self.screen)
        self.all_sprites.draw(self.screen)

    def draw_menu(self):
        self.screen.fill(BLACK)
        # create title
        title_txt = "TANK - COMBAT" if not self.show_credits else "CREDITS"
        title = screen_font_bold.render(title_txt, True, WHITE, BLACK)
        title_w = title.get_width()
        title_h = title.get_height()
        if not self.show_credits:
            # Subtitle
            subtitle_txt = "[Play game (space)] | [Show credits (enter)]"
            subtitle = screen_font.render(subtitle_txt, True, WHITE, BLACK)
            subtitle_w = subtitle.get_width()
            # Draw title and subtitle
            self.screen.blit(title, (self.mid_w - title_w // 2, self.mid_h - title_h // 2))
            self.screen.blit(subtitle, (self.mid_w - subtitle_w // 2, self.mid_h + title_h // 2))
        else:
            # draw title
            self.screen.blit(title, (self.mid_w - title_w // 2, (self.mid_h // 2) - title_h // 2))
            # subtitles
            credit_rows = [
                "<----- DEVELOPERS ----->",
                "Pedro Yutaro Mont Morency Nakamura",
                "Aline Daffiny Ferreira Gomes",
                "Leonardo Melo Crispim",
                "<----- SPRITE SOURCE ----->",
                "Dune 2: TBD",
                "[Back to menu (enter)]"
            ]
            # draw each subtitle
            space = 40
            for row in credit_rows:
                subtitle = screen_font.render(row, True, WHITE, BLACK)
                subtitle_w = subtitle.get_width()
                space += 80 if credit_rows.index(row) in (4, 6) else 40
                self.screen.blit(subtitle, (self.mid_w - subtitle_w // 2, (self.mid_h + title_h) // 2 + space))

    def fire_bullet(self, tank):
        bullet_direction = (0, 0)
        if tank == self.tank1:
            bullet_direction = (self.tank1.dx, self.tank1.dy)
        elif tank == self.tank2:
            bullet_direction = (self.tank2.dx, self.tank2.dy)
        bullet = Bullet(tank.rect.centerx + 5, tank.rect.centery + 5, bullet_direction, RED)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def run(self):
        running = True
        while running:
            if self.game_start:
                self.draw_game()
            else:
                self.draw_menu()
            self.update()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(60)
