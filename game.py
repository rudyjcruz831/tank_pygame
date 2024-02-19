import pygame
import sys
import random
from maze import Maze
from utils.maze_list import MAZE_LIST
from tank import Tank
from utils.colors import WHITE, RED, COLORS
from utils.sizes import BLOCK_SIZE, MAZE_WIDTH, MAZE_HEIGHT
from sfx import damage_sound_effect
from utils.menu import draw_menu
from time import time

pygame.init()
# maze pattern
pattern = random.choice(MAZE_LIST)
# map color
maze_color = random.choice(COLORS)
bg_color = random.choice(COLORS)

while bg_color == maze_color or bg_color == COLORS[0]:
    bg_color = random.choice(COLORS)


def quit_game():
    pygame.quit()
    sys.exit()


class Game:
    def __init__(self):
        # screen settings
        self.width = MAZE_WIDTH * BLOCK_SIZE
        self.mid_w = self.width // 2
        self.height = MAZE_HEIGHT * BLOCK_SIZE
        self.mid_h = self.height // 2
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Combat - Tank (Atari 2600)")
        # game controls
        self.game_start = False
        self.show_credits = False
        self.clock = pygame.time.Clock()
        # maze
        self.maze = Maze(pattern, maze_color)
        # tanks
        self.tank1_id = 1
        self.tank2_id = 2
        self.tank1 = Tank(1, 1, WHITE, BLOCK_SIZE, self.tank1_id, self.maze.walls)
        self.tank2 = Tank(MAZE_WIDTH - 2, MAZE_HEIGHT - 2, WHITE, BLOCK_SIZE, self.tank2_id, self.maze.walls)
        # bullet and sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank1, self.tank2)
        # player groups
        self.players = []
        self.players.append(self.tank1)
        self.players.append(self.tank2)

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
                        self.tank1.fire_bullet()
                    elif event.key == pygame.K_RETURN:
                        self.tank2.fire_bullet()
                # handle menu screen events
                elif not self.game_start:
                    if event.key == pygame.K_SPACE and not self.show_credits:
                        self.game_start = True
                    elif event.key == pygame.K_RETURN:
                        self.show_credits = not self.show_credits

    def draw_players(self, tank):
        if tank.life > 0:
            tank.draw_pointer(self.screen)
            tank.all_sprites.draw(self.screen)

    def update(self):
        # checks collision
        for player in self.players:
            for other_player in self.players:
                if other_player.id != player.id:
                    collisions = pygame.sprite.spritecollide(player, other_player.bullets, True)
                    if collisions:
                        player.life -= 1
                        damage_sound_effect.play()
        # draw tanks dir
        self.draw_players(self.tank1)
        self.draw_players(self.tank2)
        # update all
        self.all_sprites.update(self.maze.walls)

    def draw_game(self):
        self.screen.fill(bg_color)
        self.maze.draw(self.screen)
        # draw tank and bullets
        # tem que fazer parar de desenhar quando ele morrer
        self.all_sprites.draw(self.screen)

    def run(self):
        running = True
        while running:
            if self.game_start:
                self.draw_game()
            else:
                draw_menu(self.screen, self.show_credits, self.mid_w, self.mid_h)
            self.update()
            self.handle_events()
            pygame.display.flip()
            self.clock.tick(60)
