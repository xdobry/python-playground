import pygame
import math
import random
from demo_base import Demo, Scene

message = "WELCOME TO PYGAME REIMPLEMENTATION OF SOME RETRO DEMOS FROM 80s and 90s ! SHOW SOME SIMPLE EFFECTS +++ HAVE A FUN +++"

class AScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        pygame.font.init()
        font = pygame.font.SysFont("mono", 24,bold=True)
        self.msgImages = [font.render(c, True, self.colorWite) for c in list(message)]
        self.pressSpaceMsg = font.render("PRESS SPACE FOR NEXT DEMO",True, pygame.color.Color(120,80,0))
        self.backGround = pygame.surface.Surface((demo.screenRect.width,100))
        vStart = pygame.Vector3((255,20,0))
        vEnd = pygame.Vector3((10,0,255))
        for i in range(0,self.backGround.get_height()):
            cV = vStart.lerp(vEnd,i/self.backGround.get_height())
            pygame.draw.line(self.backGround,pygame.Color(int(cV.x),int(cV.y),int(cV.z)),(0,i),(self.backGround.get_width(),i))
        self.msgY = int(demo.screenRect.height*0.8)
        self.points = []
        for p in range(0,3):
            orbitRList = []
            orbitSpeedList = []
            for ci in range(0,3):
                orbitRList.append(random.randint(10,100))
                orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
            self.points.append((orbitRList,orbitSpeedList))
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        demo.screen.blit(self.backGround,(0,self.msgY-self.backGround.get_height()/2+12))
        self.pressSpaceMsg.set_alpha(int(abs(math.sin(self.counter/50))*255))
        demo.screen.blit(self.pressSpaceMsg,(demo.screenRect.centerx-self.pressSpaceMsg.get_width()/2,demo.screenRect.height-self.pressSpaceMsg.get_height()-10))
        posX = self.counter % (demo.screenRect.width+len(message)*14)
        for idx,img in enumerate(self.msgImages):
            demo.screen.blit(img,((demo.screenRect.width-posX)+idx*14,self.msgY+math.sin((posX+idx*3)/20)*20))
        pointPos = []
        for point in self.points:
            posX = demo.screenRect.centerx
            posY = demo.screenRect.centery
            for orbitR, orbitSpeed in zip(point[0],point[1]):
                posX += orbitR*math.cos(self.counter/orbitSpeed)
                posY += orbitR*math.sin(self.counter/orbitSpeed)
            pointPos.append((posX,posY))
        pygame.draw.line(demo.screen,self.colorWite,pointPos[0],pointPos[1])
        pygame.draw.line(demo.screen,self.colorWite,pointPos[1],pointPos[2])
        pygame.draw.line(demo.screen,self.colorWite,pointPos[0],pointPos[2])

if __name__ == "__main__":
    demo = Demo("Title",(800,600),40)
    AScene(demo)
    demo.start()
    pygame.quit()