import math, os
import importlib.util


class Scripts:
    def loadScript(scriptID):
        def scriptNotFoundWarning(element, render):
            print("Script not found")
            return

        table = {}
        
        #get additional scripts from folder    
        files=os.listdir("scripts/")
        for file in files:
            if ".py" in file:
                name=file.replace(".py","")
                #print(f"Importing script: {name}")
                func, meta = importer(os.path.join("scripts/", file))
            
                table[name] = functionWrapper(func, meta)

        pass #breakpoint
        
        return  table.get(scriptID, scriptNotFoundWarning)
    
def importer(module_path, function_name="script"):
    # Load the module
    spec = importlib.util.spec_from_file_location("module_name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the function from the module
    func = getattr(module, function_name)
    metadata=getattr(module, "metadata")

    return func, metadata

class functionWrapper:
    def __init__(self, function, meta) -> None:
        self.run = function
        self.runOn=meta().get("runOn", "update")
        return