import pygame
import math
import random
from demo_base import Demo, Scene

class CirclesScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    emptyColor = pygame.Color(0,0,0,0)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.circles = []
        for i in range(0,40):
            circleR = random.randint(20,100)
            circlePos = pygame.Rect((random.randint(0,demo.screenRect.width),random.randint(0,demo.screenRect.height)),(circleR,circleR))
            circleColor = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(100,255))
            pulseR = random.randint(10,int(circleR/2))
            surfaceWidth = circleR+pulseR*2
            surface = pygame.Surface((surfaceWidth,surfaceWidth),pygame.SRCALPHA)
            orbitRList = []
            orbitSpeedList = []
            for ci in range(0,random.randint(1,5)):
                orbitRList.append(random.randint(10,100))
                orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
            self.circles.append({
                "rect": circlePos,
                "color": circleColor,
                "pulseSpeed": random.randint(5,50),
                "pulseR": pulseR,
                "orbitR": orbitRList,
                "orbitSpeed": orbitSpeedList,
                "surface": surface
            })
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for circle in self.circles:
            posX = circle["rect"].centerx
            posY = circle["rect"].centery
            for orbitR, orbitSpeed in zip(circle["orbitR"],circle["orbitSpeed"]):
                posX += orbitR*math.cos(self.counter/orbitSpeed)
                posY += orbitR*math.sin(self.counter/orbitSpeed)
            csurface = circle["surface"]
            csurface.fill(self.emptyColor)
            csurfaceWidht = csurface.get_width()
            pygame.draw.circle(csurface,
                circle["color"], 
                (csurfaceWidht/2,csurfaceWidht/2),
                circle["rect"].width/2+int(math.sin(self.counter/circle["pulseSpeed"])*circle["pulseR"])
            )
            demo.screen.blit(csurface,(posX,posY))  

if __name__ == "__main__":
    demo = Demo("Circles",(800,600),40)
    CirclesScene(demo)
    demo.start()
    pygame.quit()