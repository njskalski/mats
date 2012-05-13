# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mozrunner import FirefoxRunner
from mozprofile import FirefoxProfile

from threading import Thread
import datetime, socket, time

from sys import stderr
from utils import runshellnow

class FirefoxThreadLogger:
    def __init__(self, output):
        self.output = output
        
    def __call__(self, line):
        pass

class FirefoxThread(Thread):
    def __init__(self, binary, marionette_port = 2828):
        Thread.__init__(self)
        self.binary = binary
        self.marionette_port = marionette_port
        self.logger = FirefoxThreadLogger(None)
        
    def run(self):
        self.profile = FirefoxProfile()
        self.profile.set_preferences({"marionette.defaultPrefs.enabled" : True,
                                      "marionette.defaultPrefs.port": 2828})
        self.runner = FirefoxRunner(profile = self.profile,
                                    binary = self.binary,
                                    kp_kwargs = {'processOutputLine' : [self.logger]})

        self.runner.start()        
        self.runner.wait()
        
    def getHWND(self):
        if not self.is_alive():
            return None
        else:
            return self.runner.process_handler.proc_handle.value
        
    def waitForMarionettePortOpenReady(self, timeout=300):
        '''
        This method can be run by an external thread. Returns True when the port is open, or False on timeout.
        It's active waiting with 1 sec heartbeat, if you know better solution please mail me.
        
        Originally taken from:
        https://github.com/mozilla/marionette_client/blob/master/marionette/emulator.py#L246
        '''
        starttime = datetime.datetime.now()
        while datetime.datetime.now() - starttime < datetime.timedelta(seconds=timeout):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('127.0.0.1', self.marionette_port))
                data = sock.recv(16)
                sock.close()
                if '"from"' in data:
                    #print 'MATS: sss: ***"' + str(data) + '"***'
                    return True
            except:
                #import traceback
                #print traceback.format_exc()
                pass
            time.sleep(1)
        return False
        
        