import pygame
import sys
import random
from maze import Maze
from utils.maze_list import MAZE_LIST
from tank import Tank
from utils.colors import WHITE, COL_GROUP_1, COL_GROUP_2
from utils.sizes import BLOCK_SIZE, MAZE_WIDTH, MAZE_HEIGHT
from sfx import damage_sound_effect
from utils.menu import draw_menu
from time import time

pygame.init()


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
        self.tank1_died = False
        self.tank2_died = False
        self.clock = pygame.time.Clock()
        # background
        self.bg_color = random.choice(COL_GROUP_1)
        # maze
        self.pattern = random.choice(MAZE_LIST)
        self.maze_color = random.choice(COL_GROUP_2)
        self.maze = Maze(self.pattern, self.maze_color)
        # tanks
        self.tank1 = Tank(1, 1, WHITE, BLOCK_SIZE, 1, self.maze.walls)
        self.tank2 = Tank(MAZE_WIDTH - 2, MAZE_HEIGHT - 2, WHITE, BLOCK_SIZE, 2, self.maze.walls)
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
                    if event.key == pygame.K_SPACE and not self.tank1_died:
                        self.tank1.fire_bullet()
                    elif event.key == pygame.K_RETURN and not self.tank2_died:
                        self.tank2.fire_bullet()
                # handle menu screen events
                elif not self.game_start:
                    if event.key == pygame.K_SPACE and not self.show_credits:
                        self.game_start = True
                    elif event.key == pygame.K_RETURN:
                        self.show_credits = not self.show_credits

    def handle_next_round(self, tank):
        if tank.id == 1:
            self.tank1_died = True
        else:
            self.tank2_died = True
        # maze pattern
        self.pattern = random.choice(MAZE_LIST)
        # map color
        self.bg_color = random.choice(COL_GROUP_1)
        self.maze_color = random.choice(COL_GROUP_2)
        self.maze = Maze(self.pattern, self.maze_color)
        # update tanks stats
        self.tank1.obstacles = self.tank2.obstacles = self.maze.walls
        self.tank1_died = self.tank2_died = False
        # respawn fired tank
        tank.respawn()
        tank.life = 1

    def draw_player(self, tank):
        if tank.life > 0:
            tank.draw_pointer(self.screen)
            tank.all_sprites.draw(self.screen)
        else:
            self.handle_next_round(tank)

    def update(self):
        # checks collision
        for player in self.players:
            for other_player in self.players:
                if other_player.id != player.id:
                    collisions = pygame.sprite.spritecollide(player, other_player.bullets, True)
                    if collisions:
                        player.life -= 1
                        damage_sound_effect.play()
        # draw tanks
        for player in self.players:
            self.draw_player(player)
        # update all
        self.all_sprites.update(self.maze.walls)

    def draw_game(self):
        self.screen.fill(self.bg_color)
        self.maze.draw(self.screen)
        # draw tank and bullets
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
