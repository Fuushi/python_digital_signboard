import os, datetime

class logger:
    def __init__(self, outputDir="out/", defaultFile="logs.txt") -> None:
        self.outputDir=outputDir
        self.defaultFile=defaultFile
        return
    
    def log(self, error, kwargs={}):
        #path management
        path = os.path.join(self.outputDir, self.defaultFile)
        if not os.path.exists(self.outputDir): os.mkdir(self.outputDir)

        #get metadata
        current_datetime = datetime.datetime.now()
        datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        #pack
        packet=f"[{datetime_string}] {str(error)}:::{str(kwargs)}\n"

        #save
        with open(path, "a+") as fp:
            fp.write(packet)

        #exit
        return