#intellisense
from classes import *
from render import *
import time

def script(element, render):
    import random
    element.text=str(random.random())
    element.update_flag=True

def metadata():
    return {"runOn" : "frame"}