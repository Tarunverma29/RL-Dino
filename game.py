import pygame as pg
from pygame.locals import *
import sys
import time

pg.init()
class Game:
    def __init__(self):
        self.win = pg.display.set_mode((600,300))
        self.clock = pg.time.Clock()

        self.ground1 = pg.image.load("assets/ground.png").convert_alpha()
        self.ground1_rect = self.ground1.get_rect(center=(300, 250))

        self.ground2 = pg.image.load("assets/ground.png")
        self.ground2_rect = self.ground2.get_rect(center=(900, 250))

        self.game_lost = False
        self.move_speed = 250
        self.gameloop()

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

                
            if not self.game_lost:
                self.ground1_rect.x-=self.move_speed*dt
                self.ground2_rect.x-=self.move_speed*dt

                if self.ground1_rect.right<0:
                    self.ground1_rect.x = self.ground2_rect.right
                if self.ground2_rect.right<0:
                    self.ground2_rect.x = self.ground1_rect.right

            self.clock.tick(60)
            pg.display.update()

            self.win.fill((255, 255, 255))
            self.win.blit(self.ground1, self.ground1_rect)
            self.win.blit(self.ground2, self.ground2_rect)
            pg.display.update()

game = Game()