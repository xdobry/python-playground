import pygame
import math
from demo_base import Demo, Scene


class DotsPlaneScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for px in range(0,int(demo.screenRect.width/self.dotGap)):
            for py in range(0,int(demo.screenRect.height/self.dotGap)):
                dx = px*self.dotGap+self.dotGap/2
                dy = py*self.dotGap+self.dotGap/2
                r = (demo.screenRect.centerx-dx)**2+(demo.screenRect.centery-dy)**2
                dx = dx+math.sin(r+self.counter/20)*4
                dy = dy+math.sin(r+self.counter/20)*3
                pygame.draw.rect(demo.screen,self.colorWite,pygame.rect.Rect(dx,dy,1,1))


if __name__ == "__main__":
    demo = Demo("Dots",(800,600),40)
    DotsPlaneScene(demo)
    demo.start()
    pygame.quit()