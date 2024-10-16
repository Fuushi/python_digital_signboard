#Just for Intellisense, remove in Live
from classes import *
from render import *
from imgLib import stringManupulation
import os, sys, time, json

MEMORY_LENGTH=1 #60*2
PING_INTERVAL=10

class behavior:
    def __init__(self, state, render) -> None:
        #imports
        import pythonping
        self.pinglib = pythonping
        self.history=[False]
        self.interval=PING_INTERVAL
        return
    
    def run(self, state, render):
        from presets import Presets
        resp = self.pinglib.ping(
            target="172.16.1.113",
            timeout=1,
            count=1
        )

        self.history.append(resp.success())

        if len(self.history) >= MEMORY_LENGTH: self.history=self.history[1:]

        run = (True in self.history)

        if not run:
            ## suspend the application
            #print("Suspend")
            if render.presetID != "lowPowerMode" and render.scene:
                #suspend rendering while swapping scene
                render.loadSceneFromFile("lowPowerMode")
            pass
        else:
            ## resume the applciation if necessary
            #print("Run")
            if (render.presetID == "lowPowerMode") and render.scene:
                render.loadSceneFromFile("home")
            pass

        #print(self.history)

        


        #auto shutoff
        #home = ping(state) #TODO move into a behavior class
        #render.pause = (not home) and not True #True is disabler for feature
        return