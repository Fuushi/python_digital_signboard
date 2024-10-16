#intellisense
from classes import *
from render import *
import time


def script(element, render):
    progress=render.globals.get("progress", (1,1000))

    try:
        if progress != element.__progress:
            element.__progressLastUpdate=time.time()
    except AttributeError:
        element.__progressLastUpdate=time.time()

    element.__progress=progress

    #just incase
    if progress:
        #interpolate
        interpol=(time.time()-element.__progressLastUpdate)*1000

        #calculate offsets
        ratio=(progress[0]+interpol)/progress[1]

        width=element.size[0]

        offset=int(width*ratio)

        element.assets[element.source]['lines'][0]['offsets'][1][0]=offset
        element.assets[element.source]['lines'][1]['offsets'][0][0]=offset
    return

def metadata():
    return {"runOn" : "frame"}