# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#This test tests, whether if Firefox stops once close system button is clicked.
#This test presently (June 14, 2012) fails (Firefox returns error), don't know
#why. I also left commented code that points to a different "close" button that
#happens to be in accessible tree, and does not work. I don't know why it's
#there, why it doesn't work, and what was MSAA intention in exposing it to user
#but I leave it for reference. 

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
        
    def test_if_firefox_stops_on_clicking_close_button(self):
        
        self.assertEqual(True, self.runner.instantiate_a11y())

        tree = self.runner.controller.getAccessibleTree()
        
#        this points to something else. No clue what. The MSAA is as intuitive as quantum mechanics
#        menu_buttons = tree.xpath('accessible[@name="System" and @role="2"]/accessible[@name="System" and @role="12"]/accessible[@name="System" and @role="11"]/*')
#        #/accessible[@name="System"]/accessible[@name="System"]/accessible[@default-action="Execute" and @keyboard-shortcut="c"]')
#        
#        print menu_buttons
#        
#        for button in menu_buttons:
#            if "Close" in (button.get("name") or ""):
#                close_button = button
#                break
#        
#        self.assertEqual(close_button.get('default-action'), 'Execute')
#        pyshell.runShellHere({'runner' : self.runner, 'but' : close_button})
        
        
        close_button = tree.xpath('accessible[@value="MSAA test1 - Nightly"]/accessible[@name="Close" and @role="43"]')
        self.assertEqual(len(close_button), 1)
        close_button = close_button[0]
        self.assertEqual(close_button.get('default-action'), 'Press') 
        self.assertTrue(close_button.do_default_action())
        self.runner.wait_for_stop()
        pass
            
    def tearDown(self):
        #self.runner.stop() #not in this test!
        pass
        

if __name__ == '__main__':
    unittest.main()
