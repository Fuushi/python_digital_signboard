#intellisense
from classes import *
from render import *
import time

def script(element, render):
    #run flag if both mouse over, and mouse click
    element.flashTrigger=False
    if (render.mouse_pos[0] > element.position[0]+element.offsetPosition[0] and render.mouse_pos[0] < element.position[0]+element.size[0]+element.offsetPosition[0]) and (render.mouse_pos[1] > element.position[1]+element.offsetPosition[1] and render.mouse_pos[1] < element.position[1]+element.size[1]+element.offsetPosition[1]):
        #if element.flag != True:
        #    element.flashTrigger=True
        if render.click:
            element.flag=True
            element.flashTrigger=True
            print("FLAG: click")
        else:
            #element.flag=False
            #element.flashTrigger=False
            pass
    else:
        #element.flag=False
        #element.flashTrigger=False
        pass


def metadata():
    return {"runOn" : "frame"}