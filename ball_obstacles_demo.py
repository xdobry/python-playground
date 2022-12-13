import pygame
from ball import Ball
from demo_base import Demo, Scene

class BallScene(Scene):
    backgroundColor = pygame.Color((0,0,0))
    colorWite = pygame.Color(255,255,255)
    title = "Balls with obstacles"
    def __init__(self,demo):
        Scene.__init__(self,demo)
        Ball.screenRect = demo.screenRect
        self.group = pygame.sprite.Group()
        self.balls = [
            Ball((320,224),(-3,2),pygame.Color(255,255,0)),
            Ball((150,50),(3,4),pygame.Color(255,0,0)),
            Ball((40,130),(-3,4),pygame.Color(0,255,0)),
            Ball((350,350),(3,-3),pygame.Color(0,0,255)),
            Ball((250,250),(1,-2),pygame.Color(100,0,205)),
        ]
        for ball in self.balls:
            self.group.add(ball)
        self.backgroundSurface = pygame.Surface(demo.screenRect.size)
        self.obstacles = [
            RectObstacle((100,100),(100,50)),
            RectObstacle((200,300),(80,70)),
            RectObstacle((600,60),(10,170)),
            RectObstacle((300,500),(300,20))
        ]
        for obstacle in self.obstacles:
            obstacle.draw(self.backgroundSurface,self.colorWite)
    def update(self,demo,counter):
        self.group.update()
        for idx, ball in enumerate(self.balls):
            for obstacle in self.obstacles:
                ball.tryObstacle(obstacle)
            for ball2 in self.balls[idx+1:]:
                ball.tryCollision(ball2)
    def draw(self,demo):
        demo.screen.blit(self.backgroundSurface,(0,0))
        self.group.draw(demo.screen)

class RectObstacle:
    def __init__(self,xy,size):
        self.rect = pygame.Rect(xy,size)
    def draw(self,surface,objectColor):
        pygame.draw.rect(surface,objectColor,self.rect)

if __name__ == "__main__":
    demo = Demo("Balls Obstacles",(800,600),40)
    BallScene(demo)
    demo.start()
    pygame.quit()