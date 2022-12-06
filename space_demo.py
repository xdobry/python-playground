import pygame
import random
from demo_base import Demo, Scene

class Star:
    move = pygame.math.Vector3(0,0,1)
    colors = []
    for c in range(0,256):
        colors.append(pygame.Color(c,c,c))
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
                surface.set_at((x2,y2),self.colors[r])
    def update(self):
        self.pos.z -=2
        if self.pos.z<0: 
            self.pos.z = 800
            self.pos.y = random.randint(-800,800)
            self.pos.x = random.randint(-800,800)

class StarScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.stars = []
        for i in range(0,1000):
            self.stars.append(Star())
    def update(self,demo,counter):
        for star in self.stars:
            star.update()
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        for star in self.stars:
            star.draw(demo.screen)

if __name__ == "__main__":
    demo = Demo("Space",(800,600),20)
    StarScene(demo)
    demo.start()
    pygame.quit()