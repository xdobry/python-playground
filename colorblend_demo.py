import pygame
import random
import math
from demo_base import Demo, Scene


class BlendScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.circles = []
        for c,blend in zip([pygame.Color(2,0,1,0),pygame.Color(1,2,0,0),pygame.Color(0,1,2,0),pygame.Color(1,2,1,0),pygame.Color(2,2,2,0)],[pygame.BLEND_RGBA_ADD,pygame.BLEND_RGBA_ADD,pygame.BLEND_RGBA_ADD, pygame.BLEND_RGBA_SUB,pygame.BLEND_RGBA_SUB]):
            r = random.randint(120,250)
            s = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
            pygame.draw.circle(s,c,(r,r),r)
            orbitRList = []
            orbitSpeedList = []
            for ci in range(0,random.randint(1,5)):
                orbitRList.append(random.randint(50,100))
                orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
            self.circles.append({
                "s": s,
                "orbitRList": orbitRList,
                "orbitSpeedList": orbitSpeedList,
                "blendMode": blend,
            })
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        for c in self.circles:
            posX = demo.screenRect.centerx-c["s"].get_width()/2
            posY = demo.screenRect.centery-c["s"].get_width()/2
            for orbitR, orbitSpeed in zip(c["orbitRList"],c["orbitSpeedList"]):
                posX += orbitR*math.cos(self.counter/orbitSpeed)
                posY += orbitR*math.sin(self.counter/orbitSpeed)
            demo.screen.blit(c["s"],(posX,posY),special_flags=c["blendMode"])

if __name__ == "__main__":
    demo = Demo("Blend",(800,800),40)
    BlendScene(demo)
    demo.start()
    pygame.quit()