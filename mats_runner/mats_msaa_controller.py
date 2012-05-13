# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_base_controller import MatsBaseController

from threading import Thread, Semaphore

#class PyiaRegisterThread(Thread):
#    '''
#    Represents a thread that pumps events from pyia.    
#    methods to be called from other thread:
#    start() to start it
#    stop() to stop it
#    '''
#    
#    def __init__(self, registry):
#        Thread.__init__(self)
#        self.registry = registry
#        
#        self._continue = True
#        self._continueLock = Semaphore(True)
#        
#    
#    def run(self):
#        print 'Starting ' + str(self.__class__)
#        self.eventListener = PyiaEventListener()
#        self.registry.registerEventListener(self.eventListener, 'EVENT_OBJECT_FOCUS')
#        
#        while True:
#            self._continueLock.acquire(True)
#            if self._continue != True:
#                break
#            self._continueLock.release()
#            self.registry.iter_loop(5)
#            print 'pump'
#        
#        
#    def stop(self):
#        
#        self._continueLock.acquire(True)
#        self._continue = False
#        self._continueLock.release() 
#        
#        self.registry.deregisterEventListener(self.eventListener)
#        #self.registry.stop()
#        print 'Stopping ' + str(self.__class__)
#
#class PyiaEventListener(object):
#    def __init__(self):
#        print 'MATS: listener ready'
#        pass
#        
#    def __call__(self, **args):
#        print 'MATS: MSAA CALL: ' + str(args)

class MatsMsaaController(MatsBaseController):
    def __init__(self): 
        pass

    def grabFirefoxInstance(self):
#        self.RegisterThread = PyiaRegisterThread(pyia.Registry)
#        self.RegisterThread.start()
        pass
        
    def finish(self):
        pass
#        self.RegisterThread.stop()
#        self.RegisterThread.join()