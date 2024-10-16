#Just for Intellisense, remove in Live
from classes import *
from render import *
from imgLib import stringManupulation
from logger import logger

import os, sys, time, json

class behaviorThread:
    #spotify thread is misleading, this is the general async thread
    def  __init__(self, render) -> None:   
        print("INIT: spotify")
        startTime=time.time()
        self.logger=logger()

        #construct state machine
        state=State()

        #get behavior constructor classes
        constructors=importer.getBehaviors()

        #initialize behavior objects
        behaviors=[]
        for constructor in constructors:
            behaviors.append(
                constructor(state, render)
            )

        #declare scope variables before entering loop
        i=0

        while True:
            #set loop startTime
            t1=time.time()

            #run behaviors
            for behavior in behaviors:
                if (i % behavior.interval) == 0: behavior.run(state, render)

            #exit clause
            if render.dead: break

        
            #iterate interals
            i+=1
            duration=1
            if time.time()-t1 > duration: pass
            else: time.sleep(max(0,duration-(time.time()-t1)))

            if render.resetBEHAVIOR:
                render.resetBEHAVIOR=False
                break
            
        #exit()
        self.logger.log("EXIT FROM BEHAVIOR")
        print(f"EXIT: spotify, after {int(1000*(time.time()-startTime))}")
        return #only run on exit
    

#state machine constructor (Deprecaited?)
class State:
    def __init__(self) -> None:
        self.pings=[]
        pass



class importer:
    def importer(module_path, function_name="behavior"):
        import importlib.util
        # Load the module
        spec = importlib.util.spec_from_file_location("module_name", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the function from the module
        func = getattr(module, function_name)

        return func

    def getBehaviors(path="behaviors/"):
        if not os.path.exists(path):return

        files = os.listdir(path)

        if not files: return

        foo=[]

        for file in files:
            if ".py" in file: foo.append(importer.importer(os.path.join(path, file), "behavior"))

        return foo
