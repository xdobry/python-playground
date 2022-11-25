import pygame
import random

screenRect = pygame.Rect((0,0,600,600))
objectColor = pygame.Color(255, 255, 255)

message = "** PARTICELS FALL **"

colors = []
for c in range(0,256):
    colors.append(pygame.Color(c,c,c))

class Particle:
    acc = pygame.math.Vector2(0,0.1)
    def __init__(self,x,y):
        self.pos = pygame.math.Vector2(x,y)
        self.move = pygame.math.Vector2(0,0)
        self.fixed = 10
        self.live = 255
    def draw(self,surface):
        global colors
        if self.live>0:
            surface.set_at((int(self.pos.x),int(self.pos.y)),colors[self.live])
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

def createParticles(surface):
    particles = []
    size = surface.get_size()
    for x in range(0,size[0]):
        for y in range(0,size[1]):
            col = surface.get_at((x,y))
            if col.r>0:
                particles.append(Particle((screenRect.width-size[0])/2+x,y+10))
    return particles

def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Balls Obstacles Demo')
    running = True
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    counter = 0
    font = pygame.font.SysFont("mono",42)
    textSurface = font.render(message, True, objectColor)
    textSurface2 = pygame.Surface((textSurface.get_width(),textSurface.get_height()))
    textSurface2.blit(textSurface,(0,0))
    particles = createParticles(textSurface2)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        if counter>50:
            for particle in particles:
                particle.update(screen)
        screen.fill(backgroundColor)
        for particle in particles:
            particle.draw(screen)
        pygame.display.flip()
        clock.tick(20)
        counter+=1
        if any([p.live==0 for p in particles]):
            running = False

if __name__ == "__main__":
    main()
    pygame.quit()