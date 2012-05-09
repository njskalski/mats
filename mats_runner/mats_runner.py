# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from get_config import get_config
from mats_controller import *

from firefox_thread import FirefoxThread
from marionette import Marionette

from time import sleep

class MatsRunner(object):
    def __init__(self, config_file):
        
        print 'MATS: Using ' + MatsController.__name__
        
        self.config = get_config(config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        self.marionette_port = 2828
        
        print 'MATS: Starting Firefox...'
        self.FirefoxThread = FirefoxThread(self.config['Firefox']['binary'], self.marionette_port)
        self.FirefoxThread.start()
        
        portReady = self.FirefoxThread.waitForMarionettePortOpenReady() 
        
        if portReady:
            print 'MATS: Marionette port open'
        else:
            print 'MATS: Error: timeout'
            #TODO: add some error handling here
            return
        
        sleep(4)
         
        try:
            m = Marionette('localhost', self.marionette_port)
            m.start_session()
            print 'MATS: wchodze na onet'
            m.navigate('onet.pl')
            print 'MATS: marionette succeeded'
        except Exception as e:
            print 'MATS: error ***"' + str(e) + '"***'
            import traceback
            print 'MATS: error ***"' + traceback.format_exc() + '"***'
            
        print 'MATS: Waiting for Firefox to stop'
        self.FirefoxThread.join()
        print 'MATS: Program ends'
        
        
        
        