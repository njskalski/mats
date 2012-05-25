# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is a base class for AT controllers used by MATS
# controllers are threads :( since they pretend applications using accessible
# interface

from threading import Thread, Event

class MatsBaseController(Thread):
    def __init__(self, pid):
        Thread.__init__(self)
        self.pid = pid

    def run(self):
        raise Exception("Unimplemented method in " + self.__class__.__name__)
    
    def stop(self):
        raise Exception("Unimplemented method in " + self.__class__.__name__)
    
    def getAccessibleTree(self):
        raise Exception("Unimplemented method in " + self.__class__.__name__)