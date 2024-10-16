#intellisense
from classes import *
from render import *
import time

def script(element, render):
    print((time.time()-element.lastUpdate)*1000, element.frameRate)
    if (time.time()-element.lastUpdate)*1000 > (1/element.frameRate)*1000:
        element.update_flag=True
        element.flag=True



def metadata():
    return {"runOn" : "frame"}