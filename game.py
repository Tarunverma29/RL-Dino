import pygame as pg
pg.init()
from pygame.locals import *
import sys

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


# echo "# RL-Dino" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/Tarunverma29/RL-Dino.git
# git push -u origin main