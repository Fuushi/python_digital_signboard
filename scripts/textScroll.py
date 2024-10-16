#intellisense
from classes import *
from render import *
import time


def script(element, render):
    try:
        WIDTH=element.assets['raw'].get_size()[0]

        #ignore when not playing
        if not render.playing: return

        #ignore for small text
        if WIDTH <= 820: return

        
        SPEED = 150 #pixels per second
        FRMRATE=60

        DURATION_S = WIDTH/SPEED

        FRAMES=int(DURATION_S*FRMRATE)*3

        f=render.f

        interval=f%FRAMES

        #calc slope
        deltaT = FRAMES - (FRAMES/2)
        deltaX = WIDTH

        slope = deltaX/deltaT

        offset=(interval-(FRAMES/2))*slope

        result=max(0, int(offset))

        #avoid recalculation of text unless necessary
        if (result == 0) and (interval != 10):
            return

        #crop text
        cropped_surface = element.assets['raw'].subsurface(pygame.Rect(result, 0, element.assets['raw'].get_width() - result, element.assets['raw'].get_height()))
        
        element.assets['renderCache']=cropped_surface
    except:
        pass
    return

def metadata():
    return {"runOn" : "frame"}