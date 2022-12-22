from random import randint
import pygame
import math
import random
from perlin_noise import PerlinNoise
from demo_base import Demo, Scene

# use generic programing like processing to paint
# fractal structures

def smothstep(x):
    if x==0:
        return 0
    elif x==1.0:
        return 1
    else:
        return x * x * (3 - 2 * x)

class Noise():
    def __init__(self,octaves=5,seed=7):
        random.seed(seed)
        self.octaves = 5
        self.numbers = [random.random()*2-1 for x in range(octaves-1)]
        self.numbers.append(self.numbers[0])
    def noise(self,x):
        [f,r] = math.modf(x*(self.octaves-1))
        index = int(r)
        a = self.numbers[index]
        b = self.numbers[index+1]
        return a+smothstep(f)*(b-a)

class NoiseScene(Scene):
    title = "perlin noise"
    description = "lets grow the tree using recursion and matrix transformations"
    backgroundColor = pygame.Color(0,0,0)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.noise = PerlinNoise(octaves=5,seed=13)
        myNoise = Noise()
        col = pygame.Color(255,255,255)
        colRed = pygame.Color(255,0,0)
        for x in range(0,demo.screenRect.width):
            c = demo.screenRect.centery+int(self.noise(x/demo.screenRect.width)*demo.screenRect.centery)
            demo.screen.set_at((x,c),col)
            c = demo.screenRect.centery+int(myNoise.noise(x/demo.screenRect.width)*demo.screenRect.centery)
            demo.screen.set_at((x,c),colRed)
    def draw(self,demo):
        #demo.screen.fill(self.backgroundColor)
        None


if __name__ == "__main__":
    demo = Demo("Growing Fractal Tree",(800,600),40)
    NoiseScene(demo)
    demo.start()
    pygame.quit()  