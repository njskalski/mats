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
        
        print 'Using ' + MatsController.__name__
        
        self.config = get_config(config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        self.marionette_port = 2828
        
        print 'Starting Firefox...\t',
        self.FirefoxThread = FirefoxThread(self.config['Firefox']['binary'], self.marionette_port)
        self.FirefoxThread.start()
        '''
        if self.FirefoxThread.waitForMarionettePortOpenReady():
            print 'OK'
        else:
            print 'Error: timeout'
            #TODO: add some error handling here
           ''' 
        # The line below removes firefox stdout from output, since I needed a clean
        # log for debugging. It probably can be replaced with someting better, but
        # necessary functions are not exported by MozBase
        self.FirefoxThread.runner.process_handler.proc.stdout = None
        '''
        mc = Marionette('localhost', self.marionette_port)
        mc.start_session()
        mc.navigate('onet.pl')
        
        print 'Waiting for Firefox to stop'
        self.FirefoxProcess.join()
        print 'Program ends'
        '''
        
        
        
        