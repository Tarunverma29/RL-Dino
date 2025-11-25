import pygame as pg 
import random

class Bird(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.images=[pg.image.load('assets/bird1.png').convert_alpha(),
                     pg.image.load('assets/bird2.png').convert_alpha()]
        
        self.image=self.images[0]

        self.fly_height = random.choice([170, 200, 220])

        self.rect=self.image.get_rect(midleft=(620, self.fly_height))

        self.speed = 300
        self.image_index = 0
        self.anim_counter = 0

    def update(self, dt):
        self.anim_counter += 1
        if self.anim_counter >= 8:
            self.anim_counter = 0
            self.image_index = 1 - self.image_index
            self.image = self.images[self.image_index]

        self.rect.x -= self.speed * dt

        if self.rect.right < 0:
            self.kill()        
