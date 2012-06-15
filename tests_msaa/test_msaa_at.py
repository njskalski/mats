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
from mats_runner import winconstants

class A11yTest1(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(config_file = '../winconfig.ini', url = 'file://' + os.path.join(os.getcwd(), 'pages', 'test1.html'))
        self.runner.start()
        
    def test_msaa_at(self):
        self.assertEqual(True, self.runner.instantiate_a11y())
        tree = self.runner.controller.getAccessibleTree()

        FileButton = tree.xpath('//*[@name="File" and @keyboard-shortcut="Alt+F" and @role="menuitem"]')
        
        self.assertEqual(len(FileButton), 1)
        FileButton = FileButton[0]
        
        self.assertEqual(len(FileButton), 1) #it should have a single child now
        
        FilePopup = FileButton[0]
        self.assertEqual(len(FilePopup), 0) #that has no children
        
        #until is clicked.
        
        FileButton.do_default_action()
        
        FileButton.update()
        
        print 'fb len : ' + str(len(FileButton))
        print 'fb :' + str(FileButton)
        
        
        
        self.assertTrue(
            self.runner.wait_for_event('EVENT_OBJECT_FOCUS', button.do_default_action, timeout = 10)
            )
        pass
            
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
