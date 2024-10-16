#intellisense
from classes import *
from render import *
from imgLib import *
import time


def script(element, render):
    ITERATIONS=10
    RADIUS=15
    ALPHA=(255/(2*ITERATIONS))
    if not element.assets.get("renderCache", None): return

    try:
        rendered=element.rendered_source = element.stateMachine.gaussianBlurRenderedSource
    except AttributeError:
        element.stateMachine.gaussianBlurRenderedSource = None
        rendered=None

    if element.source != rendered:
        print("STARTING GAUSS!!!")
        #gauss
        time.sleep(0.5) #DEBUG

        t1=time.time()
        
        #shaders.gauss(element.assets['renderCache'], 5, 2)

        #element.assets['renderCache'] = shaders.lazyGauss(element.assets['renderCache'], 8)

        element.assets['renderCache'] = shaders.gaussV3(element.assets['renderCache'], ITERATIONS, RADIUS, ALPHA)

        print(f"Gaussian Blur Complete, taking {int(1000*(time.time()-t1))}ms.")

        element.stateMachine.gaussianBlurRenderedSource = element.source
        
        print(element.offsetPosition)

        #apply offsets based on the size of the radius
        if element.offsetPosition[0] == 0:

            element.offsetPosition[0]-= RADIUS*2
            element.offsetPosition[1]-= RADIUS*2
        pass #BREAKPOINT
    return

def metadata():
    return {"runOn" : "update"}