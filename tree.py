import pygame as pg 
import random

class Tree(pg.sprite.Sprite):
    def __init__(self, speed, *groups):
        super().__init__(*groups)
        
        self.images = [pg.image.load(f'assets/trees/t{i}.png').convert_alpha() for i in range(1, 6)]

        self.image = random.choice(self.images)
        
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect(midbottom = (620, 250))

        self.speed = speed

    def update(self, dt):
        self.rect.x -= self.speed*dt

        if self.rect.right<0:
            self.deletemyself()

    def setmovespeed(self, move_speed):
        self.speed = move_speed

    def deletemyself(self):
        self.kill()