# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_base_controller import MatsBaseController
import winutils
import datetime
from time import sleep
from threading import Event

class MatsMsaaController(MatsBaseController):
    def __init__(self, pid):
        MatsBaseController.__init__(self,pid)
        self._ready = Event()
        
    def run(self):
        print 'Controller is waiting for window (HWND) to appear'
        self.hwnd = self.wait_and_get_firefox_hwnd()
        print 'Controller got the HWND'
        
        #just some shortcuts
        self.IAccessible = winutils.loadIAccessible()
        self.AccessibleObject = winutils.getAccessibleObjectFromWindow(hwnd = self.hwnd)
        
        #starting listener
        self.listenerThread = winutils.ListenerThread(hwnd = self.hwnd, pid = self.pid)
        self.listenerThread.start()
        self.listenerThread.wait_for_ready()
        self._ready.set()
        self.listenerThread.join()
        
    def wait_for_ready(self, timeout = None):
        self._ready.wait(timeout)
    
    def stop(self):
        self.listenerThread.stop()

    def wait_and_get_firefox_hwnd(self, timeout = 60):
        '''
        This method blocks controller thread until Firefox/Nightly window HWND is available.
        '''
        
        starttime = datetime.datetime.now()
        while datetime.datetime.now() - starttime < datetime.timedelta(seconds=timeout):
            print '..',
            try:
                Nightlies = winutils.getNightlies()
            except winutils.NightlyWindowNotFoundException as ne:
                sleep(1)
            
        if len(Nightlies) > 1:
            print 'WARNING: more than one instance of Nightly found, using first one.'
        return Nightlies[0][0]
    