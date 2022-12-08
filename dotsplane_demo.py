import pygame
from demo_base import Demo, Scene

class DotsPlaneScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    dotGap = 10
    def __init__(self,demo):
        Scene.__init__(self,demo)
    def update(self,demo,counter):
        self.counter = counter
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        mousePos = pygame.mouse.get_pos()
        mouseBut = pygame.mouse.get_pressed()[0]
        mouseInside = demo.screenRect.collidepoint(mousePos)

        for px in range(0,int(demo.screenRect.width/self.dotGap)):
            for py in range(0,int(demo.screenRect.height/self.dotGap)):
                dx = px*self.dotGap+self.dotGap/2
                dy = py*self.dotGap+self.dotGap/2
                if mouseInside:
                    dv = pygame.math.Vector2(dx,dy)
                    mv = pygame.math.Vector2(mousePos)
                    r = dv.distance_to(mv)
                    rv = mv - dv
                    if (rv.x!=0 or rv.y!=0) and r<200:
                        rv.scale_to_length(self.dotGap*2*(200-r)/200)
                        if mouseBut:
                            dv = dv + rv
                        else:
                            dv = dv - rv
                        dx = dv.x
                        dy = dv.y
                    pygame.draw.rect(demo.screen,self.colorWite,pygame.rect.Rect(dx,dy,1,1))

if __name__ == "__main__":
    demo = Demo("Dots",(800,600),40)
    DotsPlaneScene(demo)
    demo.start()
    pygame.quit()