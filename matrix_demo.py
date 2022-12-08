import pygame
import random
from demo_base import Demo, Scene

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

class MatrixScene(Scene):
    def __init__(self,demo):
        Scene.__init__(self,demo)
        self.strips = []
        self.textSource = TextSource(demo.screen)
        for i in range(0,2):
            self.strips.append(Strip(random.randint(0,self.textSource.posSize[0]),random.randint(8,10),self.textSource.charSize))
    def update(self,demo,counter):
        self.textSource.update()
        if len(self.strips)<15:
            if random.random()<0.01:
                self.strips.append(Strip(random.randint(0,self.textSource.posSize[0]),random.randint(8,15),self.textSource.charSize))
        for strip in self.strips:
            strip.update(self.textSource)
    def draw(self,demo):
        demo.screen.fill(backgroundColor)
        for strip in self.strips:
            strip.draw(self.textSource,demo.screen)

if __name__ == "__main__":
    demo = Demo("Matrix",(800,600),20)
    MatrixScene(demo)
    demo.start()
    pygame.quit()