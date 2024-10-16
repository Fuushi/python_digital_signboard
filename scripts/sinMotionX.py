#intellisense
from classes import *
from render import *
import time

        
def script(element, render):
    import math
    i=render.f/100
    offset=math.sin(i)*50
    element.offsetPosition[0]=offset

def metadata():
    return {"runOn" : "frame"}