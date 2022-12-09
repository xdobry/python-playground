from random import randint
import pygame
import numpy
import math
from demo_base import Demo, Scene
from tmatrix_util import TransMatrix2D

# use generic programing like processing to paint
# fractal structures

class Processing:
    def __init__(self,screen):
        self.screen = screen
        self.color = pygame.color.Color(255,255,255)
        self.m = TransMatrix2D()
    def line(self,fromPos,toPos):
        pygame.draw.line(self.screen,self.color,self.transPoint(fromPos),self.transPoint(toPos))
    def transPoint(self,pos):
        point = numpy.array([pos[0],pos[1],1],dtype=float)
        pointTrans = self.m.m @ point
        return int(pointTrans[0]),int(pointTrans[1])

class ProcessingScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
        font = pygame.font.SysFont("mono",42,italic=True)
        self.p = Processing(demo.screen)
        self.pi2 = math.radians(360)
        self.p.m.trans((demo.screenRect.centerx,demo.screenRect.centery))
    def update(self,demo,counter):
        self.counter = counter
    def drawRad(self):
        for i in range(0,360,10):
            self.p.m.push()
            self.p.m.rotateGrad(i+self.counter/2%10)
            self.p.line((0,0),(100,100))
            self.p.m.pop()
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.drawRad()
        self.p.m.push()
        self.p.color = pygame.color.Color(255,0,0)
        self.p.m.trans((demo.screenRect.centerx/2,demo.screenRect.centery/2))
        self.p.m.scale((0.5,0.5))
        self.drawRad()
        self.p.m.pop()
        self.p.color = pygame.color.Color(255,255,255)

if __name__ == "__main__":
    demo = Demo("Proecessing Like Demo",(800,600),40)
    ProcessingScene(demo)
    demo.start()
    pygame.quit()  