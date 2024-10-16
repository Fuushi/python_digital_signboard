#intellisense
from classes import *
from render import *
import time

def script(element, render):
    #only needs to run once
    if not element.globals:
        element.globals=render.globals

def metadata():
    #might only need to be done on init
    return {"runOn" : "frame"}