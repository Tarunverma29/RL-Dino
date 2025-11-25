import pygame as pg 
import random

class Tree(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.images = [pg.image.load(f'assets/trees/tree{i}.png').convert_alpha() for i in range(1,6)]

        self.image = random.choice(self.images)

        self.rect = self.image.get_rect(midbottom=(620, 254))

        self.speed = 250

    def update(self, dt):
        self.rect.x -= self.speed * dt