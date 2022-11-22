import pygame
import math

screenRect = pygame.Rect((0,0,400,500))
objectColor = pygame.Color(255, 255, 255)

class Brett(pygame.sprite.Sprite):
    bsize = (100,10)
    speed = 3
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(self.bsize)
        xpos = screenRect.width/2-self.bsize[1]/2
        ypos = screenRect.height-self.bsize[1]-5
        self.rect = pygame.Rect((xpos,ypos),self.image.get_rect().size)
        self.image.fill(objectColor)
        
    def move(self,direction):
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(screenRect)
    def reset(self):
        self.rect.x = screenRect.width/2-self.bsize[1]/2

class Ball(pygame.sprite.Sprite):
    bsize = 10
    speed = 3
    def __init__(self,brett):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.bsize,self.bsize),pygame.SRCALPHA)
        pygame.draw.circle(self.image,objectColor,(self.bsize/2,self.bsize/2),self.bsize/2)
        self.rect = pygame.Rect(screenRect.center,self.image.get_rect().size)
        self.moveV = pygame.math.Vector2((self.speed,self.speed))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.limit = brett.rect.top
        self.lost = False
        self.brett = brett
    def update(self, gameContext):
        if gameContext["gameState"]==1:
            return
        self.pos = self.pos + self.moveV
        if (self.pos.x<=0 and self.moveV.x<0):
            tx = self.pos.x/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
        elif (self.pos.x+self.rect.width>=screenRect.width and self.moveV.x>0):
            tx = (self.pos.x+self.rect.width-screenRect.width)/self.moveV.x
            self.pos = self.pos - self.moveV * tx
            self.moveV.x = -self.moveV.x
            self.pos = self.pos + self.moveV * tx
        if self.pos.y<=0 and self.moveV.y<0:
            ty = self.pos.y/self.moveV.y
            self.pos = self.pos - self.moveV * ty
            self.moveV.y = -self.moveV.y
            self.pos = self.pos + self.moveV * ty
        elif self.pos.y+self.rect.height>=self.limit and self.moveV.y>0:
            if self.pos.x+self.bsize/2<self.brett.rect.x or self.pos.x+self.rect.width-self.bsize/2>self.brett.rect.right:
                self.lost = True
            else:
                ty = (self.pos.y+self.rect.height-self.limit)/self.moveV.y
                self.pos = self.pos - self.moveV * ty
                self.moveV.y = -self.moveV.y
                self.pos = self.pos + self.moveV * ty
                m = (self.pos.x+self.rect.width/2-self.brett.rect.centerx)/(self.brett.rect.width/2)
                if abs(m)>0.5:
                    #print(f"rotate {m}")
                    self.moveV.rotate_rad_ip(math.sqrt(abs(m))*(1 if m>0 else -1))
        self.rect.topleft = self.pos
    def reset(self):
        self.pos.x = screenRect.centerx
        self.pos.y = screenRect.centery
        self.lost = False
        self.moveV.x = self.speed
        self.moveV.y = self.speed
    def tileCollision(self,tile):
        if abs(self.rect.centerx-tile.rect.centerx) > abs(self.rect.centery-tile.rect.centery):
            self.moveV.x = -self.moveV.x
        else:
            self.moveV.y = -self.moveV.y
    def speedUp(self):
        self.moveV.scale_to_length(self.moveV.length()+2)

class Label(pygame.sprite.Sprite):
    def __init__(self,gameContext,text):
        pygame.sprite.Sprite.__init__(self)
        self.image = gameContext["font"].render(text,True,"white")
        self.rect = pygame.Rect((0,0),self.image.get_rect().size)
        self.rect.center = (screenRect.width/2,screenRect.height/2)

class Tile(pygame.sprite.Sprite):
    size = (50,50)
    image = pygame.Surface(size,)
    columns = 6
    rows = 3
    gap = (screenRect.width-columns*size[0])/(columns+1)
    image.fill(objectColor)

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((self.gap+x*(self.gap+self.size[0]),self.gap+y*(self.gap+self.size[1])),self.size)
    

def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Ping')
    running = True
    brett = Brett()
    group = pygame.sprite.Group()
    group.add(brett)
    ball = Ball(brett)
    group.add(ball)
    backgroundColor = pygame.Color((0,0,0))
    clock = pygame.time.Clock()
    # 0 - playing
    # 1 - game over
    gameContext = {
        "gameState": 0,
        "font": pygame.font.SysFont(None, 24)
    }
    tiles = []
    lblGameOver = Label(gameContext,"GAME OVER")
    tilesMaxButton = 0
    for x in range(0,Tile.columns):
        for y in range(0,Tile.rows):
            tile = Tile(x,y)
            tiles.append(tile)
            group.add(tile)
            tilesMaxButton = max(tilesMaxButton,tile.rect.bottom)
    tilesMaxCount = len(tiles)
    tilesCount = tilesMaxCount
    
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        keystate = pygame.key.get_pressed()
        if gameContext["gameState"]==0:
            brett.move(keystate[pygame.K_RIGHT]-keystate[pygame.K_LEFT])
        elif gameContext["gameState"]==1:
            if keystate[pygame.K_SPACE]:
                gameContext["gameState"] = 0
                lblGameOver.kill()
                ball.reset()
                brett.reset()
                tilesCount = tilesMaxCount
                for tile in tiles:
                    group.add(tile)
        screen.fill(backgroundColor)
        group.update(gameContext)
        if ball.lost:
            gameContext["gameState"] = 1
            group.add(lblGameOver)
        else:
            for tile in tiles:
                if tile.alive() and ball.rect.colliderect(tile.rect):
                    ball.tileCollision(tile)
                    tile.kill()
                    tilesCount-=1
            if tilesCount==0 and ball.rect.top>tilesMaxButton:
                for tile in tiles:
                    group.add(tile)
                tilesCount = tilesMaxCount
                ball.speedUp()
        group.draw(screen)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
    pygame.quit()