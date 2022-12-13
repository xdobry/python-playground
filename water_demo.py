from distutils import core
from color_utils import genColors
import pygame
import math
from demo_base import Demo, Scene

def genSurfaces(colors,size):
    surfaces = []
    for color in colors:
        surface = pygame.Surface((size,size),pygame.SRCALPHA)
        maxr = (size/2*math.sqrt(2))**2
        for x in range(0,size):
            for y in range(0,size):
                r = (x-size/2)**2+(y-size/2)**2+40
                alpha = 210-int(r/maxr*255)
                alpha = 0 if alpha<0 else alpha
                surface.set_at((x,y),pygame.Color(color.r,color.g,color.b,alpha))
        surfaces.append(surface)
    return surfaces

class WaterScene(Scene):
    title = "color waves demo"
    description = "use sin rect movement and apha drawing to create waves"
    backgroundColor = pygame.Color((0,0,0))
    objectColor = pygame.Color(255, 255, 255)
    objectFixColor = pygame.Color(255, 0, 0)
    surfaces = genSurfaces(genColors(pygame.Color(0, 50, 100),pygame.Color(10, 20, 255),8),64)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.anim = 0.0
    def update(self,demo,counter):
        self.anim = self.anim + 0.01
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        xspan = 8
        yspan = 4
        maxr = math.sqrt(xspan**2+yspan**2)
        for x in range(0,demo.screenRect.width,16):
            xpos = (x + (math.sin(-self.anim + x * 0.01) * xspan))
            for y in range(0,demo.screenRect.height,16):
                ypos = (y + (math.sin(self.anim + y * 0.01) * yspan))
                r = math.sqrt((x-xpos)**2+(y-ypos)**2)
                colorIndex = int(r*(len(self.surfaces)/maxr))
                #print(f"{colorIndex} {r}")
                surface = self.surfaces[colorIndex]
                demo.screen.blit(surface,(int(xpos),int(ypos)))
                #demo.screen.blit(surface,(x,y),special_flags=pygame.BLEND_RGB_ADD)
                #demo.screen.blit(surface,(x,y),sp)

if __name__ == "__main__":
    demo = Demo("Water",(600,600),2)
    WaterScene(demo)
    demo.start()
    pygame.quit()