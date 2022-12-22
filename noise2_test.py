from random import randint
import pygame
import math
import random
from perlin_noise import PerlinNoise
from demo_base import Demo, Scene

def smothstep(x):
    if x==0:
        return 0
    elif x==1.0:
        return 1
    else:
        return x * x * (3 - 2 * x)

class Noise2():
    def __init__(self,octaves=5,seed=7):
        random.seed(seed)
        self.octaves = octaves
        self.reinit()
    def reinit(self):
        self.numbers = []
        for y in range(self.octaves-1):
            row = [random.random() for x in range(self.octaves-1)] 
            row.append(row[0])
            self.numbers.append(row)
        self.numbers.append(self.numbers[0])
    def smoth(self):
        for x in range(1,self.octaves-1):
            for y in range(1,self.octaves-1):
                self.numbers[x][y] = (0.25*self.numbers[x][y] 
                    + 0.125*self.numbers[x][y-1] + 0.125*self.numbers[x][y+1] + 0.125*self.numbers[x-1][y] + 0.125*self.numbers[x+1][y]
                    + 0.0625*self.numbers[x-1][y-1] + 0.0625*self.numbers[x+1][y-1] + 0.0625*self.numbers[x-1][y+1] + 0.0625*self.numbers[x+1][y+1]
                )
        x = 0
        for y in range(1,self.octaves-1):
            self.numbers[x][y] = (0.25*self.numbers[x][y] 
                    + 0.125*self.numbers[x][y-1] + 0.125*self.numbers[x][y+1] + 0.125*self.numbers[self.octaves-2][y] + 0.125*self.numbers[x+1][y]
                    + 0.0625*self.numbers[self.octaves-2][y-1] + 0.0625*self.numbers[x+1][y-1] + 0.0625*self.numbers[self.octaves-2][y+1] + 0.0625*self.numbers[x+1][y+1]
            )
            self.numbers[self.octaves-1][y] = self.numbers[x][y]
        y = 0
        for x in range(1,self.octaves-1):
            self.numbers[x][y] = (0.25*self.numbers[x][y] 
                 + 0.125*self.numbers[x][self.octaves-2] + 0.125*self.numbers[x][y+1] + 0.125*self.numbers[x-1][y] + 0.125*self.numbers[x+1][y]
                + 0.0625*self.numbers[x-1][self.octaves-2] + 0.0625*self.numbers[x+1][self.octaves-2] + 0.0625*self.numbers[x-1][y+1] + 0.0625*self.numbers[x+1][y+1]
            )
            self.numbers[x][self.octaves-1] = self.numbers[x][y]
        self.numbers[0][0] = (0.25*self.numbers[x][y] 
                    + 0.125*self.numbers[x][self.octaves-2] + 0.125*self.numbers[x][y+1] + 0.125*self.numbers[self.octaves-2][y] + 0.125*self.numbers[x+1][y]
                    + 0.0625*self.numbers[x-1][self.octaves-2] + 0.0625*self.numbers[x+1][self.octaves-2] + 0.0625*self.numbers[x-1][y+1] + 0.0625*self.numbers[x+1][y+1]
                )
        self.numbers[0][self.octaves-1] = self.numbers[0][0]
        self.numbers[self.octaves-1][self.octaves-1] = self.numbers[0][0]
        self.numbers[self.octaves-1][0] = self.numbers[0][0]
 
    def noise(self,x,y):
        [fx,rx] = math.modf(x*(self.octaves-1))
        [fy,ry] = math.modf(y*(self.octaves-1))
        indexX = int(rx)
        indexY = int(ry)
        a = self.numbers[indexX][indexY]
        b = self.numbers[indexX+1][indexY]
        c = self.numbers[indexX+1][indexY+1]
        d = self.numbers[indexX][indexY+1]
        x1 = a+smothstep(fx)*(b-a)
        x2 = d+smothstep(fx)*(c-d)
        #print(f"x1 {x1} x2 {x2} a {a} b {b} c {c} d {d}")
        return x1+smothstep(fy)*(x2-x1)

class NoiseScene(Scene):
    title = "own noise"
    description = "2 dimension noise smothstep. it is circular so it can be used in tiles"
    backgroundColor = pygame.Color(0,0,0)
    col = pygame.Color(255,0,0)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.noise = Noise2(10,2.1)
        self.tileSize= 100
        self.tile = pygame.Surface((self.tileSize,self.tileSize))
        self.updateTile()
    def updateTile(self):
        max = -200
        min = 200
        for x in range(0,self.tileSize):
            for y in range(0,self.tileSize):
                c = int(self.noise.noise(x/self.tileSize,y/self.tileSize)*225)
                #print(f"{c}")
                max = c if c>max else max
                min = c if c<min else min
                self.tile.set_at((x,y),pygame.Color(c,c,c))
        #print(f"min {min} max {max}")
    def update(self,demo,counter):
        self.counter=counter
        if self.counter%200==0:
            if (self.counter%1000==0):
                self.noise.reinit()
            else:
                self.noise.smoth()
            self.updateTile()
    def draw(self,demo):
        for tx in range(0,math.ceil(demo.screenRect.width/self.tileSize)):
            for ty in range(0,math.ceil(demo.screenRect.width/self.tileSize)):
                demo.screen.blit(self.tile,(tx*self.tileSize,ty*self.tileSize))
        for x in range(0,demo.screenRect.width):
            c = int(self.noise.noise(x/demo.screenRect.width,((self.counter/2)%100)/100)*(demo.screenRect.height))
            pygame.draw.circle(demo.screen,self.col,(x,c),2)
        None

if __name__ == "__main__":
    demo = Demo("Self programmed 2 dimmension noise using smothstep",(800,600),40)
    NoiseScene(demo)
    demo.start()
    pygame.quit()  