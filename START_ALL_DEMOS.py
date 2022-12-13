from telnetlib import RCP
import pygame
from demo_base import Demo, Scene
import ademo
import space_demo
import textfall2_demo
import textfall_demo
import waterdot_demo
import water_demo
import lines_demo
import colortunel_demo
import matrix_demo
import dots_demo
import dotsplane_demo
import dotsplane2_demo
import ball_demo
import ball_obstacles_demo
import colorblend_demo
import pygame_circles
import matrix2dTrans_demo
import textdots_demo
import processing_demo
import tree_demo

class AllScenes(Scene):
    backgroundColor = pygame.Color((0,0,0))
    def __init__(self,demo):
        self.scenes = [
            ademo.AScene(demo),
            space_demo.StarScene(demo),
            textfall2_demo.TextFallScene(demo),
            textfall_demo.TextFallScene(demo),
            waterdot_demo.WaterDotScene(demo),
            water_demo.WaterScene(demo),
            lines_demo.LinesScene(demo),
            colortunel_demo.ColorTunelScene(demo),
            matrix_demo.MatrixScene(demo),
            dots_demo.DotsScene(demo),
            dotsplane_demo.DotsPlaneScene(demo),
            dotsplane2_demo.DotsPlaneScene(demo),
            ball_demo.BallScene(demo),
            ball_obstacles_demo.BallScene(demo),
            colorblend_demo.BlendScene(demo),
            pygame_circles.CirclesScene(demo),
            matrix2dTrans_demo.DotsPlaneScene(demo),
            textdots_demo.DotsPlaneScene(demo),
            processing_demo.ProcessingScene(demo),
            tree_demo.TreeScene(demo),
        ]
        self.currentSceneIndex = 0
        self.currentScene = self.scenes[self.currentSceneIndex]
        font = pygame.font.SysFont("mono", 18,bold=True)
        self.charImages = {}
        self.descriptionPos = 0
        self.descriptionFinished = False
        for o in list(range(ord('A'),ord('Z')+1))+list(range(ord('0'),ord('9')+1))+[ord(c) for c in list(".,-!*")]:
            c = chr(o)
            if c not in self.charImages:
                self.charImages[c] = font.render(c, True, pygame.Color(255,255,255))
        Scene.__init__(self,demo)
    def update(self,demo,counter):
        self.currentScene.update(demo,counter)
        self.descriptionPos += 2
    def draw(self,demo):
        self.currentScene.draw(demo)
        if not self.descriptionFinished and hasattr(self.currentScene,"description"):
            demo.screen.fill(self.backgroundColor,pygame.rect.Rect(0,demo.screenRect.height-20,demo.screenRect.width,20))
            cpos = 0
            for c in list(self.currentScene.description.upper()):
                if c==' ':
                    cpos += 12
                    continue
                charImg = self.charImages[c]
                rcPos = cpos-self.descriptionPos+demo.screenRect.width
                if rcPos>demo.screenRect.width:
                    break
                if rcPos+charImg.get_width()>0:
                    demo.screen.blit(charImg,(rcPos,demo.screenRect.height-20))
                cpos += charImg.get_width()
            if rcPos+12<0:
                self.descriptionFinished = True
    def processEvent(self,demo,event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.currentSceneIndex += 1
            if self.currentSceneIndex>=len(self.scenes):
                self.currentSceneIndex = 0
            self.currentScene = self.scenes[self.currentSceneIndex]
            self.descriptionPos = 0
            self.descriptionFinished = False
            if hasattr(self.currentScene,"title"):
                pygame.display.set_caption(self.currentScene.title)
            demo.screen.fill(self.backgroundColor)
            self.currentScene.reset(demo)

if __name__ == "__main__":
    demo = Demo("All Demos",(800,600),20)
    AllScenes(demo)
    demo.start()
    pygame.quit()