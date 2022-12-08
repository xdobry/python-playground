import pygame

def genColors(startColor,endColor,steps):
    colors = []
    startV = pygame.math.Vector3(startColor.r,startColor.g,startColor.b)
    endV = pygame.math.Vector3(endColor.r,endColor.g,endColor.b)
    for s in range(0,steps):
        colorV = startV.lerp(endV,s/steps)
        colors.append(pygame.Color(int(colorV.x),int(colorV.y),int(colorV.z)))
    return colors