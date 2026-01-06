import pygame as pg
import random

class Bird(pg.sprite.Sprite):
    def __init__(self, speed, *groups):
        super().__init__(*groups)
        self.bl = [pg.image.load('assets/bird1.png').convert_alpha(),
                   pg.image.load('assets/bird2.png').convert_alpha()]
        self.image = self.bl[0]
        self.mask = pg.mask.from_surface(self.image)
        self.fly_height = random.choice([170, 200, 220])
        self.rect = self.image.get_rect(midleft = (620, self.fly_height))
        self.image_switch = 1
        self.anime_counter = 0
        self.speed = speed

    def update(self, dt):
        if self.anime_counter == 8:
            self.image = self.bl[self.image_switch]
            if self.image_switch == 0:
                self.image_switch = 1
            else:
                self.image_switch = 0
            self.anime_counter = 0
        self.anime_counter += 1

        self.rect.x -= self.speed*dt

        if self.rect.right < 0:
            self.deletemyself()

    def setmovespeed(self, move_speed):
        self.speed = move_speed

    def deletemyself(self):
        self.kill()