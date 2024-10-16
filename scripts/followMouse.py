#intellisense
from classes import *
from render import *
import time


def script(element, render):
    element.offsetPosition=render.mouse_pos

def metadata():
    return {"runOn" : "frame"}