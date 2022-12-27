from random import randint
import pygame
import numpy
import math
from demo_base import Demo, Scene
from tmatrix_util import TransMatrix3D

# see https://www.alanzucconi.com/2016/02/10/tranfsormation-matrix/
# for informations aber 2D transformation matix
# use numpy for fast matrix computation



def genCube(d):
    ca = []
    for x in range(-1,2,2):
        for y in range(-1,2,2):
            for z in range(-1,2,2):
                ca.append([x*d,y*d,z*d])
    return numpy.array(ca,dtype=float)

class DotsPlaneScene(Scene):
    title = "3d cube using numpy matrix"
    description = "use numpy and 3d transformation matrix"
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
        d = 1
        self.dots = numpy.column_stack((genCube(d),numpy.ones(8)))
        self.m = TransMatrix3D()
        #self.m.scale((0.5,0.5,0.5))
        self.m.trans((0,0,-10))
        self.p = TransMatrix3D()
        self.p.perspective(math.radians(45),demo.screenRect.width/demo.screenRect.height,1,200)
        #self.m.rotateGrad(-45)
        #self.m.scale((4,4))
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.m.push()
        self.m.trans((0,0,abs(math.sin(self.counter/30)*4)))
        self.m.rotateY(self.counter/30)
        self.m.rotateX(self.counter/60)
        # we use matrix dot multiplication to compute all positions in one run

        tm = self.dots @ self.m.m.T @ self.p.m
        #tm[:, 2] = numpy.true_divide(tm[:, 2], tm[:, 3])
        tm[:, 0] = numpy.true_divide(tm[:, 0], tm[:, 3])
        tm[:, 1] = numpy.true_divide(tm[:, 1], tm[:, 3])
        width = demo.screenRect.width
        height = demo.screenRect.height

        tm[:, 0] = tm[:, 0] * width / 2 + width / 2
        tm[:, 1] = -tm[:, 1] * height / 2 + height / 2
        tm = tm.astype(int)
        for lineConn in [(0,1),(0,2),(0,4),(7,5),(7,6),(7,3),(1,5),(1,3),(3,2),(4,6),(4,5),(2,6)]:
            start = tm[lineConn[0]]
            end = tm[lineConn[1]]
            pygame.draw.line(demo.screen,self.colorWite,start[:2],end[:2])
        self.m.pop()
        

if __name__ == "__main__":
    demo = Demo("Dots 2D Trans",(800,600),40)
    DotsPlaneScene(demo)
    demo.start()
    pygame.quit() 