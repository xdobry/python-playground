import pygame
import random
import math

screenRect = pygame.Rect((0,0,800,600))
matrixColor = pygame.Color(3, 160, 98)
backgroundColor = pygame.Color((0,0,0))


class Strip:
    def __init__(self,column,rows,charSize):
        self.pos = 0
        self.column = column
        self.height = rows*charSize[1]
        self.charSize = charSize
    def draw(self,textSource,screen):
        startX = 0 if self.pos<self.height else self.pos-self.height
        h = self.pos if self.pos<self.height else self.height
        screen.blit(textSource.textSource,(self.column*self.charSize[0],startX),pygame.rect.Rect(self.column*self.charSize[0],startX,self.charSize[0],h))
        if self.pos<screenRect.height:
            screen.blit(textSource.textSource,(self.column*self.charSize[0],self.pos-self.charSize[1]),pygame.rect.Rect(self.column*self.charSize[0],self.pos-self.charSize[1],self.charSize[0],self.charSize[1]),special_flags=pygame.BLEND_RGBA_ADD)
    def update(self,textSource):
        self.pos += 8
        if self.pos>screenRect.height+self.height:
            self.pos = 0
            self.column = random.randint(0,textSource.posSize[0])
            self.rows = random.randint(3,8)

class TextSource:
    def __init__(self,screen):
        self.textSource = pygame.Surface((screen.get_width(),screen.get_height()))
        self.textSource2 = pygame.Surface((screen.get_width(),screen.get_height()))
        self.textSource3 = pygame.Surface((screen.get_width(),screen.get_height()))
        font = pygame.font.SysFont("mono",32, bold=True)
        self.characters = [font.render(chr(c), True, matrixColor) for c in range(ord("A"),ord("Z")+1)]
        self.charSize = (self.characters[0].get_width(),self.characters[0].get_height()-4)
        self.posSize = (int(screenRect.width/self.charSize[0])+1,int(screenRect.height/self.charSize[1]+1))
        for x in range(0,self.posSize[0]):
            for y in range(0,self.posSize[1]):
                if random.random()>0.2:
                    self.blitChar(x,y,random.randint(0,len(self.characters)-1))
    def blitChar(self,x,y,char):
        self.textSource.blit(self.characters[char],(x*self.charSize[0],y*self.charSize[1]))
    def update(self):
        for i in range(0,5):
            rx = random.randint(0,self.posSize[0])
            ry = random.randint(0,self.posSize[1])
            self.textSource.fill(backgroundColor,pygame.rect.Rect(self.charSize[0]*rx,self.charSize[1]*ry,self.charSize[0],self.charSize[1]))
            if random.random()>0.2:
                char = random.randint(0,len(self.characters)-1)
                self.blitChar(rx,ry,char)

def main():
    pygame.init()
    screen = pygame.display.set_mode(screenRect.size, pygame.DOUBLEBUF)
    pygame.display.set_caption('Matrix Falling Code')
    running = True
    clock = pygame.time.Clock()
    counter = 0
    strips = []
    textSource = TextSource(screen)
    for i in range(0,2):
        strips.append(Strip(random.randint(0,textSource.posSize[0]),random.randint(8,10),textSource.charSize))
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill(backgroundColor)
        textSource.update()
        if len(strips)<15:
            if random.random()<0.01:
                strips.append(Strip(random.randint(0,textSource.posSize[0]),random.randint(8,15),textSource.charSize))
        for strip in strips:
            strip.update(textSource)
            strip.draw(textSource,screen)
        pygame.display.flip()
        clock.tick(40)
        counter+=1

if __name__ == "__main__":
    main()
    pygame.quit()