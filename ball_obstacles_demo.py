from turtle import back
import pygame

screenRect = pygame.Rect((0,0,400,400))
objectColor = pygame.Color(255, 255, 255)

stop = False

class RectObstacle:
    def __init__(self,xy,size):
        self.rect = pygame.Rect(xy,size)
    def draw(self,surface):
        global objectColor
        pygame.draw.rect(surface,objectColor,self.rect)

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
    def tryObstacle(self,obstacle):
        global stop
        if self.rect.colliderect(obstacle.rect):
            # check side collision
            if (obstacle.rect.bottom>self.rect.centery and obstacle.rect.top<self.rect.centery) or (obstacle.rect.left<self.rect.centerx and obstacle.rect.right>self.rect.centerx):
                if self.rect.centerx<obstacle.rect.centerx:
                    if self.rect.centery<obstacle.rect.centery:
                        if self.rect.right-obstacle.rect.left<self.rect.bottom-obstacle.rect.top:
                            dir = 3
                        else:
                            dir = 0
                    else:
                        if self.rect.right-obstacle.rect.left<obstacle.rect.bottom-self.rect.top:
                            dir = 3
                        else:
                            dir = 2
                else:
                    if self.rect.centery<obstacle.rect.centery:
                        if obstacle.rect.right-self.rect.left<self.rect.bottom-obstacle.rect.top:
                            dir = 1
                        else:
                            dir = 0
                    else:
                        if obstacle.rect.right-self.rect.left<obstacle.rect.bottom-self.rect.top:
                            dir = 1
                        else:
                            dir = 2
                if dir==0:
                    self.moveV.y = -self.moveV.y
                elif dir==1:
                    self.moveV.x = -self.moveV.x
                elif dir==2:
                    self.moveV.y = -self.moveV.y
                elif dir==3:
                    self.moveV.x = -self.moveV.x
            else:
                # corner collision
                if self.rect.centerx>obstacle.rect.centerx:
                    if self.rect.centery>obstacle.rect.centery:
                        corner = obstacle.rect.bottomright
                    else:
                        corner = obstacle.rect.topright
                else:
                    if self.rect.centery>obstacle.rect.centery:
                        corner = obstacle.rect.bottomleft
                    else:
                        corner = obstacle.rect.topleft
                corner = pygame.math.Vector2(corner)
                r = corner.distance_to(self.pos)
                if r<self.rsize:
                    tangente = pygame.math.Vector2(self.pos.x-corner.x,self.pos.y-corner.y)
                    self.moveV.reflect_ip(tangente)
                

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
    pygame.display.set_caption('Balls Obstacles Demo')
    running = True
    backgroundSurface = pygame.Surface(screenRect.size,pygame.SRCALPHA)
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
        screen.fill(backgroundColor)
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