import numpy
import pygame
from tmatrix_util import TransMatrix2D

class Processing:
    def __init__(self,screen):
        self.screen = screen
        self.color = pygame.color.Color(255,255,255)
        self.m = TransMatrix2D()
    def line(self,fromPos,toPos):
        transPoints = self.transPoints([fromPos,toPos])
        pygame.draw.line(self.screen,self.color,transPoints[0],transPoints[1])
    def transPoint(self,pos):
        point = numpy.array([pos[0],pos[1],1],dtype=float)
        pointTrans = self.m.m @ point
        return int(pointTrans[0]),int(pointTrans[1])
    def transPoints(self,points):
        points = numpy.column_stack((numpy.array(points,dtype=float),numpy.ones(len(points))))
        transPoints = []
        for dot in points.dot(self.m.m.T):
            transPoints.append((int(dot[0]),int(dot[1])))
        return transPoints