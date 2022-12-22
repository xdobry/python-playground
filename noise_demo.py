from random import randint
import pygame
import math
from perlin_noise import PerlinNoise
from demo_base import Demo, Scene

# use generic programing like processing to paint
# fractal structures

class NoiseScene(Scene):
    title = "perlin noise"
    description = "lets grow the tree using recursion and matrix transformations"
    backgroundColor = pygame.Color((61,120,215))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.noise = PerlinNoise(octaves=10, seed=1)
        max = 0
        min = 255
        for x in range(0,100):
            for y in range(0,100):
                c = abs(int(self.noise([x/100,y/100])*128+128))
                max = c if c>max else max
                min = c if c<min else min
                demo.screen.set_at((x,y),pygame.Color(c,c,c))
        print(f"min {min} max {max}")
    def draw(self,demo):
        None


if __name__ == "__main__":
    demo = Demo("Growing Fractal Tree",(800,600),40)
    NoiseScene(demo)
    demo.start()
    pygame.quit()  