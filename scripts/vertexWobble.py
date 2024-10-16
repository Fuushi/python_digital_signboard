#intellisense
from classes import *
from render import *
import time, math, random

def script(element, render):
    factor=10
    i=render.f/10
    iterator=0
    for vertex in element.assets[element.source].get("lines", [{"points":[]}])[0]['points']:
        #fOffset=math.sin(vertex[0]+(vertex[0]*vertex[1]))+vertex[0]+vertex[1]#changes time
        fOffset=math.sin(vertex[0]*100)
        vertexOffsetX=math.sin(i+fOffset)*10
        vertexOffsetY=math.sin(i+fOffset+1.115)*10
        element.assets[element.source]['lines'][0]['offsets'][iterator][0]=vertexOffsetX
        element.assets[element.source]['lines'][0]['offsets'][iterator][1]=vertexOffsetY
        iterator+=1

    for vertex in element.assets[element.source].get("polys", [{"points":[]}])[0]['points']:
        #fOffset=math.sin(vertex[0]+(vertex[0]*vertex[1]))+vertex[0]+vertex[1]#changes time
        fOffset=math.sin(vertex[0]*100)
        vertexOffsetX=math.sin(i+fOffset)*10
        vertexOffsetY=math.sin(i+fOffset+1.115)*10
        element.assets[element.source]['polys'][0]['offsets'][iterator][0]=vertexOffsetX
        element.assets[element.source]['polys'][0]['offsets'][iterator][1]=vertexOffsetY
        iterator+=1
    #print(offsets)
        
def metadata():
    return {"runOn" : "frame"}