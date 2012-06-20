# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this test tests, whether EVENT_OBJECT_FOCUS is fired once a button is clicked.
#Click action is made via Accessible tree
#this test fails for unknown reason - Firefox acts weirdly after the button is
#clicked.

import sys
sys.path.append('../')

from mats_runner import MatsRunner, pyshell 
import unittest
from time import sleep
import os
from mats_runner import winconstants, winutils

class A11yTest1(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(config_file = '../winconfig.ini', url = 'file://' + os.path.join(os.getcwd(), 'pages', 'test1.html'))
        self.runner.start()
        
    def test_ia2_from_msaa(self):
        
        self.assertEqual(True, self.runner.instantiate_a11y())

        tree = self.runner.controller.getAccessibleTree()

        app_handle = tree.xpath('//*[@role="application"]')
    
        self.assertEqual(len(app_handle), 1)
        app_handle = app_handle[0]
        
        print 'starting experimenting with ia2'
        
        ia2m = winutils.loadIAccessible2Module()
        
        def bfs(queue):
            while not len(queue) == 0:
                actnode = queue[0]
                queue = queue[1:] 
                print actnode
                winutils.getAccessible2ObjectFromMSAA(actnode.os_spec[0])
                
                for child in actnode:
                    queue.append(child)
        
        bfs([app_handle])
        
        #ia2object = winutils.getAccessible2ObjectFromMSAA(app_handle.os_spec[0])
        
        #self.runner.wait_for_stop()
        
        pass
                    
    
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
