import pygame as pg
from pygame.locals import *
import sys
import time
import random

from dino import Dino
from bird import Bird
from tree import Tree
from cloud import Cloud

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
        self.spawn_bird_timer = 0
        self.spawn_bird_delay = random.uniform(3, 6)

        self.tree = None
        self.spawn_tree_timer = 0
        self.spawn_tree_delay = random.uniform(1.5, 5)

        self.game_lost = False
        self.move_speed = 250  # pixels per second

        self.show_hitbox = True

        self.score = 0
        self.high_score = 0
        self.font = pg.font.SysFont(None, 20)
        self.big_font = pg.font.SysFont(None, 35)

        self.clouds = []
        self.last_cloud_time = 0
        self.next_cloud_spawn = random.randint(2000, 4000)

        self.gameloop()

    def spawn_bird(self):
        self.bird = Bird()
        self.spawn_bird_timer = 0
        self.spawn_bird_delay = random.uniform(3, 6)

    def spawn_tree(self):
        self.tree = Tree()
        self.spawn_tree_timer = 0
        self.spawn_tree_delay = random.uniform(1.5, 5)

    def no_obstacle_on_screen(self):
        return self.bird is None and self.tree is None
    
    def check_collision(self):
        if self.tree is not None:
            if self.dino.hitbox.colliderect(self.tree.hitbox):
                return True
            
        if self.bird is not None:
            if self.dino.hitbox.colliderect(self.bird.hitbox):
                return True
        
        return False
    
    def draw_score(self):
        score_text = self.font.render(f'Score : {self.score}', True, (0, 0, 0))
        high_score_text = self.font.render(f'High Score : {self.high_score}', True, (0, 0, 0))
        self.win.blit(score_text, (480, 30))
        self.win.blit(high_score_text, (480, 15))

    def draw_game_over(self):
        text = self.big_font.render('GAME OVER', True, (0, 0, 0))
        restart_text = self.font.render('Press R To Restart', True, (0, 0, 0))
        self.win.blit(text, (220, 120))
        self.win.blit(restart_text, (230, 155))

    def spawn_cloud(self):
        cloud = Cloud()
        self.clouds.append(cloud)
        self.last_cloud_time = pg.time.get_ticks()
        self.next_cloud_spawn = random.randint(2000, 4000)

    def reset_game(self):
        self.dino = Dino()
        self.bird = None
        self.tree = None
        self.spawn_bird_timer = 0
        self.spawn_tree_timer = 0
        self.spawn_bird_delay = random.uniform(3, 6)
        self.spawn_tree_delay = random.uniform(1.5, 5)
        self.score = 0
        self.game_lost = False
        self.ground1_rect.x = 0
        self.ground2_rect.x = 600
        self.clouds = []
        self.last_cloud_time = 0
        self.next_cloud_spawn = random.randint(2000, 4000)

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
                    if event.key==pg.K_SPACE and not self.game_lost:
                        self.dino.jumpdino()

                    if event.key==pg.K_r and self.game_lost:
                        self.reset_game()

            if not self.game_lost:
                self.score += int(60 * dt)
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

                if self.tree is not None:
                    self.tree.update(dt)
                    if self.tree.rect.right < 0:
                        self.tree = None
                
                if self.no_obstacle_on_screen():
                    self.spawn_tree_timer += dt
                    self.spawn_bird_timer += dt

                    if self.spawn_tree_timer >= self.spawn_tree_delay:
                        self.spawn_tree()

                    elif self.spawn_bird_timer >= self.spawn_bird_delay:
                        self.spawn_bird()

                now = pg.time.get_ticks()
                if now - self.last_cloud_time >= self.next_cloud_spawn:
                    self.spawn_cloud()

                for cloud in self.clouds:
                    cloud.update(dt)

                self.clouds = [c for c in self.clouds if c.rect.right > 0]

                if self.check_collision():
                    self.game_lost = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                
            self.win.fill((255, 255, 255))

            for cloud in self.clouds:
                self.win.blit(cloud.image, cloud.rect)

            self.win.blit(self.ground1, self.ground1_rect)
            self.win.blit(self.ground2, self.ground2_rect)
            self.win.blit(self.dino.image, self.dino.rect)
            
            if self.bird is not None:
                self.win.blit(self.bird.image, self.bird.rect)

            if self.tree is not None:
                self.win.blit(self.tree.image, self.tree.rect)

            self.draw_score()

            if self.game_lost:
                self.draw_game_over()

            # if self.show_hitbox:
            #     pg.draw.rect(self.win, (255, 0, 0), self.dino.hitbox, 2)

            #     if self.tree is not None:
            #         pg.draw.rect(self.win, (0, 255, 0), self.tree.hitbox, 2)

            #     if self.bird is not None:
            #         pg.draw.rect(self.win, (0, 0, 255), self.bird.hitbox, 2)
    
            pg.display.update()
            self.clock.tick(60)

game = Game()