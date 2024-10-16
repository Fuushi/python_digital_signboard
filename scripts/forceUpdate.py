#intellisense
from classes import *
from render import *
import time

def script(element, render):
    element.update_flag=True
    element.flag=True

def metadata():
    return {"runOn" : "frame"}