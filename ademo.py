import pygame
import math
import random

screenRect = pygame.Rect((0,0,800,600))
objectColor = pygame.Color(255, 255, 255)
emptyColor = pygame.Color(0,0,0,0)
colorWite = pygame.Color(255,255,255)

message = "WELCOME! PROS NEVER GO TIRED ** HOP UND EX ** LAMERS RULE IT "

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("mono", 24,bold=True)
    screen = pygame.display.set_mode(screenRect.size)
    pygame.display.set_caption('retro demo')
    running = True
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    msgImages = [font.render(c, True, colorWite) for c in list(message)]
    backGround = pygame.surface.Surface((screenRect.width,100))
    vStart = pygame.Vector3((255,20,0))
    vEnd = pygame.Vector3((10,0,255))
    for i in range(0,backGround.get_height()):
        cV = vStart.lerp(vEnd,i/backGround.get_height())
        pygame.draw.line(backGround,pygame.Color(int(cV.x),int(cV.y),int(cV.z)),(0,i),(backGround.get_width(),i))

    counter = 0
    msgY = int(screenRect.height*0.8)
    points = []
    for p in range(0,3):
        orbitRList = []
        orbitSpeedList = []
        for ci in range(0,3):
            orbitRList.append(random.randint(10,100))
            orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
        points.append((orbitRList,orbitSpeedList))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        counter += 1
        screen.fill(backgroundColor)
        screen.blit(backGround,(0,msgY-backGround.get_height()/2+12))
        posX = counter % (screenRect.width+len(message)*14)
        for idx,img in enumerate(msgImages):
            screen.blit(img,((screenRect.width-posX)+idx*14,msgY+math.sin((posX+idx*3)/20)*20))

        pointPos = []
        for point in points:
            posX = screenRect.centerx
            posY = screenRect.centery
            for orbitR, orbitSpeed in zip(point[0],point[1]):
                posX += orbitR*math.cos(counter/orbitSpeed)
                posY += orbitR*math.sin(counter/orbitSpeed)
            pointPos.append((posX,posY))
        pygame.draw.line(screen,colorWite,pointPos[0],pointPos[1])
        pygame.draw.line(screen,colorWite,pointPos[1],pointPos[2])
        pygame.draw.line(screen,colorWite,pointPos[0],pointPos[2])


        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()