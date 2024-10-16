import os, time, psutil
from datetime import datetime
import numpy as np

class behavior:
    def __init__(self, state, render) -> None:
        self.interval=60 #60
        self.uptime=time.time()
        self.reset_flag=time.time()+time_to_midnight()
        
        if os.path.exists("cache/avg.npz"):
            screensaver.loadCounter(self, "cache/avg.npz")
        else:
            self.counter=screensaver.createCounter(1280,400)
            self.count=0
        return
    

    def run(self, state, render):
        #if time to reset, reset
        if time.time() > self.reset_flag: render.dead=True

        #if memory overrun likelym reset
        mem_usage_percentage = psutil.virtual_memory().percent
        if mem_usage_percentage > 95.0:
            render.dead=True

        #screen saver
        sc=screensaver.getScreen(render)
        screensaver.incrementCounter(self.counter, sc)
        self.count+=1

        #output average
        if (self.count % 1 == 0): #adjust (1) to change minutes per output
            screensaver.saveAverageAsGrayscale(self.counter, self.count, render)
            screensaver.dumpCounter(self, self.counter, self.count, "cache/avg")
        return
    

def time_to_midnight() -> int:
    now = datetime.now()
    h = now.strftime("%H")
    s_to_midnight_approx =  (24 - int(h))*3600

    #debug inturupt TODO remove
    #return 20

    return s_to_midnight_approx

#TODO drop burnin protection here
#
class screensaver:
    def getScreen(render) -> object:
        # inherits render properties
        #print("attempting to get screen state")
        # Capture the current state of the display
        display_surface = render._screen.copy()

        # Save the captured state as an image (optional)
        #render._pygame.image.save(display_surface, 'DEBUGOUT.png')

        # Convert the surface to a numpy array
        image = render._pygame.surfarray.array3d(display_surface)
        return image

    def createCounter(x, y):
        # Create a counter for RGB values
        return np.zeros((x, y, 3))

    def incrementCounter(counter, image):
        # Increment the counter by the RGB values of the image
        counter += image[:counter.shape[0], :counter.shape[1], :]
        return counter
    
    def saveAverageAsGrayscale(counter, count, render):
        if count == 0:
            print("No increments to average.")
            return
        
        # Compute the average RGB values
        avg_gray = counter / count

        # Normalize to the range [0, 255]
        avg_gray = (avg_gray / avg_gray.max()) * 255

        # Invert the grayscale image
        avg_gray = 255 - avg_gray
        
        # Convert to an 8-bit unsigned integer type
        avg_gray = avg_gray.astype(np.uint8)
        
        # Create a Pygame surface from the grayscale image
        gray_surface = render._pygame.surfarray.make_surface(avg_gray)
        
        # Save the grayscale image
        render._pygame.image.save(gray_surface, f'DEBUGOUTAVG.png')

        return
    
    
    def dumpCounter(inherit, counter, count, filename):
        np.savez(filename, counter=counter, count=count)
        print(f"Counter and count saved to {filename}.npz")

    def loadCounter(inherit, filename):
        data = np.load(filename)
        counter = data['counter']
        count = data['count']
        inherit.count=count
        inherit.counter=counter
        print(f"Counter and count loaded from {filename}.npz")
        return counter, count