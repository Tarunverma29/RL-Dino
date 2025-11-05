import pygame as pg
from pygame.locals import *
import sys

pg.init()
class Game:
    def __init__(self):
        self.win = pg.display.set_mode((600,300))
        self.gameloop()

    def gameloop(self):
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

game = Game()



# dfgoijhrdf