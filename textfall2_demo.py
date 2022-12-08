import pygame
import random
from demo_base import Demo, Scene

objectColor = pygame.Color(255, 255, 255)

message = "** PARTICELS FALL **"

colors = []
for c in range(0,256):
    colors.append(pygame.Color(c,c,c))

class Particle:
    acc = pygame.math.Vector2(0,0.1)
    def __init__(self,x,y,dx,dy):
        self.pos = pygame.math.Vector2(x,y)
        self.move = pygame.math.Vector2(0,0)
        self.dx = dx
        self.dy = dy
        self.fixed = True
        self.live = 255
    def draw(self,surface):
        global colors
        if self.live>0:
            surface.set_at((int(self.pos.x),int(self.pos.y)),colors[self.live])
    def update(self,maxy):
        if self.live>0:
            if self.fixed:
                pos = (int(self.pos.x)-self.dx,int(self.pos.y)-self.dy)
                if pos[1]>=maxy[pos[0]]:
                    self.fixed = False
            if not self.fixed:
                self.move += self.acc
                self.move.x = self.move.x + random.random()/10-0.05
                self.move.y = self.move.y + random.random()/10-0.05
                self.pos += self.move
                self.live -= 1

def createParticles(surface,screenRect):
    particles = []
    size = surface.get_size()
    maxy = [0 for i in range(0,size[0])]
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            col = surface.get_at((x,y))
            if col.r>0:
                particles.append(Particle((screenRect.width-size[0])/2+x,y+10,int((screenRect.width-size[0])/2),10))
                maxy[x] = y
    return particles, maxy

class TextFallScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        font = pygame.font.SysFont("mono",42)
        textSurface = font.render(message, True, objectColor)
        self.textSurface2 = pygame.Surface((textSurface.get_width(),textSurface.get_height()))
        self.textSurface2.blit(textSurface,(0,0))
        self.reset(demo)
    def update(self,demo,counter):
         if counter>50:
            if counter%5==0:
                for i in range(0,len(self.maxy)):
                    if self.maxy[i]>0:
                        self.maxy[i] -= 1
            for particle in self.particles:
                particle.update(self.maxy)
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for particle in self.particles:
            particle.draw(demo.screen)
    def reset(self,demo):
        self.particles, self.maxy = createParticles(self.textSurface2,demo.screenRect)
    def isRunning(self,counter):
        return not any([p.live==0 for p in self.particles])

if __name__ == "__main__":
    demo = Demo("Space",(600,600),20)
    TextFallScene(demo)
    demo.start()
    pygame.quit()