import pygame

pos = pygame.math.Vector2(1,1.4)
v = pygame.math.Vector2(0.8,2.3)
c = pygame.math.Vector2(20,20)
lastP = 0
p = 0

screenRect = pygame.Rect((0,0,400,400))

pygame.init()
screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
pygame.display.set_caption('Balls Obstacles Demo')
running = True
backgroundColor = pygame.Color((0,0,0))
clock = pygame.time.Clock()
for i in range(0,100):
    lastP = p
    p = pos.distance_to(c)
    if lastP>0:
        print(f"p dif {lastP-p} p {p}")
    pos = pos + v
    screen.set_at((i*4,int(p)),pygame.Color(255,255,255))
pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    clock.tick(20)
