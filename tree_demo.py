from random import randint
import pygame
import math
from demo_base import Demo, Scene
from processing_utils import Processing
from color_utils import genColors
from tmatrix_util import map

# use generic programing like processing to paint
# fractal structures

class TreeScene(Scene):
    title = "growing fractal tree"
    description = "lets grow the tree using recursion and matrix transformations"
    backgroundColor = pygame.Color((61,120,215))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    speedFactor = 0.3
    colors = genColors(pygame.Color(40,100,3),pygame.Color(35,10,0),20)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.p = Processing(demo.screen)
        self.pi = math.radians(180)
        self.p.m.trans((demo.screenRect.centerx,demo.screenRect.height))
        self.counterDiff = 0
        self.addAngle = 0
        self.maxCounter = 0.8*demo.screenRect.centery/self.speedFactor
    def update(self,demo,counter):
        if self.counterDiff==0:
            self.counterDiff = counter
            self.counter = 0
        if self.counter<self.maxCounter:
            self.counter = counter - self.counterDiff
        else:
            self.addAngle = math.sin((counter - self.counterDiff - self.maxCounter)/80)/6
            #self.counterDiff = counter
    def reset(self,demo):
        self.counterDiff = 0
    def drawBranch(self,branchLength,deep):
        #print(f"{branchLength}")
        colIndex = int(map(branchLength,5,400,0,len(self.colors)-1))
        self.p.color = self.colors[colIndex]
        self.p.line((0,0),(0,-branchLength),colIndex+1)
        if branchLength>3 and deep<10:
            self.p.m.trans((0,-branchLength))
            self.p.m.push()
            self.p.m.rotate(self.pi/4+self.addAngle)
            self.drawBranch(branchLength*0.55,deep+1)
            self.p.m.pop()
            self.p.m.push()
            self.p.m.rotate(-self.pi/4+self.addAngle)
            self.drawBranch(branchLength*0.55,deep+1)
            self.p.m.pop()
        else:
            if branchLength>1:
                self.p.circle((0,-branchLength),3)
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.p.m.push()
        self.p.m.rotate(self.addAngle)
        self.drawBranch(self.counter*self.speedFactor,0)
        self.p.m.pop()

if __name__ == "__main__":
    demo = Demo("Growing Fractal Tree",(800,600),40)
    TreeScene(demo)
    demo.start()
    pygame.quit()  