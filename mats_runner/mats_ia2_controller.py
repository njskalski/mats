# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_base_controller import MatsBaseController
import winutils
import winconstants

from windows_listener import WindowsListener
import datetime
from time import sleep
from threading import Event, Lock, Condition

from collections import defaultdict

from accessible_ia2 import getAccessibleTreeFromIA2

class MatsIA2Controller(MatsBaseController):
    
    def __init__(self, pid):
        MatsBaseController.__init__(self, pid)
        
        self._ready = Event()
        self._listeners = defaultdict(set) # event_id -> set(callables)
        
        #main loop controls:
        self._stateCondition = Condition()
        self._stateActive = True
        self._statePaused = True
        
    def run(self):
        print 'Controller is waiting for window (HWND) to appear'
        self.hwnd = self.wait_and_get_firefox_hwnd_from_pid()
        print 'Controller got the HWND, and it is ' + str(self.hwnd)
        
        #just some shortcuts
        self.IA2Module = winutils.loadIAccessible2Module()
        self.IAccesssible2 = self.IA2Module.IAccessible2
        self.Accessible2Object = winutils.getAccessible2ObjectFromWindow(hwnd = self.hwnd)
        
        print 'IAccessible2 object is: ' + str(self.Accessible2Object)
        
        #starting listener
        self.listener = WindowsListener(hwnd = self.hwnd, pid = self.pid)
        self.listener.start()
        
        self._ready.set()
        
        print 'Listener is ready, call unpause_event_loop() to start pumping messages'
        
        # loop invariant: self._stateCondition is acquired, everywhere except wait() and sleep() lines
        self._stateCondition.acquire()
        while True:
            if self._stateActive:
                if self._statePaused == False:
                    self.listener.pump_messages() #TODO if function returns *always after all* messages are handled by WinProc, we can remove underlying lock to improve performance
                    messages = self.listener.get_queued_events()
                    self._process_messages(messages)
                    self._stateCondition.release()
                    sleep(1) #TODO here should be passive waiting
                    self._stateCondition.acquire()
                else:
                    self._stateCondition.wait()
                    continue
            else:

                break

        if self._statePaused == False:
            self.listener.stop()
        self._stateCondition.release()

    def unpause_event_loop(self):
        '''
        starts event loop
        '''
        
        self._stateCondition.acquire()
        if self._statePaused:
            self.listener.start()
            self._statePaused = False
        self._stateCondition.notify()
        self._stateCondition.release()
        
    def pause_event_loop(self):
        '''
        pauses event loop, deregisters windows event hook method, cleans event queue
        '''
        
        self._stateCondition.acquire()
        if not self._statePaused:
            self.listener.stop()
            self.listener.pump_messages()
            self.listener.get_queued_events()
            self._statePaused = True
        self._stateCondition.notify()
        self._stateCondition.release()
        

    def stop(self):
        '''
        To be called by external thread. Stops Controller thread.
        '''
        self._stateCondition.acquire()
        self._stateActive = False
        self._stateCondition.notify()
        self._stateCondition.release()
        
        self.join()

        
    def register_event_listener(self, event_string, callable):
        with self._stateCondition:
            self._listeners[winconstants.eventNameToInt[event_string]].add(callable)
        
    def deregister_event_listener(self, event_string, callable):
        with self._stateCondition:#
            self._listeners[winconstants.eventNameToInt[event_string]].remove(callable)

    def _process_messages(self, messages):
        '''
        while here, stateConditionLock is acquired!
        '''
        for event in messages:
            for callable in self._listeners[event.get_id()]:
                callable(event)
            
    def clear_event_queue(self):
        with self._eventQueueLock:
            self._eventQueue = []
    
    def _inject_events(self, events):
        if len(events) > 0:
            with self._eventQueueLock:
                self._eventQueue.append(events)
    
    def wait_for_ready(self, timeout = None):
        self._ready.wait(timeout)
    
    def wait_and_get_firefox_hwnd_from_pid(self, timeout = 60):
        '''
        This method blocks controller thread until Firefox/Nightly window HWND is available.
        TODO : this method sucks, but I really need it in order for MATS to be
        reliable. Fix active waiting with something civilized. 
        '''
        
        starttime = datetime.datetime.now()
        while datetime.datetime.now() - starttime < datetime.timedelta(seconds=timeout):
            Nightlies = winutils.getNightliesByPID(self.pid)
            if len(Nightlies) > 0:
                break
            sleep(1)
        
        if len(Nightlies) == 0:
            raise Exception("Nightly window not found - HWND wait timeout")
        
        if len(Nightlies) > 1:
            print 'WARNING: more than one instance of Nightly found, using first one.'
            print Nightlies
        return Nightlies[0][0]
    
    def getAccessibleTree(self):
        return getAccessibleTreeFromIA2(self.Accessible2Object)
        