#intellisense
from classes import *
from render import *
import time


def script(element, render):
    factor=0.02

    element.offsetPosition[1] = 0
    #delta from middle
    ratio = (render.mouse_pos[1] - int(render.window['x']/2)) / int(render.window['x']/2)
    
    element.offsetPosition[1] = ratio*int(render.window['x']/2)*factor*(element.zoffset+0.00001)

def metadata():
    return {"runOn" : "frame"}