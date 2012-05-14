# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_base_controller import MatsBaseController

from threading import Thread, Semaphore
import winutils

class MatsMsaaController(MatsBaseController):
    def __init__(self): 
        pass

    def start(self):
        self.hwnd = self.getFirefoxHwnd()
        self.IAccessible = winutils.loadIAccessible()
        self.AccessibleObject = winutils.getAccessibleObjectFromWindow(self.hwnd)
        pass
        
    def finish(self):
        pass

    def getFirefoxHwnd(self):
        Nightlies = winutils.getNightlies()
        if len(Nightlies) == 0:
            raise Exception("No instance of Nightly found running")
        if len(Nightlies) > 1:
            print 'WARNING: more than one instance of Nightly found, using first one.'
        return Nightlies[0][0]
         