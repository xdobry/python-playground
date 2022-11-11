import pygame
import math
import random

screenRect = pygame.Rect((0,0,800,600))
objectColor = pygame.Color(255, 255, 255)
emptyColor = pygame.Color(0,0,0,0)
    

def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size)
    pygame.display.set_caption('circles')
    running = True
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    circles = []
    for i in range(0,40):
        circleR = random.randint(20,100)
        circlePos = pygame.Rect((random.randint(0,screenRect.width),random.randint(0,screenRect.height)),(circleR,circleR))
        circleColor = pygame.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(100,255))
        pulseR = random.randint(10,int(circleR/2))
        surfaceWidth = circleR+pulseR*2
        surface = pygame.Surface((surfaceWidth,surfaceWidth),pygame.SRCALPHA)
        orbitRList = []
        orbitSpeedList = []
        for ci in range(0,random.randint(1,5)):
            orbitRList.append(random.randint(10,100))
            orbitSpeedList.append(random.randint(10,100)*(1 if random.randint(0,1) == 0 else -1))
        circles.append({
            "rect": circlePos,
            "color": circleColor,
            "pulseSpeed": random.randint(5,50),
            "pulseR": pulseR,
            "orbitR": orbitRList,
            "orbitSpeed": orbitSpeedList,
            "surface": surface
        })
    counter = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        counter += 1
        screen.fill(backgroundColor)
        for circle in circles:
            posX = circle["rect"].centerx
            posY = circle["rect"].centery
            for orbitR, orbitSpeed in zip(circle["orbitR"],circle["orbitSpeed"]):
                posX += orbitR*math.cos(counter/orbitSpeed)
                posY += orbitR*math.sin(counter/orbitSpeed)
            csurface = circle["surface"]
            csurface.fill(emptyColor)
            csurfaceWidht = csurface.get_width()
            pygame.draw.circle(csurface,circle["color"], (csurfaceWidht/2,csurfaceWidht/2),circle["rect"].width/2+int(math.sin(counter/circle["pulseSpeed"])*circle["pulseR"]))
            screen.blit(csurface,(posX,posY))
        #pygame.draw.circle(screen,objectColor,screenRect.center,200)
        pygame.display.flip()
        clock.tick(50)

if __name__ == "__main__":
    main()
    pygame.quit()