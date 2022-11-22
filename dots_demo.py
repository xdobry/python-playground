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
    dotsCount = 20
    counter = 0
    orbitRList = [250,50,125]
    orbitSpeedList = [50,30,-30]
    colors = [pygame.color.Color((255-(5*x),255-(5*x),255-(5*x))) for x in range(0,dotsCount)]
    #for ci in range(0,3):
    #    orbitRList.append(random.randint(50,200))
    #    orbitSpeedList.append(random.randint(20,100)*(1 if random.randint(0,1) == 0 else -1))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        counter += 1
        screen.fill(backgroundColor)

        for p in range(0,len(orbitRList)):
            for pointNum in range(0,dotsCount):
                posX = screenRect.centerx
                posY = screenRect.centery
                for orbitR, orbitSpeed in zip(orbitRList,orbitSpeedList):
                    posX += orbitR*math.cos((counter+(pointNum*13))/orbitSpeed)*(p+1)/len(orbitRList)
                    posY += orbitR*math.sin((counter+(pointNum*13))/orbitSpeed)*(p+1)/len(orbitRList)
                pygame.draw.rect(screen,colors[dotsCount-pointNum-1],pygame.rect.Rect(posX,posY,4,4))

        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()