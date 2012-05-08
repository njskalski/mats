# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from get_config import get_config
from mats_controller import *

from firefox_thread import FirefoxThread
from marionette import Marionette

from time import sleep

from sys import stderr

class MatsRunner(object):
    def __init__(self, config_file):
        
        print 'MATS: Using ' + MatsController.__name__
        
        self.config = get_config(config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        self.marionette_port = 2828
        
        print 'MATS: Starting Firefox...\t',
        self.FirefoxThread = FirefoxThread(self.config['Firefox']['binary'], self.marionette_port)
        self.FirefoxThread.start()
        
        if self.FirefoxThread.waitForMarionettePortOpenReady():
            print 'MATS: OK'
        else:
            print 'MATS: Error: timeout'
            #TODO: add some error handling here
            return
         
        try:
            mc = Marionette('127.0.0.1', self.marionette_port)
            mc.start_session()
            mc.navigate('onet.pl')
            print 'MATS: marionette succeeded'
        except Exception as e:
            print 'MATS: ' + str(e.__class__)
            
        print 'MATS: Waiting for Firefox to stop'
        self.FirefoxThread.join()
        print 'MATS: Program ends'
        
        
        
        