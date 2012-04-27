# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mozrunner import FirefoxRunner
from mozprofile import FirefoxProfile

from threading import Thread
from time import sleep

class FirefoxThread(Thread):
    def __init__(self, binary):
        print 'fftconstruct'
        Thread.__init__(self)
        self.binary = binary
        print 'fftconstructed'
        
    def run(self):
        print 'Starting FirefoxProcess'
        self.profile = FirefoxProfile()
        self.runner = FirefoxRunner(self.profile, self.binary)
        
        self.runner.start()
        self.runner.wait()