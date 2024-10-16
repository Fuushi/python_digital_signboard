#Just for Intellisense, remove in Live
from classes import *
from render import *
from imgLib import stringManupulation
import os, sys, time, json

class behavior:
    import time
    def __init__(self, state, render) -> None:
        #sets run interval to 1s
        self.interval=1#s

        self.base_hsv=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.start_time=time.time()

        #to prevent burnin, colors will be random
        #hsv format


        """if render.presetID=="lowPowerMode":
            #assign colors
            bg = render.scene.getElement("low_power_bg").assets.get('assets/square.json', None)
            clock = render.scene.getElement("clock").assets.get('assets/square.json', None)
            if bg and clock:
                bg['polys'][0]['color'] = c1
                clock.text_color=c2

            else:
                pass #assets still loading
        else:
            pass # not in low power mode
"""

    
    def run(self, state, render):
        #print(f"preset_id: {render.presetID}")
        #modify colors over time in sub-perceptible increments

        from imgLib import comp
        
        #get refs
        if render.presetID=="lowPowerMode":
            #assign colors
            bg = render.scene.getElement("low_power_bg").assets.get('assets/square.json', None)
            clock = render.scene.getElement("clock")
            if bg and clock:
                #update colors
                SPEED=0.8
                OFFSET=128
                SATURATION=80
                BRIGHTNESS=150                

                deg1= (self.base_hsv[0]+((time.time()-self.start_time)*SPEED))%255
                deg2=(deg1+OFFSET)%255

                h1=(deg1, SATURATION, BRIGHTNESS)
                h2=(deg2, SATURATION, BRIGHTNESS)

                c1=comp.hsv_to_rgb(*h1)
                c2=comp.hsv_to_rgb(*h2)

                bg['polys'][0]['color'] = c1
                clock.text_color = c2

                #print("updated color")
                
  


        #
        
        return
