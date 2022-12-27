import pygame
import math
import random
from demo_base import Demo, Scene

class FreqMod2():
    def __init__(self,size,a,b):
        self.size = size
        self.a = a
        self.oa = 0.2
        self.ob = 0.1
        self.b = b
        self.pi2 = math.radians(360)
    def noise(self,x,y):
        xs = x * self.pi2
        ys = y * self.pi2
        #print(f"xs {xs}")
        return (math.sin(xs+math.sin(ys*self.a)+self.oa)+math.sin(ys+math.sin(xs*self.b)+self.ob)+2)/4
    def smoth(self):
        None
    def reinit(self):
        self.a = random.randint(1,5)
        self.b = random.randint(1,5)
        self.oa = random.random()*self.pi2
        self.ob = random.random()*self.pi2

class NoiseScene(Scene):
    title = "frequncy modulation"
    description = "frequency modulation on RGB to produce tile color patterns"
    backgroundColor = pygame.Color(0,0,0)
    colR = pygame.Color(255,0,0)
    colG = pygame.Color(0,255,0)
    colB = pygame.Color(0,0,255)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.tileSize= 100
        self.noiseR = FreqMod2(self.tileSize,2,3)
        self.noiseG = FreqMod2(self.tileSize,3,2)
        self.noiseB = FreqMod2(self.tileSize,4,2)
        self.tile = pygame.Surface((self.tileSize,self.tileSize))
        self.updateTile()
    def updateTile(self):
        max = -200
        min = 200
        for x in range(0,self.tileSize):
            for y in range(0,self.tileSize):
                r = int(self.noiseR.noise(x/self.tileSize,y/self.tileSize)*255)
                g = int(self.noiseG.noise(x/self.tileSize,y/self.tileSize)*255)
                b = int(self.noiseB.noise(x/self.tileSize,y/self.tileSize)*255)
                #print(f"{c}")
                max = r if r>max else max
                min = r if r<min else min
                self.tile.set_at((x,y),pygame.Color(r,g,b))
        #print(f"min {min} max {max}")
    def update(self,demo,counter):
        self.counter=counter
        if (self.counter%500==0):
            self.noiseR.reinit()
            self.noiseG.reinit()
            self.noiseB.reinit()
            self.updateTile()
    def draw(self,demo):
        for tx in range(0,math.ceil(demo.screenRect.width/self.tileSize)):
            for ty in range(0,math.ceil(demo.screenRect.width/self.tileSize)):
                demo.screen.blit(self.tile,(tx*self.tileSize,ty*self.tileSize))
        for x in range(0,demo.screenRect.width):
            r = int(self.noiseR.noise(x/demo.screenRect.width,((self.counter/2)%100)/100)*(demo.screenRect.height))
            g = int(self.noiseG.noise(x/demo.screenRect.width,((self.counter/2)%100)/100)*(demo.screenRect.height))
            b = int(self.noiseB.noise(x/demo.screenRect.width,((self.counter/2)%100)/100)*(demo.screenRect.height))
            pygame.draw.circle(demo.screen,self.colR,(x,r),2)
            pygame.draw.circle(demo.screen,self.colG,(x,g),2)
            pygame.draw.circle(demo.screen,self.colB,(x,b),2)
        None

if __name__ == "__main__":
    demo = Demo("frequency modulation noise 2 dim",(800,600),40)
    NoiseScene(demo)
    demo.start()
    pygame.quit()  