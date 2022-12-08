import pygame
from demo_base import Demo, Scene
from ball import Ball


class BallScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    def __init__(self,demo):
        Scene.__init__(self,demo)
        Ball.screenRect = demo.screenRect
        self.group = pygame.sprite.Group()
        self.balls = [
            Ball((320,224),(-3,2),pygame.Color(255,255,255)),
            Ball((150,50),(3,4),pygame.Color(255,0,0)),
            Ball((40,130),(-3,4),pygame.Color(0,255,0)),
            Ball((350,350),(3,-3),pygame.Color(0,0,255)),
            Ball((250,250),(1,-2),pygame.Color(100,0,205)),
        ]
        for ball in self.balls:
            self.group.add(ball)
    def update(self,demo,counter):
        self.group.update()
        for idx, ball in enumerate(self.balls):
            for ball2 in self.balls[idx+1:]:
                ball.tryCollision(ball2)
    def draw(self,demo):
        demo.screen.fill(self.backgroundColor)
        self.group.draw(demo.screen)

if __name__ == "__main__":
    demo = Demo("Balls",(800,600),40)
    BallScene(demo)
    demo.start()
    pygame.quit()