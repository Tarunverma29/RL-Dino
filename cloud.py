import pygame as pg 
import random

class Cloud:
    def __init__(self):
        self.image = pg.image.load('assets/cloud.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 600 + random.randint(0, 100)
        self.rect.y = random.randint(20, 80)

        self.speed = random.randint(30, 50)

    def update(self, dt):
        self.rect.x -= self.speed*dt