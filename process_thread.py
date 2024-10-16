#SET ENV
DEBUG_DO_THREADING = True #FOR TESTING PURPOSES

#Just for Intellisense, remove in Live
from classes import *
from render import *

import os, sys, time, json
from datetime import datetime

from logger import logger

class processThread:
    def THREAD(render):
        


        ####
        print("INIT: Process")
        verbose=False
        startTime=time.time()
        frequency=1/(60*2)

        log=logger()

        while True:
            procStart=time.time()
            #run element scripts
            if render.scene and not render.suspend:
                
                for element in render.scene.elements:
                                #deal with element loading
                    if not element.initialized:
                        element.initialize()

                    if element.initialized and element.scripts:
                        for script in element.scripts:
                            if script:
                                script.run(element, render)
                            else:
                                raise FileNotFoundError
                            
                        #ensures only one thread can trigger an update at a time
                        safe=True
                        for thread in element.threads:
                            if thread['type'] == "updater": safe=False

                        #spawn updater threads
                        #(element.update_flag and element.initialized and safe)
                        if (element.update_flag and element.initialized and safe):
                            if element.type=="volume":
                                if (time.time()-element.PARTICLE_UPDATE_TIME)*1000 < 16*2: continue

                            if DEBUG_DO_THREADING:
                                thread=threading.Thread(target=element.update, args=())
                                thread.start()
                                element.threads.append({"type" : "updater", "ref" : thread})

                            else:
                                #single threaded processing
                                element.update()

                    #trigger re-render for text
                    if element.type=="text":

                        stringManupulation.fStringInterpreter(element)

                        if (element.text != element.rendered_text):
                            element.update_flag=True

                        if (element.type == "volume"): element.update_flag=True

                    #ensure threads die properly
                    for thread in element.threads:
                        if not thread['ref'].is_alive(): 
                            thread['ref'].join()
                            thread['ref']=None
                            element.threads.remove(thread)
                            del thread
                            gc.collect()
                    thread=None

            now = datetime.now() # current date and time
            timeS = now.strftime("%I:%M %p")
            if timeS[0] == "0":
                timeS=timeS[1:]
            render.globals['clock']=str(timeS)

            if render.dead:
                break

            if render.resetPROC:
                render.resetPROC=False
                return

            if verbose: print(f"Physics Updated, taking: {int(1000*(time.time()-procStart))}ms")
            if (frequency-(time.time()-procStart)) > 0: time.sleep(max(0,frequency-(time.time()-procStart)))
            elif verbose: print("Cant Keep up!")

        log.log("EXIT FROM PROCESS")
        print(f"EXIT: Process, after {int(1000*(time.time()-startTime))}")
