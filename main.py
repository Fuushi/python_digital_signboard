from render import *
from behaviorThread import *
from process_thread import *
from logger import logger
import threading
import random
import sys

def main():
    lg = logger()
    lg.log("INIT MAIN", sys.argv)

    render=renderObj()

    threads=[]
    
    thread=threading.Thread(target=renderThread, args=(render,))
    thread.start()
    threads.append(threadWrapper(thread, renderThread, "render"))

    thread=threading.Thread(target=processThread.THREAD, args=(render,))
    thread.daemon=True
    thread.start()
    threads.append(threadWrapper(thread, processThread.THREAD, "process"))

    thread=threading.Thread(target=behaviorThread, args=(render,))
    thread.daemon=True
    thread.start()
    threads.append(threadWrapper(thread, behaviorThread, "behavior"))

    time.sleep(1)

    render.loadSceneFromFile(render.config.get("default_preset", "home"))

    hijack(render)

    while True:

        for thread in threads:

            #if render thread is dead, return
            if (thread.id == "render") and (not thread.thread.is_alive()):
                lg.log("EXITED FROM MAIN BY RENDER", threads)
                lg.log(" ")
                return
            
            else:
                #restart dead threads (not render)
                if not thread.thread.is_alive():
                    #
                    print(f"WARNING!!!: ATTEMPTING THREAD RESTART {thread.id}")

                    thread.thread.join()

                    sub=threading.Thread(target=thread.target, args=(render,))
                    sub.daemon=True
                    sub.start()

                    thread.thread=sub

                    lg.log("RESTARTED THREAD", {"id" : thread.id})

            #handle explicit exit clauses (TODO)
                    

            
        time.sleep(1)


    return

class threadWrapper:
    def __init__(self, thread, target=None, id=None) -> None:
        self.thread=thread
        self.target=target
        self.id=id
        return

def hijack(render):
    pass
    return
        
if __name__ == "__main__":
    main()