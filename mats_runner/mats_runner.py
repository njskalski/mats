# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from get_controller import get_controller
from get_config import get_config

from firefox_thread import FirefoxThread
    
class MatsRunner(object):
    def __init__(self, config_file):
        self.controller = get_controller()
        print 'Using ' + self.controller.__class__.__name__
        
        self.config = get_config(config_file)   #get_config makes sure that the config makes sense. More details in get_config.py
        
        !!use mozprocess instead of mozrunner wrapped with process
        
        print 'Starting Firefox'
        self.FirefoxProcess = FirefoxThread(self.config['Firefox']['binary'])
        self.FirefoxProcess.start()
        self.controller.initFirefoxInstance()
        print 'Waiting for Firefox to stop'
        self.FirefoxProcess.join()
        print 'Program ends'
        
        
        
        
        
        
        
        