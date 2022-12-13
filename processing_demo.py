from random import randint
import pygame
import numpy
import math
from demo_base import Demo, Scene
from tmatrix_util import TransMatrix2D
from processing_utils import Processing

# use generic programing like processing to paint
# fractal structures

class ProcessingScene(Scene):
    title = "generic fractal draws"
    description = "use processing language approach to generate repetative matrix translated fractal structures"
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
        font = pygame.font.SysFont("mono",42,italic=True)
        self.p = Processing(demo.screen)
        self.pi2 = math.radians(360)
        self.p.m.trans((demo.screenRect.centerx,demo.screenRect.centery))
        self.counterDiff = 0
    def update(self,demo,counter):
        if self.counterDiff==0:
            self.counterDiff = counter
        self.counter = counter - self.counterDiff
    def reset(self,demo):
        self.counterDiff = 0
    def drawRad(self):
        for i in range(0,360,10):
            self.p.m.push()
            gradAdd = (self.counter-50)/2%10 if self.counter>50 else 0
            self.p.m.rotateGrad(i+gradAdd)
            self.p.line((0,0),(100,100))
            self.p.m.pop()
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.p.m.push()
        if self.counter>300:
            self.p.m.scale((1+0.5*abs(math.sin((self.counter-300)/100)),(1+0.5*abs(math.sin((self.counter-300)/100)))))
        self.drawRad()
        if self.counter>200:
            for d,col in zip ([[1,1],[1,-1],[-1,-1],[-1,1]],[
                pygame.color.Color(255,0,0),
                pygame.color.Color(0,255,0),
                pygame.color.Color(0,0,255),
                pygame.color.Color(255,255,0)
            ]):
                self.p.m.push()
                self.p.color = col
                self.p.m.trans((demo.screenRect.centerx/2*d[0],demo.screenRect.centery/2*d[1]))
                self.p.m.scale((0.5,0.5))
                self.drawRad()
                self.p.m.pop()
        self.p.color = pygame.color.Color(255,255,255)
        self.p.m.pop()

if __name__ == "__main__":
    demo = Demo("Proecessing Like Demo",(800,600),40)
    ProcessingScene(demo)
    demo.start()
    pygame.quit()  