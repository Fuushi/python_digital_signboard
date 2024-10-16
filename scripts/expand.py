#intellisense
from classes import *
from render import *
import time

def script(element, render):
    if element.flashTrigger and element.flag:
        element.size = (200,100)
        element.update_flag=True

    if element.flashTrigger and not element.flag:
        element.size = (100,100)
        element.update_flag=True

def metadata():
    #can probably swap to update with some tuning
    return {"runOn" : "frame"}