#intellisense
from classes import *
from render import *
import time


def script(element, render):
    import math
    i=render.f/1000
    offset=math.sin(i)
    element.offsetPosition[1]=offset


def metadata():
    return {"runOn" : "frame"}