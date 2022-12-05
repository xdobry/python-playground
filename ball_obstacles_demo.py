import pygame
import math
from ball import Ball

screenRect = pygame.Rect((0,0,400,400))
objectColor = pygame.Color(255, 255, 255)

Ball.screenRect = screenRect

stop = False

class RectObstacle:
    def __init__(self,xy,size):
        self.rect = pygame.Rect(xy,size)
    def draw(self,surface):
        global objectColor
        pygame.draw.rect(surface,objectColor,self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Balls Obstacles Demo')
    running = True
    backgroundSurface = pygame.Surface(screenRect.size)
    obstacles = []
    obstacles.append(RectObstacle((100,100),(100,50)))
    obstacles.append(RectObstacle((200,300),(80,70)))
    for obstacle in obstacles:
        obstacle.draw(backgroundSurface)

    group = pygame.sprite.Group()
    balls = []
    balls.append(Ball((320,224),(-3,2),pygame.Color(0,255,0)))
    balls.append(Ball((150,50),(3,4),pygame.Color(255,0,0)))
    balls.append(Ball((150,250),(-3,2),pygame.Color(0,0,255)))
    for ball in balls:
        group.add(ball)
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
   
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.blit(backgroundSurface,(0,0))
        #mousePos = pygame.mouse.get_pos()
        #balls[0].pos.x = mousePos[0]
        #balls[0].pos.y = mousePos[1]
        if not stop:
            group.update()
            for idx, ball in enumerate(balls):
                for obstacle in obstacles:
                    ball.tryObstacle(obstacle)
                for ball2 in balls[idx+1:]:
                    ball.tryCollision(ball2)
        group.draw(screen)
        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()