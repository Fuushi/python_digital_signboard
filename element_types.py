DEBUG_SHOW_EMITTERS=True

#imports
import pygame
from imgLib import *
import json, re, time, requests, gc

#this file contains update and initialization functions for all element classes

class element_base:
    class volume_element:

        class Particle:
            def __init__(self, pos=[0,0], vel=[0,0]) -> None:
                #TODO build particle object
                self.pos=pos
                self.particle_size=5
                self.date_of_birth=0
                self.lifespan=30 #(integrate range at creation time)
                self.velocity=vel
                
                return
            
        class Emitter:
            def __init__(self, pos=[0,0], rate=1, rate_variance=0):
                self.pos=pos
                self.rate=rate
                self.rate_variance=0
                self.last_spawn=0
            
            
            

        def initialize(self) -> None:
            def render(screen, element, render):
                #render

                #iterate through particles, and draw texture (or geometry) to screen

                for particle in self.particles:
                    #calc screenspace position
                    x=self.position[0]+particle.pos[0]
                    y=self.position[1]+particle.pos[1]
                    if element.tex:
                        screen.blit(element.tex, (x,y))
                    else:
                        pygame.draw.circle(screen, (0,0,255), (x,y), 2)

                if DEBUG_SHOW_EMITTERS:
                    for emitter in element.emitters:
                        pygame.draw.circle(screen, (255,0,0), emitter.pos, 5)

                return
            self.draw=render
            self.spawnEmitter=element_base.volume_element.spawnEmitter

            #initialize

            #LITERALS (get from pass in)
            PARTICLE_SIZE=5 #px
            PARTICLE_SIZE_RANGE=0
            MAX_INTERACTIONS=50
            PARTICLE_LIFESPAN=30
            PARTICLE_LIFESPAN_RANDOMNESS=15
            PARTICLE_ALGORITHM="RAY"
            POSITION=(0,0)

            if self.source:
                #bake particle textures
                try: img = pygame.image.load(self.source)
                except: raise FileNotFoundError#img=pygame.image.load("assets/background1.jpg")

                tex=pygame.transform.smoothscale(img, (PARTICLE_SIZE,PARTICLE_SIZE))
            else:
                tex=None

            self.tex=tex

            self.particle_size=5
            self.particle_size_range=0
            self.particle_textures=[tex]
            self.max_entities=self.max_entities
            self.max_frame_interactions=50
            self.particle_lifespan=30
            self.particle_lifespan_range=15
            self.particle_algorithm='comet'
            self.domain=self.size
            self.position=(0,0)

            self.particles=[]
            self.emitters=[]




        def update(self):
            if (time.time()-self.PARTICLE_UPDATE_TIME)*1000 < 16: return

            now=time.time() 
        
            #loop through emmiters
            for emitter in self.emitters:
                ## decide
                
                if (now - emitter.last_spawn) > emitter.rate:


                    ##spawn particle
                    SPEED=35
                    pos=[emitter.pos[0],emitter.pos[1]]
                    xVec=(0.5-random.random())
                    yVec=math.sqrt((0.5**2)-(xVec**2)) * random.choice((-1,1))
                    self.particles.append(
                        element_base.volume_element.Particle(pos=pos, vel=[xVec*SPEED,yVec*SPEED])
                    )

                    emitter.last_spawn=now

            if not self.particles: return



            #enforce particle cap
            element_base.volume_element.algorithms.enforceParticleCap(self)

            #update particle system
            element_base.volume_element.algorithms.softball(self)

            #enforce bounds
            element_base.volume_element.algorithms.enforeBounds(self)

            
            self.PARTICLE_UPDATE_TIME=now
            return
        
        
        def killAllParticles(self):

            return
        
        def spawnEmitter(self, pos, rate=1, rate_variance=0) -> object:
            emitter=element_base.volume_element.Emitter(pos=pos, rate=rate, rate_variance=rate_variance)
            self.emitters.append(emitter)
            return emitter
        
        class algorithms:
            def comet(self):
                #COMET algorithm
                for particle in self.particles:
                    particle.pos[0] = particle.pos[0] + particle.velocity[0]
                    particle.pos[1] = particle.pos[1] + particle.velocity[1]
                    pass

            def softball(self):
                #SOFTBALL algorithm
                for particle in self.particles:
                    #calculate velocity
                    particle.velocity[0] = particle.velocity[0]*0.9
                    particle.velocity[1] = particle.velocity[1]*0.9

                    #integrate position
                    particle.pos[0] = particle.pos[0] + particle.velocity[0]
                    particle.pos[1] = particle.pos[1] + particle.velocity[1]

            def enforeBounds(self):
                for particle in self.particles:
                    if particle.pos[0] > self.domain[0] or particle.pos[1] > self.domain[1] or particle.pos[0] < 0 or particle.pos[1] < 0:
                        self.particles.remove(particle)

            def enforceParticleCap(self):
                if len(self.particles) > self.max_entities:
                    to_remove=self.particles[::-1][self.max_entities-1:]
                    for particle in to_remove:
                        self.particles.remove(particle)
                        del particle
                    to_remove=None

            def cometCtypes(self):
                #TODO implement
                return

            
        



    class gradient_element:
        def initialize(self) -> None:
            def render(screen, element, render):
                screen.blit(element.assets["gradient"], element.position, special_flags=element.flag)
                return
            self.draw=render
            #TODO clean up variables
            drawGradient(self)

        def update(self) -> None:
            #gradient does not have an update function, return
            return
        



    class video_element:
        def initialize(self) -> None:
            def render(screen, element, render):
                #for data in element.assets.get('frames', []):

                #get frame
                frameNum=element.getFrame(render)
                frameRef=element.assets["frames"][frameNum]['ref']

                #blit & mask
                if element.maskPoly:
                    t1=time.time()
                    # Create a mask surface with the same size as the frame
                    mask_surface = pygame.Surface(element.size).convert_alpha()
                    mask_surface.fill((0, 0, 0, 0))  # Fill with transparent color

                    # Draw the polygon mask on the mask surface
                    mask_surface=element.assets.get(f"masks{str(element.maskPoly)}", None)
                    if not mask_surface:
                        #TODO ensure cleanup on mask variable
                        mask_surface = pygame.Surface(element.size).convert_alpha()
                        mask_surface.fill((0, 0, 0, 0))  # Fill with transparent color
                        pygame.draw.polygon(mask_surface, (255, 255, 255, 255), element.maskPoly)
                        element.assets[f"masks{str(element.maskPoly)}"]=mask_surface

                    #print(f"DEBUG: drawing mask layer, took {int(1000*(time.time()-t1))}ms"); t1=time.time()

                    # Apply the mask to the frame reference
                    masked_frame = pygame.Surface(element.size).convert_alpha()
                    masked_frame.blit(frameRef, (0, 0))
                    masked_frame.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                    #print(f"DEBUG: applying mask layer, took {int(1000*(time.time()-t1))}ms"); t1=time.time()

                    # Blit the masked frame onto the screen
                    screen.blit(masked_frame, element.get_pos())
                    #print(f"DEBUG: screen blit took {int(1000*(time.time()-t1))}ms"); t1=time.time()
                else:
                    # If no mask polygon is provided, simply blit the frame onto the screen
                    screen.blit(frameRef, element.get_pos())

                return
            
            self.draw=render
            ##check filetype
            if self.source.split(".")[::-1][0] == "gif":
                paths=loadAndCache.gif(self.source)
                self.assets["framesRaw"]=[]
                self.assets["frames"]=[]
                i=0
                for path in paths:
                    img=pygame.image.load(path)
                    self.assets["framesRaw"].append(img)
                    self.assets["frames"].append(self.assets["frames"].append(
                            {
                                "ref" : pygame.transform.smoothscale(img, (self.size[0]+self.offsetScale[0],self.size[1]+self.offsetScale[1])),
                                "loaded" : True
                            }
                        ))
                    i+=1
                self.numFrames=i

            elif self.source.split(".")[::-1][0] == "mp4":
                #TODO mp4 handler
                start=time.time()
                paths=loadAndCache.mp4(self.source)
                print(f"DEBUG: First time video import took {int(1000*(time.time()-start))}ms"); start=time.time()
                self.assets["framesRaw"]=[]
                self.assets["frames"]=[]
                i=0
                for path in paths:
                    try:
                        if i < self.framesInMemory: img=pygame.image.load(path)
                        else: img=None
                    except FileNotFoundError: continue

                    frameDict={"ref" : img, "loaded" : (i<self.framesInMemory)}

                    self.assets["framesRaw"].append(frameDict)

                    if not img: #bad
                        self.assets["frames"].append(frameDict)
                        i+=1
                        continue

                    if self.size == img.get_size():
                        #uses same ref to save memory while supporting legacy code
                        self.assets["frames"].append(frameDict)
                    else:
                        self.assets["frames"].append(
                            {
                                "ref" : pygame.transform.smoothscale(img, (self.size[0]+self.offsetScale[0],self.size[1]+self.offsetScale[1])),
                                "loaded" : True
                            }
                        )

                    #print(f"DEBUG: frame processing took {int(1000*(time.time()-start))}ms"); start=time.time()
                    i+=1
                self.numFrames=i
                return

            def update(self) -> None:
                #video does not have an update function, return
                return
            
    class model:
        def initialize(self) -> None:
            def render(screen, element, render):

                return
            self.draw=render

        def render(self) -> None:
            return


            
    class svg_element:
        def initalize(self) -> None:
            def render(screen, element, render):
                i2=0
                for data in element.assets[element.source].get('lines', []):
                
                    for i in range(len(data['points'])-1):
                        pygame.draw.line(
                            screen, 
                            data['color'], 
                            (
                                data['points'][i][0]+element.offsetPosition[0]+element.assets[element.source]['lines'][i2]["offsets"][i][0]+element.position[0], 
                                data['points'][i][1]+element.offsetPosition[1]+element.assets[element.source]['lines'][i2]["offsets"][i][1]+element.position[1]
                            ), 
                            (
                                data['points'][i+1][0]+element.offsetPosition[0]+element.assets[element.source]['lines'][i2]["offsets"][i+1][0]+element.position[0],
                                data['points'][i+1][1]+element.offsetPosition[1]+element.assets[element.source]['lines'][i2]["offsets"][i+1][1]+element.position[1]
                            ), 
                            data['thickness'])
                        
                        #print(element.assets[element.source]['lines'][0]["offsets"])
                    i2+=1
                for data in element.assets[element.source].get("polys", []):
                    pointsArr=[]
                    for i in range(len(data['points'])-1):
                        pointsArr.append(
                            (
                                data['points'][i][0]+element.offsetPosition[0]+element.assets[element.source]['polys'][0]["offsets"][i][0], 
                                data['points'][i][1]+element.offsetPosition[1]+element.assets[element.source]['polys'][0]["offsets"][i][1]
                            )
                        )
                    pygame.draw.polygon(
                        surface=screen, 
                        color=data['color'], 
                        points=pointsArr,
                        width=data.get("thickness", 0)
                    )

                for data in element.assets[element.source].get("circles", []):

                    for point in data['points']:

                        pygame.draw.circle(surface=screen, color=data['color'], center=(point[0],point[1]),radius=data['radius'])

                return
            self.draw=render
            ##not class constructor ((inherits parent properties))
            with open(self.source, "r") as fp: data=fp.read()
            decode = json.loads(data)
            self.assets[self.source]=decode
            #no render cache needed

        def update(self) -> None:
            #svg does not have an update function, return
            return

    class text_element:
        def initialize(self) -> None:
            def render(screen, element, render):
                drop=element.assets.get("dropShadow", None)
                if drop:
                    screen.blit(drop, (element.get_pos()[0]-10, element.get_pos()[1]-10), special_flags=pygame.BLEND_RGB_SUB)

                screen.blit(element.raster(), element.get_pos())
                return
            
            self.draw=render
            #text handler
            if self.globals: globals=self.globals
            else: globals={}

            #fString interpreter
            if self.text_template: matches = re.findall(r'\{(.*?)\}', self.text_template)
            else: matches = re.findall(r'\{(.*?)\}', self.text)

            for match in matches: self.text=self.text_template.replace(("{"+f"{match}"+"}"), globals.get(match, "@keyError"))

            font = pygame.font.SysFont(self.font, self.font_size)
            canvas = font.render(self.text, True, self.text_color)
            self.assets["raw"] = canvas
            self.assets["renderCache"] = canvas
            try:
                if self.stateMachine.dropShadow:
                    shadowTexture=shaders.gaussV3(canvas, 5, 5, (255/16))
                    shadowTexture=shaders.invert(shadowTexture)
                    shadowTexture=shaders.invert(shadowTexture)
                    shaders.brighten(shadowTexture, 100)
                    self.assets["dropShadow"]=shadowTexture
            except AttributeError: pass

            #once rendered, commit rendered text to bank
            self.rendered_text=self.text

            return
        
        def update(self) -> None:
            #requires custom behavior, assign at runtime
            if (self.text != self.rendered_text) or ("{" in self.text) or self.globals or self.runEveryFrame:
                
                if self.text_template: stringManupulation.fStringInterpreter(self)

                if self.text != self.rendered_text:

                    canvas=shaders.textRender(self.text, self.font, self.font_size, self.text_color, pygame)
                    self.assets["raw"]=canvas
                    self.assets["renderCache"] = canvas

                    #dropshadown handling
                    try:
                        if self.stateMachine.dropShadow:
                            shadowTexture=shaders.gaussV3(canvas, 5, 5, (255/16))
                            shadowTexture=shaders.invert(shadowTexture)
                            shadowTexture=shaders.invert(shadowTexture)
                            shaders.darken(shadowTexture, 90)
                            self.assets["dropShadow"]=shadowTexture
                    except AttributeError: pass

                    self.rendered_text=self.text
                
                else:
                    pass #skiprender
            return

    class raster:
        #INITALIZE CALLS ARE NOT A BUILTIN CONSTRUCTOR, THIS IS CUSTOM BEHAVIOR, INHERITS PARENTS ATTRIBUTES
        def initialize(self) -> None:
            def render(screen, element, render):
                drop=element.assets.get("dropShadow", None)
                if drop:
                    screen.blit(drop, (element.get_pos()[0]-10, element.get_pos()[1]-10), special_flags=pygame.BLEND_RGB_SUB)

                screen.blit(element.raster(), element.get_pos())
                return
            
            self.draw=render
            try: img = pygame.image.load(self.source)
            except: img=pygame.image.load("assets/background1.jpg")

            if self.renderBevel:
                img=shaders.bevel(img, radius=self.bevelRadius, pygame=pygame)
                pass

            if not self.crop:
                resizedImage = pygame.transform.smoothscale(img, self.size)
            else:
                aspect_ratio = img.get_width() / img.get_height()
                target_aspect_ratio = self.size[0] / self.size[1]

                # Calculate crop dimensions to maintain aspect ratio
                if aspect_ratio > target_aspect_ratio:
                    # Crop width
                    new_width = int(img.get_height() * target_aspect_ratio)
                    cropped_image = img.subsurface(((img.get_width() - new_width) // 2, 0, new_width, img.get_height()))
                else:
                    # Crop height
                    new_height = int(img.get_width() / target_aspect_ratio)
                    cropped_image = img.subsurface((0, (img.get_height() - new_height) // 2, img.get_width(), new_height))

                # Resize the cropped image to fit the target size
                resizedImage = pygame.transform.smoothscale(cropped_image, self.size)

            self.assets["source"] = img
            self.assets["renderCache"] = resizedImage

            #swaps string arg for function definition

        
        def update(self):
            skipRaster=False
            if "http" in self.source: #source in cloud
                #detect if source is local or not
                name=self.source.replace("/", "").replace(":","").replace(".","").replace("https:","")
                #print(name.replace(".",""), "=", self.rendered_text.replace(".",""))
                if name.replace(".","") != self.rendered_text.replace(".",""): #quick optimization
                    if not os.path.exists(f"assets/spotifyCache/{name}.jpeg"):
                        try:
                            response = requests.get(self.source)
                        except:
                            print(f"Get error: {self.source}") #this will crash
                            raise FileNotFoundError
                        if response.status_code == 200:
                            with open(f"assets/spotifyCache/{name}.jpeg", 'wb') as f:
                                f.write(response.content)
                                print(f"Downloaded {name}")
                            
                            del response
                        else:
                            print("Failed to download image.")
                            name="background1.jpg"  
                else:
                    #print("DEBUG: already rendered, skipping download")
                    skipRaster=True
                self.source=f"assets/spotifyCache/{name}.jpeg"
                self.rendered_text=f"assets/spotifyCache/{name}.jpeg"
            
            else:
                if not self.rendered_text:
                    self.rendered_text=self.source

                elif self.source==self.rendered_text:
                    skipRaster=True
                
                self.rendered_text=self.source
                        
                ##

        
            if not skipRaster:
                #raster
                try: img = pygame.image.load(self.source)
                except:
                    self.source="assets/background1.jpg"
                    img = pygame.image.load(self.source)
                    
                #TODO make work with scaling properly
                if self.renderBevel: img=shaders.bevel(img, radius=self.bevelRadius, pygame=pygame)


                if not self.crop:
                    resizedImage = pygame.transform.smoothscale(img, self.size)
                else:
                    aspect_ratio = img.get_width() / img.get_height()
                    target_aspect_ratio = self.size[0] / self.size[1]
                    if aspect_ratio > target_aspect_ratio:
                        # Crop width
                        new_width = int(img.get_height() * target_aspect_ratio)
                        cropped_image = img.subsurface(((img.get_width() - new_width) // 2, 0, new_width, img.get_height()))
                    else:
                        # Crop height
                        new_height = int(img.get_width() / target_aspect_ratio)
                        cropped_image = img.subsurface((0, (img.get_height() - new_height) // 2, img.get_width(), new_height))

                    # Resize the cropped image to fit the target size
                    resizedImage = pygame.transform.smoothscale(cropped_image, self.size)
                    

                self.assets["source"] = img
                self.assets["renderCache"] = resizedImage

            return
        

class StateMachine:
    def __init__(self) -> None:
        #stores miscelanious data for scripting
        return

def parseArgs(self, element_type, source, size, position, **kwargs) -> None:
    #inherits parent attributes, only used as shorthand

    kwargs=kwargs['kwargs']
    #print(kwargs)
    self.type=element_type
    self.id=kwargs.get("id",str(int(random.random()*1000000)))
    self.globals=None
    self.source=source
    self.size=size
    self.position=position
    self.stateMachine=StateMachine()
    self.runEveryFrame=False
    self.flag=False
    self.flashTrigger=False
    self.maskPoly=kwargs.get("maskPoly", None)
    self.numFrames=0
    self.frameMemoryOffset=0
    self.allowThreadedUpdates=True
    self.framesInMemory=kwargs.get("framesInMemory", 100)
    self.interval=kwargs.get("interval", 1)
    self.text=kwargs.get("text", None)
    self.text_template=kwargs.get("text_template", None)
    self.rendered_text=""
    self.font=kwargs.get("font", None)
    self.font_size=kwargs.get("font_size", None)
    self.text_color=kwargs.get("text_color", None)
    self.colors=kwargs.get("colors", None)
    self.method=kwargs.get("method", None) #LEGACY
    self.offsetPosition=kwargs.get("offsetPosition", [0, 0])
    self.offsetScale=kwargs.get("offsetScale", [0, 0])
    self.offsetRotation=kwargs.get("offsetRotation", 0)
    self.zoffset=kwargs.get("zoffset", 0)
    self.render=True
    self.initialized=False
    self.update_flag=False#TODO add the internal update flag for changing text
    self.assets={}
    self.verbose=kwargs.get("verbose", True)
    self.scripts=kwargs.get("scripts", [])
    self.crop=kwargs.get("crop", False)
    self.lastUpdate=time.time()
    self.max_entities=kwargs.get("max_entities", 50)
    self.frameRate=30
    self.PARTICLE_UPDATE_TIME=time.time()
    if platform.system()!="Windows" : self.systemOffset=(0,5)
    else: self.systemOffset=(0,0)
    return