#intellisense
from classes import *
from render import *
import time


def script(element, render):
    ## adjust offsets based off render cache
        ##use element size as fallback
    ## centre div along element position (only applies to x for my usecase)

    render=element.assets.get("renderCache", None)
    if render:
        size=render.get_size()

    else:
        #use element size
        size=element.size

    offsetX= 0 - int(size[0]/2)
    #offsetY= 0# - int(size[1]/2)

    element.offsetPosition[0]=offsetX
        
    return

def metadata():
    return {"runOn" : "frame"}