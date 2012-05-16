# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from get_config import get_config
from mats_controller import *

from firefox_thread import FirefoxThread
from marionette import Marionette

from time import sleep

from pyshell import *
from winutils import *

from threading import Thread, Event


class MatsRunner(Thread):
    def __init__(self, config_file = 'config.ini', url = 'about:blank'):
        Thread.__init__(self)
        self.config_file = config_file
        self.url = url
        self._ready = Event()
        
    def run(self):
        '''
        This method starts MATS.
        '''
        
        print 'Using ' + MatsController.__name__ + ' as controller.'
        print 'Loading config from "' + self.config_file + '"...',
        self.config = get_config(self.config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        self.marionette_port = self.config['Marionette']['port'] 
        print 'OK'
        
        print 'Starting Firefox/Nightly from "' + self.config['Firefox']['binary'] + '" with Marionette on port ' + str(self.marionette_port) + '.'        
        self.FirefoxThread = FirefoxThread(self.config['Firefox']['binary'], self.marionette_port)
        self.FirefoxThread.start()
        
        print 'Creating controller'
        pid = self.FirefoxThread.getPID() # this function blocks until PID is available from FirefoxThread
        self.controller = MatsController(pid)
        
        print 'Starting controller'
        self.controller.start()
        self.controller.wait_for_ready()
        
        print 'Waiting for Marionette port to open (' + str(self.marionette_port) + ')'
        portReady = self.FirefoxThread.waitForMarionettePortOpenReady(self.config['Marionette']['port_timeout'])
        if portReady:
            print 'Marionette port open'
        else:
            print 'Error: timeout, shutting down MATS'
            self.controller.stop()
            self.FirefoxThread.stop()
        
        #TODO: remove line below once https://bugzilla.mozilla.org/show_bug.cgi?id=753273 is fixed
        sleep(10)
        
        try:
            print 'Starting Marionette'
            m = Marionette('localhost', self.marionette_port)
            #TODO: move starting session and navigation to separate methods
            print 'Starting session'
            m.start_session()
            print 'Navigating to ' + self.url
            m.navigate(self.url)
        except Exception as e:
            print 'Error starting Marionette'
            fall(e)
            self.controller.stop()
            self.FirefoxThread.stop()

        print 'MATS up and running. Waiting until Firefox/Nightly to stops.'
        self._ready.set()
        self.FirefoxThread.join()
        print 'Stopping controller'
        self.controller.stop()
        self.controller.join()
        print 'MATS runner finishes.'
    
    def wait_until_ready(self, timeout = None):
        '''
        To be called by external thread. Blocks until MATS runner is ready to receive commands
        '''
        self._ready.wait(timeout)
    
    def stop(self):
        '''
        To be called by external thread. Stops MATS runner.
        '''
        self.FirefoxThread.stop()
        