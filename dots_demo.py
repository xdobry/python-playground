import pygame
import math
from demo_base import Demo, Scene

class DotsScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.dotsCount = 20
        self.orbitRList = [250,50,125]
        self.orbitSpeedList = [50,30,-30]
        self.colors = [pygame.color.Color((255-(5*x),255-(5*x),255-(5*x))) for x in range(0,self.dotsCount)]
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for p in range(0,len(self.orbitRList)):
            for pointNum in range(0,self.dotsCount):
                posX = demo.screenRect.centerx
                posY = demo.screenRect.centery
                for orbitR, orbitSpeed in zip(self.orbitRList,self.orbitSpeedList):
                    posX += orbitR*math.cos((self.counter+(pointNum*13))/orbitSpeed)*(p+1)/len(self.orbitRList)
                    posY += orbitR*math.sin((self.counter+(pointNum*13))/orbitSpeed)*(p+1)/len(self.orbitRList)
                pygame.draw.rect(demo.screen,self.colors[self.dotsCount-pointNum-1],pygame.rect.Rect(posX,posY,4,4))

if __name__ == "__main__":
    demo = Demo("Dots",(800,600),40)
    DotsScene(demo)
    demo.start()
    pygame.quit()