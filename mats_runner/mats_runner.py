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

import threading

class MatsRunner(object):
    def __init__(self, config_file = 'config.ini', url = 'about:blank'):
        self.config_file = config_file
        self.url = url
        
    def start(self):
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
        #sleep(10)
        
        try:
            print 'Starting Marionette'
            self.marionette = Marionette('localhost', self.marionette_port)
            #TODO: move starting session and navigation to separate methods
            print 'Starting session'
            sleep(5) #TODO temporary workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=757078
            self.marionette_session = self.marionette.start_session()
            print 'Navigating to ' + self.url
            print self.marionette.navigate(self.url)
        except Exception as e:
            print 'Error starting Marionette'
            fall(e)
            self.controller.stop()
            self.FirefoxThread.stop()

        print 'MATS up and running. Waiting until Firefox/Nightly to stops.'
    
    def wait_for_stop(self):
        self.FirefoxThread.join()
        print 'Stopping controller'
        self.controller.stop()
        self.controller.join()
        print 'MATS runner finishes.'
    
    def stop(self):
        self.FirefoxThread.stop()
        self.FirefoxThread.join()
        print 'Stopping controller'
        self.controller.stop()
        self.controller.join()
        print 'MATS runner finishes.'
    
    def instantiate_a11y(self):
        '''
        runs via marionette script taken from 
        http://dxr.lanedo.com/search.cgi?tree=mozilla-central&string=nsIAccessibleApplication
        
        sets context to content after doing it's stuff
        '''
        
        script = \
'''
const nsIAccessibleRetrieval = Components.interfaces.nsIAccessibleRetrieval;
const nsIAccessibleApplication = Components.interfaces.nsIAccessibleApplication;

var gAccRetrieval = Components.classes["@mozilla.org/accessibleRetrieval;1"].
  getService(nsIAccessibleRetrieval);
app = gAccRetrieval.getApplicationAccessible().
    QueryInterface(nsIAccessibleApplication);
    
return app != null;
'''
        self.marionette.set_context("chrome")
        notNull = self.marionette.execute_script(script)
        #self.marionette.set_context("content")
        return notNull
    
    def is_a11y_instantiated(self):
        '''
        to do doc
        '''
        
        script = \
'''
    var enabled = false;
    return enabled;
    try {
        enabled = components.manager.QueryInterface(Ci.nsIServiceManager)
                    .isServiceInstantiatedByContractID(
                    "@mozilla.org/accessibilityService;1",
                    Ci.nsISupports);
    } catch (ex) {
        enabled = false;
    }
    return enabled;
'''
        return self.marionette.execute_script(script)
    
    def wait_for_event(self, event_string, callable, timeout = 60):
        '''
        this method is the easiest interface to wait for an event.
        First, it registers listener.
        Second, it calls callable (TODO: add arguments)
        Third, it waits for the event or timeouts
        
        it returns True if the event was captured, and False if timeout occured
        
        TODO: abstract it to cross-platform
        '''
        
        arrived = threading.Event()
        
        def callback(event):
            print 'got event! ' + str(event)
            arrived.set()
            
        self.controller.register_event_listener(event_string, callback)
        self.controller.unpause_event_loop()
        
        callable()
        #TODO next two lines should be 'atomic' towards event pump. NEEDS URGENT FIX
        
        result = arrived.wait(timeout)
        
        self.controller.pause_event_loop()
        self.controller.deregister_event_listener(event_string, callback)
        return result