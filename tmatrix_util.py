import numpy
import math

# https://www.alanzucconi.com/2016/02/10/tranfsormation-matrix/

class TransMatrix2D:
    def __init__(self):
        self.m = numpy.eye(3)
        self.stack = []
    def push(self):
        self.stack.append(self.m.copy())
    def pop(self):
        self.m = self.stack.pop()
    def trans(self,v):
        t = numpy.eye(3)
        t[0,2] = v[0]
        t[1,2] = v[1]
        self.m = self.m @ t
    def scale(self,v):
        t = numpy.eye(3)
        t[0,0] = v[0]
        t[1,1] = v[1]
        self.m = self.m @ t
    def rotateGrad(self,grad):
        self.rotate(math.radians(grad))
    def rotate(self,radians):
        t = numpy.eye(3)
        cos = math.cos(radians)
        sin = math.sin(radians)
        t[0,0] = cos
        t[0,1] = sin
        t[1,0] = -sin
        t[1,1] = cos
        self.m = self.m @ t
    def share(self,v):
        t = numpy.eye(3)
        t[0,1] = v[0]
        t[1,0] = v[1]
        self.m = self.m @ t

def map(x,sourceFrom,sourceTo,targetFrom,targetTo):
    return targetFrom+(x-sourceFrom)*(targetTo-targetFrom)/(sourceTo-sourceFrom)