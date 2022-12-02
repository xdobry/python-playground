import pygame
import random
import math

screenRect = pygame.Rect((0,0,800,800))
matrixColor = pygame.Color(3, 160, 98)
backgroundColor = pygame.Color((0,0,0))



def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Matrix Falling Code')
    running = True
    clock = pygame.time.Clock()
    counter = 0
    circles = []
    for c,blend in zip([pygame.Color(2,0,1,0),pygame.Color(1,2,0,0),pygame.Color(0,1,2,0),pygame.Color(1,2,1,0),pygame.Color(2,2,2,0)],[pygame.BLEND_RGBA_ADD,pygame.BLEND_RGBA_ADD,pygame.BLEND_RGBA_ADD, pygame.BLEND_RGBA_SUB,pygame.BLEND_RGBA_SUB]):
        r = random.randint(120,250)
        s = pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,c,(r,r),r)
        orbitRList = []
        orbitSpeedList = []
        for ci in range(0,random.randint(1,5)):
            orbitRList.append(random.randint(50,100))
            orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
        circles.append({
            "s": s,
            "orbitRList": orbitRList,
            "orbitSpeedList": orbitSpeedList,
            "blendMode": blend,
        })
    
   
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        #screen.fill(backgroundColor)
        for c in circles:
            posX = screenRect.centerx-c["s"].get_width()/2
            posY = screenRect.centery-c["s"].get_width()/2
            for orbitR, orbitSpeed in zip(c["orbitRList"],c["orbitSpeedList"]):
                posX += orbitR*math.cos(counter/orbitSpeed)
                posY += orbitR*math.sin(counter/orbitSpeed)
                screen.blit(c["s"],(posX,posY),special_flags=c["blendMode"])
        pygame.display.flip()
        clock.tick(40)
        counter+=1

if __name__ == "__main__":
    main()
    pygame.quit()