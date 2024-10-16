import pygame
from scripts import *
from imgLib import *
from element_types import *
import os, time, json, sys, re, random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor



class Scene:
    def __init__(self) -> None:
        self.sceneID="empty"
        self.elements=[]
        return
    
    def getElement(self, uid) -> object:
        for element in self.elements:
            if element.id == uid:
                return element
            
        return None
    
    def destroy(self) -> None:
        print("UNLOADING SCENE")
        for element in self.elements:
            element.destroy()
            del element

            

        return None

        
class Element:
    
    def __init__(self, element_type, source, size, position, **kwargs) -> None:
        parseArgs(self, element_type, source, size, position, **kwargs)

        #internal
        self.threads=[]


        #misc
        self.renderBevel=False
        self.bevelRadius=50
        self.down=False
        self.flag=0
        return
    
    def initialize(self):
        #loads all relevant assets into memory, must be done before rendering
        #allow to happen in background
        start=time.time()
        if self.type == "raster":
            element_base.raster.initialize(self)

        elif self.type == "text":
            element_base.text_element.initialize(self)
        
        elif self.type == "svg":
            element_base.svg_element.initalize(self)
        
        elif self.type == "video":
            element_base.video_element.initialize(self)
            
        elif self.type == "gradient":
            element_base.gradient_element.initialize(self)
            
        elif self.type == "volume":
            element_base.volume_element.initialize(self)

        #load scripts as finally (generalization untested)
        newScripts=[]
        for script in self.scripts:
            if type(script) == str:
                newScripts.append(Scripts.loadScript(script))
        self.scripts=newScripts

        print(f"INITIALIZED ELEMENT: {self.id}, taking: {int((time.time()-start)*1000)}ms")
        self.initialized=True

    def update(self):
        #TODO change update function to match initialize behavior (load from separate class file)
        #UPDATE BEHAVIOR IS MORE COMPLICATED THAN INIT, CONSIDER THREAD LOCKING!!!

        self.update_flag=False
        self.flashTrigger=False #test
        start=time.time()
        skipRaster=False

        #This code is unfixable
        #unfixable code vs the indomnitable human spirit
        if self.type == "raster":
            element_base.raster.update(self)

        elif self.type == "text":
            element_base.text_element.update(self)

        elif self.type == "volume":
            element_base.volume_element.update(self)
            pass

            

        else:
            #may need to explicitely call update functions even for non updating elements, nts
            pass

        if self.verbose: print(f"UPDATING ELEMENT: {self.id}, taking: {int(1000*(time.time()-start))}ms")
        return None
    
    def getFrame(self, render):

        #lazy loading
        try:
            frameIndex=int(render.f/self.interval)%self.numFrames
            if self.numFrames <= self.framesInMemory:
                return frameIndex
        except: return 0
        
        #if frames was not loaded, return frame 0 (frame 0 does not unload)
        try:
            if not self.assets["frames"][frameIndex]['loaded']: #DEBUG REMOVE TRUE, forces buffering on every frame
                #if buffering, load frames in thread, try to avoid
                print("Buffering: Attempting to load frames on demand")
                loadFrames(self, frameIndex, pygame, ThreadPoolExecutor)
                if not self.assets["frames"][frameIndex]['loaded']:
                    print("Load failed, returning to index 0")
                    return 0
                return frameIndex
        except: print("WARNING: Unexpected error occured while buffering"); return 0

        #check if overrun likely
        unloadedFrames=0
        for i in range(int(self.framesInMemory/self.interval)):
            checkFrame=(i+frameIndex)%self.numFrames #better wrap logic
            checkAsset=self.assets["frames"][checkFrame]['loaded']
            if not checkAsset: unloadedFrames+=1

        unloaded= unloadedFrames > 30 #TODO make variable

        #ensure thread safety
        safe=True
        for thread in self.threads:
            if thread['type'] == "loader":
                safe=False

        #spawn threads
        if safe and unloaded:
            thread=threading.Thread(target=loadFrames, args=(self, frameIndex, pygame, ThreadPoolExecutor,))
            thread.start()
            self.threads.append({"type" : "loader", "ref" : thread})
        
        
        return frameIndex
    
    def updateSourceRaster(self, source):
        #used to push new source from another thread
        name=source.replace("/", "").replace(":","").replace(".","").replace("https:","")
        path=f"assets/spotifyCache/{name}.jpeg"
        if (path != self.source) and not ("https:" in self.source):
            self.source=source
            self.update_flag=True

    def get_pos(self):
        #function wrapper to save time getting position after offsets
        return self.position[0]+self.offsetPosition[0]+self.systemOffset[0], self.position[1]+self.offsetPosition[1]+self.systemOffset[1]

    def raster(self):
        #returns render cache, if exists; else returns source reference, just shorthand
        return self.assets.get("renderCache", None)
    
    def destroy(self) -> None:
        def free(obj):
            #print(f"FREEING OBJ: {obj}")
            if type(obj) == type([]):
                for foo in obj:
                    free(foo)
                obj = None
            elif type(obj) == type({}):
                for key in obj:
                    if (type(obj[key]) != type([])) and (type(obj[key]) != type({})):
                        obj[key] = None
                    else:
                        free(obj[key])
                obj = None
                    
            else:
                foo = None
            obj = None
            return
        print(f"UNLOADING ELEMENT: {self.id}")
        self.safe=False
        #join all threads
        for thread in self.threads:
            thread['ref'].join()
        #unload all assets
        free(self.assets)
        #unload state machine
        self.stateMachine=None
        #unload globals
        free(self.globals)
        self.globals=None
        #unload scripts
        self.scripts=None #
        return None


