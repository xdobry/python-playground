from random import randint
import pygame
import numpy
import math
from demo_base import Demo, Scene
from tmatrix_util import TransMatrix2D

def text2dots(text,font):
    textSurface = font.render(text, True, pygame.color.Color(255,255,255))
    textSurface2 = pygame.Surface((textSurface.get_width(),textSurface.get_height()))
    textSurface2.blit(textSurface,(0,0))
    particles = []
    size = textSurface2.get_size()
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            col = textSurface2.get_at((x,y))
            if col.r>0:
                particles.append([x,y])
    return numpy.column_stack((numpy.array(particles),numpy.ones(len(particles)))), textSurface2.get_size()

def map(x,sourceFrom,sourceTo,targetFrom,targetTo):
    return targetFrom+(x-sourceFrom)*(targetTo-targetFrom)/(sourceTo-sourceFrom)

class DotsPlaneScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
        font = pygame.font.SysFont("mono",42,italic=True)
        self.dots, self.size = text2dots("AMIGA",font)
        self.m = TransMatrix2D()
        self.m.trans((demo.screenRect.centerx-self.size[0]/2,demo.screenRect.centery-self.size[1]/2))
        #self.m.rotateGrad(-45)
        #self.m.scale((4,4))
        self.counterDiff = 0
        self.pi2 = math.radians(360)
    def update(self,demo,counter):
        if self.counterDiff==0:
            self.counterDiff = counter
        self.counter = counter-self.counterDiff
    def drawDots(self,demo):
        # we use matrix dot multiplication to compute all positions in one run
        for dot in self.dots.dot(self.m.m.T):
            demo.screen.set_at((int(dot[0]), int(dot[1])), self.colorWite)
    def rotateBump(self,demo,start):
        c = self.counter - start
        self.m.push()
        self.m.trans((self.size[0]/2,self.size[1]/2))
        self.m.rotate(c/50)
        sx = math.cos(c/80)*4
        sy = math.cos(c/80+0.3)*4
        self.m.scale((sx,sy))
        self.m.trans((-self.size[0]/2,-self.size[1]/2))
        self.drawDots(demo)
        self.m.pop()
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        if self.counter<200:
            self.drawDots(demo)
        elif self.counter<400:
            self.m.push()
            s = map(self.counter,200,400,1,4)
            self.m.trans((self.size[0]/2,self.size[1]/2))
            self.m.scale((s,s))
            self.m.trans((-self.size[0]/2,-self.size[1]/2))
            self.drawDots(demo)
            self.m.pop()
        elif self.counter<600:
            self.m.push()
            s = map(self.counter,400,600,0,self.pi2)
            self.m.trans((self.size[0]/2,self.size[1]/2))
            self.m.scale((4,4))
            self.m.share((math.sin(s)*2,0))
            self.m.trans((-self.size[0]/2,-self.size[1]/2))
            self.drawDots(demo)
            self.m.pop()
        elif self.counter<800:
            self.m.push()
            s = map(self.counter,600,800,4,12)
            self.m.trans((self.size[0]/2,self.size[1]/2))
            self.m.scale((4,s))
            self.m.trans((-self.size[0]/2,-self.size[1]/2))
            self.drawDots(demo)
            self.m.pop()
        elif self.counter<1000:
            self.m.push()
            s = map(self.counter,800,1000,0,self.pi2*4)
            d = map(self.counter,800,1000,1,8)
            self.m.trans((self.size[0]/2,self.size[1]/2))
            self.m.scale((4,4+abs(math.cos(s)*(8-d))))
            self.m.trans((-self.size[0]/2,-self.size[1]/2))
            self.drawDots(demo)
            self.m.pop()
        else:
            self.rotateBump(demo,1000)
        

if __name__ == "__main__":
    demo = Demo("Dots 2D Trans",(800,600),40)
    DotsPlaneScene(demo)
    demo.start()
    pygame.quit()   