import pygame as pg 

class Dino(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.run_images=[pg.image.load('assets/dino1.png').convert_alpha(),
                         pg.image.load('assets/dino2.png').convert_alpha()]
        
        self.crouch_images=[pg.image.load('assets/dino_crouch1.png').convert_alpha(),
                            pg.image.load('assets/dino_crouch2.png').convert_alpha()]
        
        self.image=self.run_images[0]
        self.resetdino()
        self.gravity = 900
        self.jumpspeed = 350

    def resetdino(self):
        self.rect=self.image.get_rect(bottomleft=(75, 254))

        self.image_index=0
        self.anim_counter=0
        self.anim_speed=4
        self.velocity_y=0
        self.is_on_ground = True
        self.crouch=False

    def update(self, dt):
        keys=pg.key.get_pressed()
        if keys[pg.K_DOWN]:
            self.crouch=True
        else: self.crouch=False

        if self.is_on_ground:
            self.anim_counter+=1

            if self.anim_counter>=self.anim_speed:
                self.anim_counter=0

                self.image_index = 1 - self.image_index
            
            if self.crouch:
                self.image=self.crouch_images[self.image_index]
                self.rect = self.image.get_rect(bottomleft=(75,251))
            else:
                self.image = self.run_images[self.image_index]
                self.rect=self.image.get_rect(bottomleft=(75, 254))

        else:
            self.velocity_y += self.gravity*dt 
            self.rect.y += self.velocity_y*dt

            if self.rect.bottom >= 254:
                self.rect.bottom = 254
                self.velocity_y=0
                self.is_on_ground = True

            self.image = self.run_images[self.image_index]


    def jumpdino(self):
        if self.is_on_ground:
            self.velocity_y = -self.jumpspeed
            self.is_on_ground = False