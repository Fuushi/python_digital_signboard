#intellisense
from classes import *
from render import *
import time

def script(element, render):
    #runs once per second

    #if in low power mode, run
    if render.presetID=="lowPowerMode":
        #change asset color from object reference to a random 8bit color
        assets=element.assets.get('assets/square.json', None)
        if assets:
            assets['polys'][0]['color'] = [
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        ]

    else:
        pass #not in low power mode

def metadata():
    #can probably swap to update with some tuning
    return {"runOn" : "frame"}