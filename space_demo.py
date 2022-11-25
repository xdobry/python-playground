import pygame
import random
import math

screenRect = pygame.Rect((0,0,800,600))
objectColor = pygame.Color(255, 255, 255)

message = "** PARTICELS FALL **"

colors = []
for c in range(0,256):
    colors.append(pygame.Color(c,c,c))

class Star:
    move = pygame.math.Vector3(0,0,1)
    def __init__(self):
        self.pos = pygame.math.Vector3(random.randint(-800,800),random.randint(-800,800),random.randint(50,800))
    def draw(self,surface):
        global colors
        if self.pos.z>100:
            # https://ogldev.org/www/tutorial12/tutorial12.html
            x2 = int(self.pos.x/self.pos.z*150+400)
            y2 = int(self.pos.y/self.pos.z*150+400)
            if x2>0 and x2<800 and y2>0 and y2<800:
                r = 255-int(self.pos.z/800*255)
                surface.set_at((x2,y2),colors[r])
    def update(self):
        self.pos.z -=2
        if self.pos.z<0: 
            self.pos.z = 800
            self.pos.y = random.randint(-800,800)
            self.pos.x = random.randint(-800,800)



def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Balls Obstacles Demo')
    running = True
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    counter = 0
    stars = []
    for i in range(0,1000):
        stars.append(Star())
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(backgroundColor)
        for star in stars:
            star.update()
            star.draw(screen)
        pygame.display.flip()
        clock.tick(20)
        counter+=1

if __name__ == "__main__":
    main()
    pygame.quit()