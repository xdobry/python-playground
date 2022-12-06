import pygame

class Scene:
    def __init__(self,demo):
        demo.addScene(self)
    def processEvent(self,demo,event):
        None
    def update(self,demo,counter):
        None
    def draw(self,demo):
        None
    def isRunning(self,counter):
        return True

class Demo:
    def __init__(self,title,screenSize,clock=50):
        pygame.init()
        self.screenRect = pygame.rect.Rect((0,0,screenSize[0],screenSize[1]))
        self.title = title
        self.scenes = []
        self.currentScene = None
        self.clock = clock
        None
    def addScene(self,scene):
        self.scenes.append(scene)
        self.currentScene = scene  
    def start(self):
        self.screen = pygame.display.set_mode(self.screenRect.size, pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)
        clock = pygame.time.Clock()
        running = True
        counter = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif self.currentScene:
                    self.currentScene.processEvent(self,event)
            counter+=1
            if self.currentScene:
                self.currentScene.update(self,counter)
                self.currentScene.draw(self)
                if not self.currentScene.isRunning(counter):
                    running = False
            pygame.display.flip()
            clock.tick(50)

