#intellisense
from classes import *
from render import *
import time

def script(element, render):
    raise DeprecationWarning
    state=element.states.get("pullDown", None)

    if not state:
        #start animation
        if (not element.down) and (not render.playing):
            print("Creating Drop Animation")
            frameDuration=50
            #start and end frame
            startFrame=render.f

            endFrame=render.f+frameDuration

            element.states["pullDown"]={
                "startFrame" : startFrame,
                "endFrame" : endFrame,
                "basePose" : (0,0), #deep copy
                "slope" : -1,
                "baseOffsets" : (element.offsetPosition[0], element.offsetPosition[1])
            }

            element.down=True

            pass
        elif (element.down) and (render.playing):
            print("Creating Lift Animation")
            frameDuration=50
            #start and end frame
            startFrame=render.f

            endFrame=render.f+frameDuration

            element.states["pullDown"]={
                "startFrame" : startFrame,
                "endFrame" : endFrame,
                "basePose" : (0,0), #deep copy
                "slope" : 1,
                "baseOffsets" : (element.offsetPosition[0], element.offsetPosition[1])
            }
            element.down=False


            pass
            
    else:
        #run animation
        #Offsets are calculated inline, only run this if rerender needed

        """frame=render.f-state['startFrame']
        _d=1

        #calc offsets
        yOffset=(math.cos(frame/((50/10)*3.141592))*state['slope']*(200*_d))+(200*_d)

        #apply scale to size
        element.offsetPosition[1]=yOffset

        #apply offsets to ensure centring

        #ensure update flag
        element.update_flag=True

        #ensure end of animation
        if render.f >= state['endFrame']:
            element.states["pullDown"]=None
            element.runEveryFrame=False"""

    return

def metadata():
    return {"runOn" : "update"}