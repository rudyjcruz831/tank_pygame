import pygame
import sys
import random
from maze import Maze
from utils.maze_list import MAZE_LIST
from bullet import Bullet
from tank import Tank
from fonts import screen_font, screen_font_bold
from utils.colors import BLACK, WHITE, RED, COLORS
from utils.sizes import BLOCK_SIZE, MAZE_WIDTH, MAZE_HEIGHT
from sfx import shoot_sound_effect

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
        self.tank1 = Tank(1, 1, WHITE, BLOCK_SIZE, 1, self.maze.walls)
        self.tank2 = Tank(MAZE_WIDTH - 2, MAZE_HEIGHT - 2, WHITE, BLOCK_SIZE, 2, self.maze.walls)
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
                # handle shooting
                if self.game_start:
                    if event.key == pygame.K_SPACE:
                        self.fire_bullet(self.tank1)
                        shoot_sound_effect.play()
                    elif event.key == pygame.K_RETURN:
                        self.fire_bullet(self.tank2)
                        shoot_sound_effect.play()
                # handle menu screen events
                elif not self.game_start:
                    if event.key == pygame.K_SPACE and not self.show_credits:
                        self.game_start = True
                    elif event.key == pygame.K_RETURN:
                        self.show_credits = not self.show_credits

    def update(self):
        self.all_sprites.update(self.maze.walls, self.bullets)
        # tanks dir
        self.tank1.draw_pointer(self.screen)
        self.tank2.draw_pointer(self.screen)

    def draw_game(self):
        self.screen.fill(bg_color)
        self.maze.draw(self.screen)
        # draw tank and bullets
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
            bullet_direction = (self.tank1.block_dx / 3, self.tank1.block_dy / 3)
        elif tank == self.tank2:
            bullet_direction = (self.tank2.block_dx/3, self.tank2.block_dy/3)
        bullet = Bullet(tank.rect_block.centerx, tank.rect_block.centery, bullet_direction, RED)
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
