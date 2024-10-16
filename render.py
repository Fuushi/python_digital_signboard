from scripts import *
from presets import *
from classes import *
import os, time, json, sys, platform
import pygame
from logger import logger
from element_types import element_base
import gc

class renderObj:
    def __init__(self) -> None:
        #get configurator
        with open("config.json", 'r') as fp: self.config=json.loads(fp.read())

        #init variables
        self.presetID=None
        self.uptime=time.time()
        self.suspend=False
        self.globals={"raw" : "0", "song" : "Not playing...", "clock" : "00:00:00"}
        self.createEmptyScene()
        self.mouse_pos = (0,0)
        self.window = {"x" : 1280, "y" : 400}
        self.f=0
        self.processReady=True
        self.threaded=True
        self.verbose=platform.system() == "Windows"
        self.dead=False
        self.playing=True
        self.pb=None #commit playback
        self.pause=False
        self.logger=logger()
        self.debug_display=False
        self.resetPROC=False
        self.resetBEHAVIOR=False
        
        return
    
    def loadSceneFromFile(self, id="home") -> object: 
        #this function is high maitenence because i am not making a decorator for this

        #ensure memory safety
        self.suspend=True
        time.sleep(0.16*2)
        self.scene.destroy()
        self.scene = None

        if id=="home": scene = Presets.home(self); self.presetID="home"

        elif id=="homeV2": scene = Presets.homeV2(self); self.presetID="homeV2"
        elif id=="debug": scene = Presets.debug(self); self.presetID="debug"
        elif id=="lowPowerMode": scene = Presets.lowPowerMode(self); self.presetID="lowPowerMode"
        elif id=="bangboo": scene=Presets.bangboo(self); self.presetID="bangboo"

        else: scene = Presets.empty(self); self.presetID="empty"

        #unlock
        time.sleep(0.16*2)
        self.suspend=False
        
        ##create elements with parameters from file
        return scene
    
    def createEmptyScene(self) -> object:
        scene = Scene()
        self.scene=scene
        return scene
    
    def unloadScene(self) -> object:
        self.scene.destroy()
    
    
    def createElement(self, element_type, source, size, position, **kwargs) -> dict:
        ref = Element(
            element_type=element_type,
            source=source,
            size=size, #immutable
            position=position, #mutable, use offsets when possible
            kwargs=kwargs
        )
        #print(kwargs)
        self.scene.elements.append(ref)
        return ref
    
    def render(self, screen):
        if not self.scene: return
        screen.fill((0,0,0))
        for element in self.scene.elements:
            if element.initialized and element.render:

                objects.updateAnimationInlineV2(element, self)
                    
                element.lastUpdate=time.time()

                element.draw(screen, element, self)

        return
    
    def debugHUD(self, screen):
        #tracked objects
        trackers=[Element, Scene, StateMachine, logger, functionWrapper]

        lines=[f"DEBUG MENU:::"]
        #text
        

        for obj in trackers:
            lines.append(f"{str(obj)}:::{count_instances(obj)}")
        
        pygame.draw.rect(screen, (0,0,0), (30,30, 300, 300))
        i=0
        for line in lines:
            ref=shaders.textRenderFast(line, "arial", 15, (255,255,255), pygame)
            screen.blit(ref, (30,30+(15*i)))
            i+=1
        return



class renderThread:
    def __init__(self, render) -> None:
        pygame.init()

        window = {"x" : 1280, "y" : 400}

        screen = pygame.display.set_mode((window['x'], window['y']), vsync=True)
        pygame.display.set_caption("Spotify Deck")
        
        #pass screen to render
        render._pygame=pygame
        render._screen=screen

        clock = pygame.time.Clock()
        f=0
        while True:
            render.click=False
            frame_start = time.time()
            render.globals["f"] = str(render.f)
            render.states={} #use for transfering arbitrary Data (DEPRECIATED)
            
            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #exit clause
                    render.dead=True
                    render.logger.log("EXIT FROM RENDER", {"frame" : f})
                    return
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        render.click=True

                        #debug
                        if not render.debug_display: render.debug_display=True
                        else: render.debug_display=False

                    if event.button == 2:
                        print("RESETTING THREADS")
                        render.resetPROC=True
                        render.resetBEHAVIOR=True

            #power save mode (DEPRECIATE)
            if render.pause:
                pygame.display.flip()
                pygame.display.update()
                render.processReady=True
                f += 1
                render.f+=1
                clock.tick(60)
                continue
                
            #peripherals
            mx, my = pygame.mouse.get_pos()
            render.mouse_pos=(mx, my)

            #render
            if not render.suspend: render.render(screen)
            else: pygame.draw.circle(screen, (255,0,0), (1265,15), 10)

            #DEBUG TABLES
            if render.debug_display: render.debugHUD(screen)
            #debug lag marker
            if render.verbose: pygame.draw.circle(screen, (255,255,255), (mx, my), 3)
            if render.dead: return

            #calculate frametime
            frame_end = time.time()
            if int(1000*(time.time()-frame_start)) > 1000*(1/60):
                if render.verbose: print(f"Lag Spike detected, frametime: {int(1000*(frame_end-frame_start))}ms")
                if render.verbose: pygame.draw.circle(screen, (255,0,0), (1265,15), 10)

            #flip the canvas
            pygame.display.flip()
            pygame.display.update()
            f += 1
            render.f+=1
            clock.tick(60)
        return
    
def count_instances(cls):
    return sum(1 for obj in gc.get_objects() if isinstance(obj, cls))