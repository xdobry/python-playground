import pygame
import math

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
        self.hasCollisionWith = []
    # collision with another ball
    def tryCollision(self,ball):
        global stop
        distS = self.pos.distance_squared_to(ball.pos) 
        if distS<self.rsize2s:
            # compute the time when the ball are exactly matching
            # then move back to the time compute reflection and add the time again
            D = self.pos-ball.pos
            Dx = D.x
            Dy = D.y
            d = self.moveV-ball.moveV
            dx = d.x
            dy = d.y
            dxq = dx**2
            dyq = dy**2
            # maxima solve([(Dx-t*dx)^2+(Dy-t*dy)^2=r],[t]);
            #t0 = -(math.sqrt((dy**2+dx**2)*r-Dx**2*dy**2+2*Dx*Dy*dx*dy-Dy**2*dx**2)-Dy*dy-Dx*dx)/(dy**2+dx**2)
            t1 = (math.sqrt((dyq+dxq)*self.rsize2s-Dx**2*dyq+2*Dx*Dy*dx*dy-Dy**2*dxq)+Dy*dy+Dx*dx)/(dyq+dxq)
            #print(f"t0 {t0} t1 {t1}")
            self.pos = self.pos - t1 * self.moveV
            ball.pos = ball.pos - t1 * ball.moveV
            #newDist = self.pos.distance_to(ball.pos)
            #print(f"newDist {newDist}")
            tangente = ball.pos - self.pos
            tangenteOrtho = pygame.math.Vector2(tangente.y,-tangente.x)
            selfTProj = self.moveV.project(tangente)
            selfTOProj = self.moveV.project(tangenteOrtho)
            ballTProj = ball.moveV.project(tangente)
            ballTOProj = ball.moveV.project(tangenteOrtho)
            self.moveV = ballTProj + selfTOProj
            ball.moveV = selfTProj + ballTOProj
            self.pos = self.pos + t1 * self.moveV
            ball.pos = ball.pos + t1 * ball.moveV
            self.rect.center = self.pos
            ball.rect.center = ball.pos

    # collision with rect obstacle            
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
                    ty = (self.rect.bottom-obstacle.rect.top)/self.moveV.y
                    #print(f"dir {dir} ty {ty}")
                    self.pos = self.pos - self.moveV * ty
                    self.moveV.y = -self.moveV.y
                    self.pos = self.pos + self.moveV * ty                    
                elif dir==1:
                    tx = (self.rect.left-obstacle.rect.right)/self.moveV.x
                    #print(f"dir {dir} ty {tx}")
                    self.pos = self.pos - self.moveV * tx
                    self.moveV.x = -self.moveV.x
                    self.pos = self.pos + self.moveV * tx                    
                elif dir==2:
                    ty = (self.rect.top-obstacle.rect.bottom)/self.moveV.y
                    #print(f"dir {dir} ty {ty}")
                    self.pos = self.pos - self.moveV * ty
                    self.moveV.y = -self.moveV.y
                    self.pos = self.pos + self.moveV * ty                    
                elif dir==3:
                    tx = (self.rect.right-obstacle.rect.left)/self.moveV.x
                    #print(f"dir {dir} ty {tx}")
                    self.pos = self.pos - self.moveV * tx
                    self.moveV.x = -self.moveV.x
                    self.pos = self.pos + self.moveV * tx
                self.rect.center = self.pos                   
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
                    vx = self.moveV.x
                    vy = self.moveV.y
                    vxq = vx * vx
                    vyq = vy * vy
                    r1x = corner.x - self.pos.x
                    r1y = corner.y - self.pos.y
                    rq = self.rsize * self.rsize
                    # t is the time needed to set back the ball to exactly match the corner
                    # vectors: r1 = r0-tv
                    # v - is bewegung
                    # r0 - gesuchter vector (ball center zu corner)
                    # | r0 | = r^2
                    # mit hilfe von maxima
                    t1 = -(math.sqrt((rq-r1x*r1x)*vyq+2*r1x*r1y*vx*vy+(rq-r1y*r1y)*vxq)-r1y*vy-r1x*vx)/(vyq+vxq)
                    #t2 = (math.sqrt((rq-r1x*r1x)*vyq+2*r1x*r1y*vx*vy+(rq-r1y*r1y)*vxq)+r1y*vy+r1x*vx)/(vyq+vxq)
                    #rqs = (r1x-t1*vx)*(r1x-t1*vx)+(r1y-t1*vy)*(r1y-t1*vy)
                    #s01 = self.pos + t1 * self.moveV
                    #s02 = self.pos + t2 * self.moveV
                    #r01 = corner.distance_to(s01)
                    #r02 = corner.distance_to(s02)
                    #print(f"t1 {t1} t2 {t2} rqs={rqs} rq={rq} r01={r01} r02={r02}")
                    self.pos = self.pos + self.moveV * t1
                    #r0 = corner.distance_to(self.pos)
                    #print(f"r0 {r0}")
                    r0 = self.pos-corner
                    self.moveV.reflect_ip(r0)
                    self.pos = self.pos - self.moveV * t1
                    self.rect.center = self.pos 
                

    def update(self):
        self.pos = self.pos + self.moveV
        if (self.pos.x<=self.rsize and self.moveV.x<0):
            tx = -(self.rsize-self.pos.x)/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
            #print(f"rc 0 tx {tx} {self.pos}")
        elif (self.pos.x+self.rsize)>=Ball.screenRect.width and self.moveV.x>0:
            tx = (self.pos.x+self.rsize-Ball.screenRect.width)/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
            #print(f"rc 1 tx {tx} {self.pos}")
        if self.pos.y<=self.rsize and self.moveV.y<0:
            ty = -(self.rsize-self.pos.y)/self.moveV.y
            self.pos = self.pos - self.moveV * ty
            self.moveV.y = -self.moveV.y
            self.pos = self.pos + self.moveV * ty
            #print(f"rc 2 ty {ty} {self.pos}")
        elif self.pos.y+self.rsize>=Ball.screenRect.height and self.moveV.y>0:
            ty = (self.pos.y+self.rsize-Ball.screenRect.height)/self.moveV.y
            self.pos = self.pos - self.moveV * ty
            self.moveV.y = -self.moveV.y
            self.pos = self.pos + self.moveV * ty
            #print(f"rc 3 ty {ty} {self.pos}")
        self.rect.center = self.pos