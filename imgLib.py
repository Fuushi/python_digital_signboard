from PIL import Image
import os, sys
import cv2
import time
import numpy as np
import math
import platform
import random

class comp:
    def hsv_to_rgb(h, s, v):
        # Convert HSV from 0-255 to 0-1 range
        h = h / 255.0 * 360
        s = s / 255.0
        v = v / 255.0
        
        # Calculate RGB
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        # Convert RGB from 0-1 to 0-255 range
        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)
        
        return r, g, b
    
    def rgb_to_hsv(r, g, b):
        # Convert RGB from 0-255 range to 0-1 range
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        
        # Find max and min RGB values
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        delta = cmax - cmin
        
        # Calculate Hue
        if delta == 0:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        else:
            h = (60 * ((r - g) / delta) + 240) % 360
        
        # Calculate Saturation
        if cmax == 0:
            s = 0
        else:
            s = (delta / cmax) * 255
        
        # Calculate Value
        v = cmax * 255
        
        # Convert Hue to 0-255 range
        h = int(h / 360 * 255)
        
        # Return HSV values in 8-bit range (0-255)
        return int(h), int(s), int(v)




class loadAndCache:
    def gif(path):
        paths=[]

        try:
            im = Image.open( path )
        except IOError:
            print ("Cant load", path)
            sys.exit(1)

        i = 0

        try:
            while True:
                uid=path.split(".")[::-1][0].replace("\\", "") #uid is a bad variable name
                fileName=path.split(".")[0].replace("\\","")
                framePath=f'assets/frames/{fileName}{uid}'+str(i)+'.jpg'
                if os.path.exists(framePath):
                    paths.append(framePath)
                    i+=1
                    continue
                else:
                    pass
                background = Image.new("RGB", im.size, (255, 255, 255))
                background.paste(im)
                background.save(framePath, 'JPEG', quality=80)

                paths.append(framePath)

                i += 1
                im.seek( im.tell() + 1 )

        except EOFError:
            pass # end of sequence

        return paths
    
    def mp4(path):
        #framePaths.append(framePath)
        # Open video file
        t=time.time()
        checkpointID = 0
        

        cap = cv2.VideoCapture(path)
        i = 0
        framePaths=[]

        #lazy load check
        uid=path.split(".")[::-1][0].replace("\\", "") #uid is a bad variable name
        fileName=path.split(".")[0].replace("\\","").replace("assets", "")
        framePath=(f'assets/frames/{fileName}{uid}'+str(i)+'.jpg').replace("mp4", "-")
        if os.path.exists(framePath):
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
            #print(f"frame count: {frame_count}")

            for i in range(frame_count):
                #print(i)
                uid=path.split(".")[::-1][0].replace("\\", "") #uid is a bad variable name
                fileName=path.split(".")[0].replace("\\","").replace("assets", "")
                framePath=(f'assets/frames/{fileName}{uid}'+str(i)+'.jpg').replace("mp4", "-")
                framePaths.append(framePath)

            

            return framePaths



        # Loop through video frames
        while cap.isOpened():
            #calculate metadata
            uid=path.split(".")[::-1][0].replace("\\", "") #uid is a bad variable name
            fileName=path.split(".")[0].replace("\\","").replace("assets", "")
            framePath=(f'assets/frames/{fileName}{uid}'+str(i)+'.jpg').replace("mp4", "-")
            framePaths.append(framePath)
            #check if already converted
            if os.path.exists(framePath):
                
                i += 1
                continue
            
            #extract frame data
            ret, frame = cap.read()
            if not ret:
                break



            #convert
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            pil_image.save(framePath)

            # Save frame as JPEG
            i += 1

        
        cap.release()

        #debug (force buffering here)
        #time.sleep(0.3)
        
        return framePaths
    
class shaders:
    def bevel(img, radius=10, pygame=None):
        if not pygame: import pygame

        size=img.get_size()
        
        mask=pygame.Surface(size, pygame.SRCALPHA)  # Create a surface with an alpha channel
        mask.fill((0, 0, 0, 255))  # Fill with transparent black
        
        poly=[
            (0,radius),
            (0,size[1]-radius),
            (radius, size[1]),
            (size[0]-radius, size[1]),
            (size[0], size[1]-radius),
            (size[0], radius),
            (size[0]-radius, 0),
            (radius, 0),
            (0,radius)
        ]

        alphaChannel=(0,0,0,0)

        pygame.draw.polygon(
            mask,
            alphaChannel,
            poly
        )

        pygame.draw.circle(mask, alphaChannel, (radius, radius), radius)
        pygame.draw.circle(mask, alphaChannel, (size[0]-radius, radius), radius)
        pygame.draw.circle(mask, alphaChannel, (radius, size[1]-radius), radius)
        pygame.draw.circle(mask, alphaChannel, (size[0]-radius, size[1]-radius), radius)

        # Blit the mask onto the img_with_bevel surface with appropriate blending mode
        img_with_bevel = pygame.Surface(size, pygame.SRCALPHA)
        img_with_bevel.blit(img, (0, 0))
        img_with_bevel.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)  # Use BLEND_RGBA_MULT for blending

        return img_with_bevel
    
    def dropShadow(img, radius, pygame=None):
        if not pygame: import pygame #only for intellisense
        import cv2
        #create surface of imgsize + diameter
        surface=pygame.Surface((img.get_size()[0]+2*radius,img.get_size()[1]+2*radius)).convert_alpha()
        surface.fill(0,0,0,0)
        #blit base image onto surface
        surface.blit(img (radius,radius))

        #gaussian blur (this will be slow)
        shaders.gauss(img, radius)
        
        #turn all rgb values to black, conserving alpha
        for x in range(surface.get_width()):
            for y in range(surface.get_height()):
                r, g, b, a = surface.get_at((x, y))
                surface.set_at((x, y), (0, 0, 0, a))  # Setting RGB to black, alpha unchanged

        #blit original surface back ontop
        surface.blit(img, (radius,radius))

        return surface

    
    def lazyGauss(img, scalar, pygame=None):
        if not pygame: import pygame
        ##
        img2 = pygame.transform.smoothscale(img, (int(img.get_size()[0]/scalar), int(img.get_size()[1]/scalar)))

        img = pygame.transform.smoothscale(img2, (img.get_size()))
        

        return img
    
    def textRenderFast(text, font, font_size, color, pygame=None):
        #LEGACY, used as fallback for composite (now textRender)
        if not pygame: import pygame
        font = pygame.font.SysFont(font, font_size)

        canvas = font.render(
            text, True, color
        )

        return canvas
    
    def textRender(text, base_font, font_size, color, pygame=None):
        #composite render'
        if not pygame: import pygame #for intellisense

        segments = stringManupulation.unicode_segregator(text)
        

        if len(segments) >= 2 or not stringManupulation.is_ascii(segments[0]):
            if platform.system() == "Windows":
                font_path = 'E:/code/fonts/NotoSansJP-Bold.ttf' #unicode font
            else:
                font_path = "NotoSansJP-Bold.ttf"
            asciiFont=pygame.font.SysFont(base_font, font_size)
            unicodeFont = pygame.font.Font(font_path, font_size - 3) #3 is guess

        else:
            # if extra fonts not neede, use legacy as fallback
            return shaders.textRenderFast(text, base_font, font_size, color, pygame)

        canvas=[]
        for segment in segments:

            if stringManupulation.is_ascii(segment):

                canvas.append((asciiFont.render(segment, True, color), False))

            else:

                canvas.append((unicodeFont.render(segment, True, color), True))

        height=canvas[0][0].get_size()[1]

        width=0
        for can in canvas: width += can[0].get_size()[0]

        surface=pygame.Surface((width, height)).convert_alpha()
        surface.fill((0,0,0,0))

        offset=0
        for can in canvas:
            surface.blit(can[0], (offset,0-(8*can[1])))
            offset+=can[0].get_size()[0]

        return surface 
    
    def gIter(canvas, img, radius, alpha, pygame=None):
        if not pygame: import pygame
        flag=0
        img.set_alpha(alpha)
        canvas.blit(img, (radius+int(random.random()*radius),radius+int(random.random()*radius)), special_flags=flag)
        canvas.blit(img, ((radius*2)+int(random.random()*radius),radius+int(random.random()*radius)), special_flags=flag)
        canvas.blit(img, (radius+int(random.random()*radius), (radius*2)+int(random.random()*radius)), special_flags=flag)
        canvas.blit(img, (radius*2+int(random.random()*radius),radius*2+int(random.random()*radius)), special_flags=flag)

        return img

    def gaussV3(img_ref, iterations : int, radius : int, alpha : int, pygame=None):
        if not pygame: import pygame

        img=img_ref.copy()
        
        #expand canvas
        t1=time.time()
        canvas=pygame.Surface((img.get_size()[0]+(4*radius), img.get_size()[1]+(4*radius))).convert_alpha()
        canvas.fill((0,0,0,0))
        canvas.blit(img, (radius*2, radius*2))
        #print(f"Created Canvas, taking; {int(1000*(time.time()-t1))}ms")


        for i in range(iterations):
            shaders.gIter(canvas, img, radius, alpha, pygame)

            img.blit(canvas, (0-radius, 0-radius))

        return canvas
    
    def invert(img, pygame=None):
        #this function is tailored to drop shadows, may encounter issues in other uses
        if not pygame: import pygame

        noAlpha=shaders.removeAlpha(img)

        surface = pygame.Surface(noAlpha.get_size())
        surface.fill((255,255,255))

        surface.blit(noAlpha, (0,0), special_flags=pygame.BLEND_RGB_SUB)

        return surface

    def removeAlpha(img, pygame=None):
        if not pygame: import pygame

        surface = pygame.Surface(img.get_size())
        surface.fill((0,0,0))

        surface.blit(img, (0,0))

        return surface
    
    def brighten(img, factor, pygame=None):
        if not pygame: import pygame

        surface = pygame.Surface(img.get_size())
        surface.fill((factor,factor,factor))

        img.blit(surface, (0,0), special_flags=pygame.BLEND_RGB_ADD)

    def darken(img, factor, pygame=None):
        if not pygame: import pygame

        surface = pygame.Surface(img.get_size())
        surface.fill((factor,factor,factor))

        img.blit(surface, (0,0), special_flags=pygame.BLEND_RGB_SUB)




def select(arr, index, n) -> list:
    #returns unloaded frames from an array
    indices=[]
    for i in range(len(arr)):
        indices.append(i)

    selected_indices = []
    for _ in range(n):
        current_index = (index + _) % len(arr)
        selected_indices.append(indices[current_index])
    if len(selected_indices) > len(arr):
        return selected_indices[:len(arr)]
    return selected_indices

def load(element, frameIndice, paths, pygame=None):
        if not pygame:
            import pygame
        try:
            element.assets["frames"][frameIndice] = {
                "ref" : pygame.image.load(
                    paths[frameIndice]
                ),
                "loaded" : True
            }
        except:
            element.assets["frames"][frameIndice] = {
                "ref" : pygame.image.load(
                    paths[0]
                ),
                "loaded" : True}

#calls frame load function (wrapper)
def load_frame(element, frameIndice, paths, pygame):
    load(element, frameIndice, paths, pygame)

#spawns thread pool
def load_frames(element, frameIndices, paths, pygame, ThreadPoolExecutor) -> int:
    n=0
    with ThreadPoolExecutor(max_workers=4) as executor:  # Adjust max_workers as needed
        futures = []
        for frameIndice in frameIndices:
            if not element.assets["frames"][frameIndice]['loaded']:
                futures.append(executor.submit(load_frame, element, frameIndice, paths, pygame))
                n+=1      
    # Wait for all tasks to complete
    for future in futures:
        future.result()

    return n

def loadFrames(element, frameIndex, pygame, ThreadPoolExecutor):
    t2=time.time()

    #get unloaded frame indices
    frameIndices=select(element.assets["frames"], frameIndex, int(element.framesInMemory/element.interval))

    #get paths for all frames
    paths=loadAndCache.mp4(element.source)

    # load frames to element
    framesLoaded=load_frames(element, frameIndices, paths, pygame, ThreadPoolExecutor)

    #unload unneeded frames
    arr=[]
    for i in range(element.numFrames):
        arr.append(i)
    #remove known indices
    for i in frameIndices:
        arr.remove(i)

    #remove 0
    try: arr.remove(0)
    except: pass

    for i in arr:
        element.assets["frames"][i]={
            "ref" : None,
            "loaded" : False
        } 

    if element.verbose: print(f"Loaded {framesLoaded} frames in {int(1000*(time.time()-t2))}ms")



def drawGradient(element,pygame=None) -> None:
    if not pygame: import pygame; pygame.init()

    size = element.size
    position = element.position
    color1 = element.colors[1]
    color2 = element.colors[0]

    gradient_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()

    for y in range(size[1]):
        # Calculate color interpolation
        r = int(color1[0] + (color2[0] - color1[0]) * (y / size[1]))
        g = int(color1[1] + (color2[1] - color1[1]) * (y / size[1]))
        b = int(color1[2] + (color2[2] - color1[2]) * (y / size[1]))
        alpha = min(int(color1[3] + (color2[3] - color1[3]) * (y / size[1])*1.5), 255) #*2 force darken

        # Draw line with interpolated color and alpha
        pygame.draw.line(gradient_surface, (r, g, b, alpha), (0, y), (size[0], y))

    element.assets["gradient"] = gradient_surface

    return

class stringManupulation:

    def unicode_segregator(string): #separates a string into segments of unicode and non-unicode for rendering
        
        segments = []
        current_segment = ''
        
        for char in string:
            if ord(char) < 128:  # ASCII character
                if current_segment:
                    if ord(current_segment[0]) < 128:
                        current_segment = current_segment + char
                    else:
                        segments.append(current_segment)
                        current_segment = char
                else:
                    current_segment = char
            else:  # Unicode character
                if current_segment:
                    if ord(current_segment[0]) >= 128:
                        current_segment = current_segment + char
                    else:
                        segments.append(current_segment)
                        current_segment = char
                else:
                    current_segment = char
        
        if current_segment:
            segments.append(current_segment)
        #print(segments)
        return segments
    
    def fStringInterpreter(element) -> None:
        try:
            import re
            #get globals
            if element.globals: globals=element.globals
            else: globals={}

            if element.text_template: matches = re.findall(r'\{(.*?)\}', element.text_template)
            else: matches = re.findall(r'\{(.*?)\}', element.text)

            for match in matches:
                search="{"+f"{match}"+"}"
                c=element.text_template.replace((search), globals.get(match, "@keyError"))
                element.text=c

            return c
        except:
            return "UNHANDLED ERR"
    
    def is_ascii(string) -> bool:
        return (ord(string[0]) < 128)
    
    def compileNames(pb) -> str:
        artistString=""
        for artist in pb['item']['artists']:
            artistString = artistString + f"{artist['name']}, "
        artistString = artistString[:len(artistString)-2]
        return artistString
    
    def strfTime(ms : int) -> str:
        minutes=int(ms/60_000)

        seconds=int((ms/1000)%60)

        if len(str(seconds)) == 1: seconds = "0" + str(seconds)

        string=f"{minutes}:{seconds}"

        return string
    
class objects:
    def updateAnimationInline(element, render):
        #LEGACY
        raise DeprecationWarning
        #done to enforce animations when script are lagging
        state=element.states.get("pullDown", None)

        

        if state:
            frame=render.f-state['startFrame']
            _d=1

            #calc offsets
            yOffset=(math.cos(frame/((50/10)*3.141592))*state['slope']*(200*_d))+(200*_d)

            #apply scale to size
            element.offsetPosition[1]=yOffset

            #apply offsets to ensure centring

            #ensure update flag

            #ensure end of animation
            if render.f >= state['endFrame']:
                element.states["pullDown"]=None
                element.runEveryFrame=False

        return
    
    def updateAnimationInlineV2(element, render): #based on element state machine
        #done to enforce animations when script are lagging
        try:
            state=element.stateMachine.pullDownAnimation
            if state:
                frame=render.f-state['startFrame']
                _d=1

                #calc offsets
                yOffset=(math.cos(frame/((50/10)*3.141592))*state['slope']*(200*_d))+(200*_d)

                #apply scale to size
                element.offsetPosition[1]=yOffset

                #apply offsets to ensure centring

                #ensure update flag

                #ensure end of animation
                if render.f >= element.stateMachine.pullDownAnimation['endFrame']:
                    element.stateMachine.pullDownAnimation=None
                    element.runEveryFrame=False

        except:
            pass

        return