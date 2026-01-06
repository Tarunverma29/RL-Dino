import pygame as pg
import sys 
import time 
from dino import Dino
from bird import Bird
from tree import Tree
from cloud import Cloud
import random


pg.init()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 300
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Dino Run')

        self.g1 = pg.image.load('assets/ground.png').convert_alpha()
        self.g1_rect = self.g1.get_rect(center = (300, 250))
        self.g2 = pg.image.load('assets/ground.png').convert_alpha()
        self.g2_rect = self.g2.get_rect(center = (900, 250))

        self.speed = 250
        self.lost = False
        self.clock = pg.time.Clock()
        self.enemy_create_counter = 0
        self.enemy_create_time = 80
        self.enemy_group = pg.sprite.Group()
        self.score = 0
        self.last_speed_score = 0

        self.clouds = []
        self.last_cloud_time = 0
        self.next_cloud_time = random.randint(2000, 4000)

        self.font = pg.font.Font('assets/font.ttf', 20)

        self.label_score = self.font.render('Score : 0', True, (0, 0, 0))
        self.label_score_rect = self.label_score.get_rect(center = (80, 20))

        self.restart_font = pg.font.Font('assets/font.ttf', 30)
        self.lbl_restart = self.restart_font.render('Restart Game', True, (0, 0, 0))
        self.restart_rect = self.lbl_restart.get_rect(center = (300, 150))

        self.dead_sound = pg.mixer.Sound('assets/sfx/dead.mp3')
        self.jump_sound = pg.mixer.Sound('assets/sfx/jump.mp3')
        self.points_sound = pg.mixer.Sound('assets/sfx/points.mp3')

        self.dino = Dino()
        self.gameloop()

    def checkcollisions(self):
        if pg.sprite.spritecollide(self.dino, self.enemy_group, True , pg.sprite.collide_mask):
            self.stopgame()

    def stopgame(self):
        self.lost = True
        self.dead_sound.play()

    def create_cloud(self):
        cloud = Cloud()
        self.clouds.append(cloud)
        self.last_cloud_time = pg.time.get_ticks()
        self.next_cloud_time = random.randint(2000, 4000)
    
    def restart(self):
        self.lost = False
        self.score = 0
        self.enemy_create_counter = 0
        self.speed = 250
        self.label_score = self.font.render('Score : 0', True, (0, 0, 0))
        self.dino.resetdino()
        self.clouds = []
        self.last_cloud_time = 0
        self.next_cloud_time = random.randint(2000, 4000)
        for enemy in self.enemy_group:
            enemy.deletemyself()

    def gameloop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    if not self.lost:
                        self.dino.jump(dt)
                        self.jump_sound.play()
                    else:
                        self.restart() 
            
            self.window.fill((255, 255, 255))
            if not self.lost:
                self.g1_rect.x -= self.speed*dt
                self.g2_rect.x -= self.speed*dt

                if self.g1_rect.right < 0:
                    self.g1_rect.x = self.g2_rect.right
                if self.g2_rect.right < 0:
                    self.g2_rect.x = self.g1_rect.right

                if self.enemy_create_counter == self.enemy_create_time:
                    if random.randint(0,1) == 0:
                        self.enemy_group.add(Bird(speed=self.speed))
                    else:
                        self.enemy_group.add(Tree(speed=self.speed))
                    self.enemy_create_counter = 0
                self.enemy_create_counter += 1

                now = pg.time.get_ticks()
                if now - self.last_cloud_time >= self.next_cloud_time:
                    self.create_cloud()

                for cloud in self.clouds:
                    cloud.update(dt)

                self.clouds = [c for c in self.clouds if c.rect.right > 0] 

                self.score += 0.1
                self.label_score = self.font.render(f'Score : {int(self.score)}', True, (0, 0, 0))
                self.dino.update(dt)
                self.enemy_group.update(dt)
                self.checkcollisions()
            else:
                self.window.blit(self.lbl_restart, self.restart_rect)


            if int(self.score) != 0 and int(self.score)%50 == 0 and int(self.score) != self.last_speed_score:
                self.speed += 10
                self.last_speed_score = int(self.score)
                for enemy in self.enemy_group:
                    enemy.setmovespeed(self.speed)

            if int(self.score)%100==0 and int(self.score) != 0:
                self.points_sound.play()

            self.window.blit(self.dino.image, self.dino.rect)
            for enemy in self.enemy_group:
                self.window.blit(enemy.image, enemy.rect)

            for cloud in self.clouds:
                self.window.blit(cloud.image, cloud.rect)
                
            self.window.blit(self.g1, self.g1_rect)    
            self.window.blit(self.g2, self.g2_rect)
            self.window.blit(self.label_score, self.label_score_rect)

            pg.display.update()
            self.clock.tick(60)

game = Game()