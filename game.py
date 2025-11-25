import pygame as pg
from pygame.locals import *
import sys
import time
import random

from dino import Dino
from bird import Bird
from tree import Tree

pg.init()

class Game:
    def __init__(self):
        self.win = pg.display.set_mode((600, 300))
        pg.display.set_caption("Dino Run")

        self.ground1 = pg.image.load('assets/ground.png').convert_alpha()
        self.ground2 = pg.image.load('assets/ground.png').convert_alpha()

        self.ground1_rect = self.ground1.get_rect(center=(300, 250))
        self.ground2_rect = self.ground2.get_rect(center=(900, 250))

        self.clock = pg.time.Clock()

        self.dino=Dino()

        self.bird = None
        self.first_bird = True
        self.spawn_bird_timer = 0
        self.spawn_bird_delay = 10

        self.tree = None
        self.spawn_tree_timer = 0
        self.spawn_tree_delay = random.uniform(1.5, 5)

        self.game_lost = False
        self.move_speed = 250  # pixels per second

        self.gameloop()

    def spawn_bird(self):
        self.bird = Bird()
        self.spawn_bird_timer = 0
        
        if self.first_bird:
            self.spawn_bird_delay = 10
            self.first_bird = False
        else:
            self.spawn_bird_delay = random.uniform(2, 4)

    def spawn_tree(self):
        self.tree = Tree()
        self.spawn_tree_timer = 0
        self.spawn_tree_delay = random.uniform(1.5, 5)

    def gameloop(self):
        last_time = time.time()

        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        self.dino.jumpdino()

            if not self.game_lost:
                self.ground1_rect.x -= self.move_speed * dt
                self.ground2_rect.x -= self.move_speed * dt

                if self.ground1_rect.right < 0:
                    self.ground1_rect.x = self.ground2_rect.right
                if self.ground2_rect.right < 0:
                    self.ground2_rect.x = self.ground1_rect.right

                self.dino.update(dt)

            if self.bird is not None:
                self.bird.update(dt)

                if self.bird.rect.right < 0:
                    self.bird = None
                
            if self.bird is None:
                self.spawn_bird_timer += dt

                if self.spawn_bird_timer >= self.spawn_bird_delay:
                    self.spawn_bird()

            if self.tree is not None:
                self.tree.update(dt)

                if self.tree.rect.right < 0:
                    self.tree = None

            if self.tree is None:
                self.spawn_tree_timer += dt

                if self.spawn_bird_timer >= self.spawn_tree_delay:
                    self.spawn_tree()
                
            self.win.fill((255, 255, 255))
            self.win.blit(self.ground1, self.ground1_rect)
            self.win.blit(self.ground2, self.ground2_rect)
            self.win.blit(self.dino.image, self.dino.rect)
            
            if self.bird is not None:
                self.win.blit(self.bird.image, self.bird.rect)

            if self.tree is not None:
                self.win.blit(self.tree.image, self.tree.rect)

            pg.display.update()
            self.clock.tick(60)

game = Game()
