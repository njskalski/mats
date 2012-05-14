#taken from : http://code.activestate.com/recipes/355319/

import sys
from code import InteractiveConsole
import traceback
from itertools import chain 

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = ''.join(self.out)
        self.reset()
        return output

class superHandler:
    class callHandler:
        def __init__(self, name):
            self.name = name
        
        def __call__(self, *args, **kwargs):
            print self.name,args,kwargs
        
        def lookup(self, name):
            print 'someone is looking for "' + name + '" in "' + self.name + '...'
            
        def __getattribute__(self,name):
            self.lookup(name)
            return callHandler(name)
        
        def __getattr__(self, name):
            return self.__getattribute__(name)
    
    def __getattr__(self,name):
        return self.callHandler(name)
    
    def __getattribute__(self,name):
        return self.__getattr__(name)

class Shell(InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self, defs = {}):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        
        #merging envrironments
        env = {k : v for k, v in chain(globals().iteritems(), defs.iteritems())}
        
        InteractiveConsole.__init__(self, env)
        return

    def get_output(self): sys.stdout = self.cache
    def return_output(self): sys.stdout = self.stdout

    def push(self,line):
        self.get_output()
        # you can filter input here by doing something like
        # line = filter(line)
        InteractiveConsole.push(self,line)
        self.return_output()
        output = self.cache.flush()
        # you can filter the output here by doing something like
        # output = filter(output)
        print output # or do something else with it
        return 

def runShellHere(defs = {}):
    s = Shell(defs)
    s.interact()

def gf(obj, infix):
    for field in dir(obj):
        if infix in field:
            print field,

def fall(e):
    print 'Exception fall: ' + str(e.__class__)
    print traceback.format_exc()

def falee(e):
    fall(e)
    runShellHere()
