from random import randint
import pygame
import numpy
import math
from demo_base import Demo, Scene
from tmatrix_util import TransMatrix2D

# see https://www.alanzucconi.com/2016/02/10/tranfsormation-matrix/
# for informations aber 2D transformation matix
# use numpy for fast matrix computation



def genPlane(colx,coly,d):
    def genFun(x,y):
        m = x%colx*d
        m[:,1] = numpy.floor(x[:,0]/coly)*d
        return m
    return numpy.fromfunction(genFun,(colx*coly,2),dtype=float)

class DotsPlaneScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
        sizex = 20
        sizey = 20
        d = 5
        self.dots = numpy.column_stack((genPlane(sizex,sizey,d),numpy.ones(sizex*sizey)))
        self.m = TransMatrix2D()
        self.m.trans((demo.screenRect.centerx-45,demo.screenRect.centery-45))
        #self.m.rotateGrad(-45)
        #self.m.scale((4,4))
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.m.push()
        self.m.trans((45,45))
        self.m.rotate(self.counter/30)
        sx = math.sin(self.counter/50)*4
        sy = math.sin(self.counter/50+0.3)*4
        self.m.scale((sx,sy))
        self.m.trans((-45,-45))
        # we use matrix dot multiplication to compute all positions in one run
        for dot in self.dots.dot(self.m.m.T):
            demo.screen.set_at((int(dot[0]), int(dot[1])), self.colorWite)
        self.m.pop()
        

if __name__ == "__main__":
    demo = Demo("Dots 2D Trans",(800,600),40)
    DotsPlaneScene(demo)
    demo.start()
    pygame.quit()   