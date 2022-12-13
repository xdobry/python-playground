import pygame
import random
from demo_base import Demo, Scene

class Circle:
    def __init__(self,max,pos,r=10):
        self.b = 50
        self.max = max
        self.reset()
        self.r = r
        self.pos = pos
    def reset(self):
        self.r = 10
        self.speed = 2
        self.color = pygame.color.Color(random.randint(1,5),random.randint(1,5),random.randint(1,5),255)
    def updateDraw(self,surface):
        pygame.draw.circle(surface,self.color,self.pos,self.r,width=self.b)
        self.r = self.r + self.speed
        if (self.r>self.max):
            self.reset()

class ColorTunelScene(Scene):
    title = "color tunel"
    description = "use blend modes to mode circles in diffent colors"
    backgroundColor = pygame.Color((0,0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.addSurface = pygame.Surface(demo.screenRect.size,pygame.SRCALPHA)
        self.subSurface = pygame.Surface(demo.screenRect.size,pygame.SRCALPHA)
        self.circlesAdd = [Circle(demo.screenRect.width/2*1.45,demo.screenRect.center,80+i*80) for i in range(0,7)]
        self.circlesSub = [Circle(demo.screenRect.width/2*1.45,demo.screenRect.center,20+i*80) for i in range(0,7)]
    def update(self,demo,counter):
        self.addSurface.fill(self.backgroundColor)
        self.subSurface.fill(self.backgroundColor)
        for c in self.circlesAdd:
            c.updateDraw(self.addSurface)
        for c in self.circlesSub:
            c.updateDraw(self.subSurface)
    def draw(self,demo):
        demo.screen.blit(self.addSurface,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
        demo.screen.blit(self.subSurface,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

if __name__ == "__main__":
    demo = Demo("Space",(800,800),40)
    ColorTunelScene(demo)
    demo.start()
    pygame.quit()