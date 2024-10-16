#intellisense
from classes import *
from render import *
import time


def script(element, render):
    #TODO migrate scale to use element.offsetScale, make scale attribute protected
    state=element.states.get("expandSmooth", None)
    if state:
        print("Running Animation")
        #handle running animation

        #calc scale
        scaleAdder = state['deformSlope']*(render.f-state['startFrame'])+1

        #apply scale to size
        element.offsetScale=(int(scaleAdder+state['baseSize'][0]),element.offsetScale[1])

        #apply offsets to ensure centring

        #ensure update flag
        element.update_flag=True

        #ensure end of animation
        if render.f >= state['endFrame']:
            element.states["expandSmooth"]=None
            element.runEveryFrame=False

        pass

    else:
        if element.flashTrigger and element.flag:
            print("Creating Open Animation")
            #start animation
            #constants
            frameDuration=30

            #start and end frame
            startFrame=render.f

            endFrame=render.f+frameDuration

            #define formula
            deformSlope=10/3

            #force updates every frame until complete

            element.states["expandSmooth"]={
                "startFrame" : startFrame,
                "endFrame" : endFrame,
                "deformSlope" : deformSlope,
                "baseSize" : (0,0), #deep copy
                "baseOffsets" : (element.offsetPosition[0], element.offsetPosition[1])
            }
            element.runEveryFrame=True

            pass
        if element.flashTrigger and not element.flag:
            print("Creating Close Animation")

            frameDuration=30

            #start and end frame
            startFrame=render.f

            endFrame=render.f+frameDuration

            #define formula
            deformSlope=10/-3

            #force updates every frame until complete

            element.states["expandSmooth"]={
                "startFrame" : startFrame,
                "endFrame" : endFrame,
                "deformSlope" : deformSlope,
                "baseSize" : (100,100 ), #deep copy
                "baseOffsets" : (element.offsetPosition[0], element.offsetPosition[1])
            }
            element.runEveryFrame=True

            #undo animation
            #element.update_flag=True
            pass

def metadata():
    return {"runOn" : "frame"}
