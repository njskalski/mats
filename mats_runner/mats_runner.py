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


class MatsRunner(object):
    def __init__(self, config_file):
        
        print 'Using ' + MatsController.__name__
        
        self.config = get_config(config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        self.marionette_port = 2828
        
        
        
        print 'Starting Nightly...'
        self.FirefoxThread = FirefoxThread(self.config['Firefox']['binary'], self.marionette_port)
        self.FirefoxThread.start()
        
        print 'Creating controller'
        pid = self.FirefoxThread.getPID() # this is blocking function!
        self.controller = MatsController(pid)
        
        print 'Waiting for Marionette port to open (' + str(self.marionette_port) + ')'
        portReady = self.FirefoxThread.waitForMarionettePortOpenReady()
        if portReady:
            print 'Marionette port open'
        else:
            print 'Error: timeout'
            #TODO: add some error handling here
            return
         
        sleep(7)
        
        try:
            print 'connecting'
            m = Marionette('localhost', self.marionette_port)
            print 'starting session'
            m.start_session()
            print 'navigating'
            m.navigate('http://9gag.com/')
            print 'marionette succeeded'
        except Exception as e:
            fall(e)

        try:
            print 'starting controller'
            self.controller.start()
            print 'controller successful'
        except Exception as e:
            fall(e)
            
        print 'Waiting for Firefox to stop'
        
        #runShellHere({'runner' : self})
        
        self.FirefoxThread.join()
       
        self.controller.finish()
    
        print 'Program ends'
        
        
        
        
        
