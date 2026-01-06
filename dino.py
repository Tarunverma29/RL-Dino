import pygame as pg

class Dino(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.drl = [pg.image.load('assets/dino1.png').convert_alpha(),
                    pg.image.load('assets/dino2.png').convert_alpha()]
        self.dcl = [pg.image.load('assets/dino_crouch1.png').convert_alpha(),
                    pg.image.load('assets/dino_crouch2.png').convert_alpha()]
        
        self.image = self.drl[0]
        self.mask = pg.mask.from_surface(self.image)
    
        self.resetdino()
        self.gravity = 10
        self.jumpspeed = 270

    def update(self, dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.crouch = True
        else:
            self.crouch = False

        if self.on_ground:
            if self.animation_counter == 4:
                if self.crouch:
                    self.image = self.dcl[self.switch]
                    self.rect = pg.Rect(100, 220, 55, 10)
                else:
                    self.image = self.drl[self.switch]
                    self.rect = pg.Rect(100, 203, 43, 51)
                self.mask = pg.mask.from_surface(self.image)
                if self.switch == 1:
                    self.switch = 0
                else:
                    self.switch = 1
                self.animation_counter = 0
            self.animation_counter += 1
        else:
            self.y_velocity += self.gravity*dt
            self.rect.y += self.y_velocity
            if self.rect.y >= 203:
                self.on_ground = True
                self.rect.y = 203

    def jump(self, dt):
        if self.on_ground:
            self.y_velocity =- self.jumpspeed*dt
            self.on_ground = False

    def resetdino(self):
        self.rect = pg.Rect(100, 203, 43, 51)
        self.animation_counter = 0
        self.switch = 1
        self.crouch = False
        self.on_ground = True
        self.y_velocity = 0
        