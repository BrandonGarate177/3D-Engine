from object_3d import *
import pygame as pg


class SoftwareRender: 
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT= 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2 
        self.FPS = 144 
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()


    # Translation matrix 

    # [[1, 0, 0, 0],
    #  [0, 1, 0, 0],
    #  [0, 0, 1, 0],
    #  [tx, ty, tz, 1]]

    # THIS IS SUPER DUPPA CRAZY MAD IMPORTANT TYPE SHIIIIIIT

    # Scaling matrix 

    # [[Sx, 0, 0, 0],
    #  [0, Sy, 0, 0],
    #  [0, 0, Sz, 0],
    #  [0, 0, 0, 1]]

    # this up here is deadass the most important part of the program, its the math type shit. I am gonna put it in a seperate file to make the program easier to code
    # im feeling big brain type shiiit 

    def create_objects(self):
        self.object = object(self)

    def draw(self):
        self.screen.fill((47, 79, 79))

    def run(self): 
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
    # this checks if the application is closed

if __name__ == '__main__': 
    app = SoftwareRender()
    app.run()            

