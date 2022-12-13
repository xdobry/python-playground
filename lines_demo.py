from distutils import core
from color_utils import genColors
import pygame
import random
from demo_base import Demo, Scene

class MemoryPoint:
    def __init__(self,pos,v,memSize):
        self.pos = pygame.math.Vector2(pos)
        self.moveV = pygame.math.Vector2(v)
        self.memory = []
        self.counter = 0
        self.memSize = memSize
    def update(self):
        self.pos = self.pos + self.moveV
        if self.pos.x<=0 and self.moveV.x<0:
            self.moveV.x = -self.moveV.x
        elif self.pos.x>=MemoryPoint.screenRect.width and self.moveV.x>0:
            self.moveV.x = -self.moveV.x
        if self.pos.y<=0 and self.moveV.y<0:
            self.moveV.y = -self.moveV.y
        elif self.pos.y>=MemoryPoint.screenRect.height and self.moveV.y>0:
            self.moveV.y = -self.moveV.y
        self.counter += 1
        if self.counter%2==0:
            self.memory.append(self.pos.copy())
            if len(self.memory)>self.memSize:
                self.memory.pop(0)

def genRandomXY(range,add=0, minus=False):
    x = random.randint(0,range[0])+add
    y = random.randint(0,range[1])+add
    if minus:
        x = -x if random.random()>0.5 else x
        y = -y if random.random()>0.5 else y
    return (x,y)

class Line:
    def __init__(self,startColor,endColor,steps,velRange):
        self.colors = genColors(startColor,endColor,steps)
        self.p1 = MemoryPoint(genRandomXY(Line.screenRect.size),genRandomXY((velRange[1]-velRange[0],velRange[1]-velRange[0]),velRange[0],True),steps)
        self.p2 = MemoryPoint(genRandomXY(Line.screenRect.size),genRandomXY((velRange[1]-velRange[0],velRange[1]-velRange[0]),velRange[0],True),steps)
    def update(self):
        self.p1.update()
        self.p2.update()
    def draw(self,screen):
        for color, p1, p2 in zip(self.colors,self.p1.memory,self.p2.memory):
            pygame.draw.line(screen,color,(int(p1.x),int(p1.y)),(int(p2.x),int(p2.y)))

class LinesScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    title = "moving lines"
    description = "very simple but effective"
    def __init__(self,demo):
        Scene.__init__(self,demo)
        Line.screenRect = demo.screenRect
        MemoryPoint.screenRect = demo.screenRect
        linesCount = 8
        self.lines = [Line(pygame.Color(10, 10, 10),pygame.Color(0, 50, 250),linesCount,(4,12)),Line(pygame.Color(10, 10, 10),pygame.Color(0, 255, 20),linesCount,(4,12)),Line(pygame.Color(10, 10, 10),pygame.Color(255, 0, 20),linesCount,(4,12))]
    def update(self,demo,counter):
        for line in self.lines:
            line.update()
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for line in self.lines:
            line.draw(demo.screen)

if __name__ == "__main__":
    demo = Demo("Water",(800,600),20)
    LinesScene(demo)
    demo.start()
    pygame.quit()