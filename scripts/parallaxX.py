#intellisense
from classes import *
from render import *
import time


def script(element, render):
    factor=0.02

    element.offsetPosition[0] = 0
    #delta from middle
    ratio = (render.mouse_pos[0] - int(render.window['x']/2)) / int(render.window['x']/2)

    element.offsetPosition[0] = ratio*int(render.window['x']/2)*factor*(element.zoffset+0.001)

def metadata():
    return {"runOn":"frame"}