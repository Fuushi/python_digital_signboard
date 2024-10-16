#intellisense
from classes import *
from render import *
import time


def script(element, render):
    element.flashTrigger=False
    if (render.mouse_pos[0] > element.position[0]+element.offsetPosition[0] and render.mouse_pos[0] < element.position[0]+(element.size[0]+element.offsetScale[0])+element.offsetPosition[0]) and (render.mouse_pos[1] > element.position[1]+element.offsetPosition[1] and render.mouse_pos[1] < element.position[1]+(element.size[1]+element.offsetScale[1])+element.offsetPosition[1]):
        if element.flag != True:
            element.flashTrigger=True
        element.flag=True
    else:
        if element.flag:
            element.flashTrigger=True
        element.flag=False
        
        
def metadata():
    return {"runOn" : "frame"}