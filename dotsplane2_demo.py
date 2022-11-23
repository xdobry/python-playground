import pygame
import math
import random

screenRect = pygame.Rect((0,0,800,600))
objectColor = pygame.Color(255, 255, 255)
emptyColor = pygame.Color(0,0,0,0)
colorWite = pygame.Color(255,255,255)

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screenRect.size)
    pygame.display.set_caption('dots demo')
    running = True
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    counter = 0
    dotGap = 10
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        counter += 1
        screen.fill(backgroundColor)

        for px in range(0,int(screenRect.width/dotGap)):
            for py in range(0,int(screenRect.height/dotGap)):
                dx = px*dotGap+dotGap/2
                dy = py*dotGap+dotGap/2
                r = (screenRect.centerx-dx)**2+(screenRect.centery-dy)**2
                dx = dx+math.sin(r+counter/20)*4
                dy = dy+math.sin(r+counter/20)*3
                pygame.draw.rect(screen,colorWite,pygame.rect.Rect(dx,dy,1,1))

        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()