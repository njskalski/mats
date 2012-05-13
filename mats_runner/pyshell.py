#taken from : http://code.activestate.com/recipes/355319/

import sys
from code import InteractiveConsole

class FileCacher:
    "Cache the stdout text so we can analyze it before returning it"
    def __init__(self): self.reset()
    def reset(self): self.out = []
    def write(self,line): self.out.append(line)
    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output

class Shell(InteractiveConsole):
    "Wrapper around Python that can filter input/output to the shell"
    def __init__(self):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        InteractiveConsole.__init__(self, globals())
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

def runShellHere():
    s = Shell()
    s.interact()

def gf(obj, infix):
    for field in dir(obj):
        if infix in field:
            print field,
            