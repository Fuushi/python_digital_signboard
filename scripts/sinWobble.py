#intellisense
from classes import *
from render import *
import time

        
def script(element, render):
    #TODO
    i=render.f/10
    radius=50
    period=10
    factor=1
    xoffset=math.sin(i/period*-1)*radius*(element.zoffset)
    yoffset=math.cos(i/period*-1)*radius*(element.zoffset)


    element.offsetPosition[0] = xoffset*factor
    element.offsetPosition[1] = yoffset*factor
    pass 

def metadata():
    return {"runOn" : "frame"}