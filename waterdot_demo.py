import pygame
import math
from demo_base import Demo, Scene

class WaterDotScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    objectColor = pygame.Color(255, 255, 255)
    objectFixColor = pygame.Color(255, 0, 0)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.anim = 0.0
    def update(self,demo,counter):
        self.anim = self.anim + 0.02
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for x in range(0,demo.screenRect.width,16):
            xpos = (x + (math.sin(self.anim + x * 0.01) * 8))
            for y in range(0,demo.screenRect.height,16):
                ypos = (y + (math.sin(self.anim + y * 0.01) * 8))
                demo.screen.set_at((int(xpos), int(ypos)), self.objectColor)
                #demo.screen.set_at((x,y), self.objectFixColor)

if __name__ == "__main__":
    demo = Demo("Space",(600,600),20)
    WaterDotScene(demo)
    demo.start()
    pygame.quit()