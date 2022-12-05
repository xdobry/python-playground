import pygame
from ball import Ball

screenRect = pygame.Rect((0,0,400,400))
objectColor = pygame.Color(255, 255, 255)

Ball.screenRect = screenRect


def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Balls Demo')
    running = True
    group = pygame.sprite.Group()
    balls = []
    balls.append(Ball((320,224),(-3,2),objectColor))
    balls.append(Ball((150,50),(3,4),pygame.Color(255,0,0)))
    balls.append(Ball((40,130),(-3,4),pygame.Color(0,255,0)))
    balls.append(Ball((350,350),(3,-3),pygame.Color(0,0,255)))
    balls.append(Ball((250,250),(1,-2),pygame.Color(100,0,205)))
    for ball in balls:
        group.add(ball)
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
   
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(backgroundColor)
        group.update()
        for idx, ball in enumerate(balls):
            for ball2 in balls[idx+1:]:
                ball.tryCollision(ball2)
        group.draw(screen)
        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()