import pygame
import random
from demo_base import Demo, Scene

message = "** PARTICELS FALL **"
objectColor = pygame.Color(255, 255, 255)

class Particle:
    acc = pygame.math.Vector2(0,0.1)
    colors = []
    for c in range(0,256):
        colors.append(pygame.Color(c,c,c))
    def __init__(self,x,y):
        self.pos = pygame.math.Vector2(x,y)
        self.move = pygame.math.Vector2(0,0)
        self.fixed = 10
        self.live = 255
    def draw(self,surface):
        global colors
        if self.live>0:
            surface.set_at((int(self.pos.x),int(self.pos.y)),self.colors[self.live])
    def update(self,surface):
        if self.live>0:
            if self.fixed==10:
                pos = (int(self.pos.x),int(self.pos.y))
                colorDown = surface.get_at((pos[0],pos[1]+1))
                if colorDown.r==0:
                    colorDown = surface.get_at((pos[0],pos[1]+2))
                    if colorDown.r==0:
                        self.fixed = 9
            if self.fixed==0:
                self.move += self.acc
                self.move.x = self.move.x + random.random()/10-0.05
                self.move.y = self.move.y + random.random()/10-0.05
                self.pos += self.move
                self.live -= 1
            else:
                self.fixed -= 1

def createParticles(surface,screenRect):
    particles = []
    size = surface.get_size()
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            col = surface.get_at((x,y))
            if col.r>0:
                particles.append(Particle((screenRect.width-size[0])/2+x,y+10))
    return particles

class TextFallScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        font = pygame.font.SysFont("mono",42)
        textSurface = font.render(message, True, objectColor)
        textSurface2 = pygame.Surface((textSurface.get_width(),textSurface.get_height()))
        textSurface2.blit(textSurface,(0,0))
        self.particles = createParticles(textSurface2,demo.screenRect)
    def update(self,demo,counter):
        if counter>50:
            for particle in self.particles:
                particle.update(demo.screen)
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for particle in self.particles:
            particle.draw(demo.screen)
    def isRunning(self,counter):
        return not any([p.live==0 for p in self.particles])

if __name__ == "__main__":
    demo = Demo("Space",(600,600),20)
    TextFallScene(demo)
    demo.start()
    pygame.quit()