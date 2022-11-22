import pygame
import math

screenRect = pygame.Rect((0,0,400,400))
objectColor = pygame.Color(255, 255, 255)


class Ball(pygame.sprite.Sprite):
    rsize = 30
    rsize2s = (rsize*2)**2
    def __init__(self,pos,move,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.rsize*2,self.rsize*2),pygame.SRCALPHA)
        pygame.draw.circle(self.image,color,(self.rsize,self.rsize),self.rsize)
        self.rect = pygame.Rect(pos,self.image.get_rect().size)
        self.moveV = pygame.math.Vector2(move)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.rect.center = self.pos
        self.hasCollision = False
    def tryCollision(self,ball):
        global stop
        distS = self.pos.distance_squared_to(ball.pos) 
        if distS<self.rsize2s:
            if not self.hasCollision:
                tangente = ball.pos - self.pos 
                tangenteOrtho = pygame.math.Vector2(tangente.y,-tangente.x)
                selfTProj = self.moveV.project(tangente)
                selfTOProj = self.moveV.project(tangenteOrtho)
                ballTProj = ball.moveV.project(tangente)
                ballTOProj = ball.moveV.project(tangenteOrtho)
                self.moveV = ballTProj + selfTOProj
                ball.moveV = selfTProj + ballTOProj
                self.hasCollision = True
        else:
            self.hasCollision = False

    def update(self):
        self.pos = self.pos + self.moveV
        if (self.pos.x<=self.rsize and self.moveV.x<0):
            tx = (self.rsize-self.pos.x)/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
        elif (self.pos.x+self.rsize)>=screenRect.width and self.moveV.x>0:
            tx = (self.pos.x+self.rsize-screenRect.width)/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
        if self.pos.y<=self.rsize and self.moveV.y<0:
            ty = (self.rsize-self.pos.y)/self.moveV.y
            self.pos = self.pos - self.moveV * ty
            self.moveV.y = -self.moveV.y
            self.pos = self.pos + self.moveV * ty
        elif self.pos.y+self.rsize>=screenRect.height and self.moveV.y>0:
            ty = (self.pos.y+self.rsize-screenRect.height)/self.moveV.y
            self.pos = self.pos - self.moveV * ty
            self.moveV.y = -self.moveV.y
            self.pos = self.pos + self.moveV * ty
        self.rect.center = self.pos
    

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