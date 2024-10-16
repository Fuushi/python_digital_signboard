#intellisense
from classes import *
from render import *
import time

def script(element, render):
    ##
    element.flashTrigger=False #manual override
    state=element.states.get("mouse", None)

    mouseOver=(render.mouse_pos[0] > element.position[0]+element.offsetPosition[0] and render.mouse_pos[0] < element.position[0]+element.size[0]+element.offsetPosition[0]) and (render.mouse_pos[1] > element.position[1]+element.offsetPosition[1] and render.mouse_pos[1] < element.position[1]+element.size[1]+element.offsetPosition[1])
    
    if not state:
        element.states["mouse"]={
            "pos" : render.mouse_pos,
            "mouse_over" : mouseOver
        }
    else:
        state['pos']=render.mouse_pos
        state['mouse_over']=mouseOver

    if mouseOver and render.click:
        element.flag=True
        element.flashTrigger=True
        print("FLAG: click")

def metadata():
    return {"runOn" : "frame"}