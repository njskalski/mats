# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this is a basic test of AccessibleTree facilities working. It checks:
# accessibleTree construction
# accessibleTree navigation via xpath
# accessibleTree xml getters
# accessibleTree custom node methods (MSAA)
# accessibleTree updating (manual)

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
        
        FilePopup = None #removing old
        #until is clicked.
        
        FileButton.do_default_action()
        FileButton.update()
        
        self.assertGreater(len(FileButton), 1) # check for newcomer
        
        FilePopup2 = FileButton[1] #get him
        
        self.assertGreater(FilePopup2.get("height"), 0) #he should be visible.
        
#        print 'fb len : ' + str(len(FileButton))
#        for child in FileButton:
#            print str(child.items())
#            for sub in child:
#                print 'sub:' + str(sub.items())

        ExitButton = FilePopup2.xpath('accessible[@name="Exit" and @role="menuitem"]')
        self.assertEqual(len(ExitButton), 1)
        ExitButton = ExitButton[0]
        
        self.assertTrue(ExitButton.do_default_action())
        
        self.runner.wait_for_stop()
            
    def tearDown(self):
        pass
        

if __name__ == '__main__':
    unittest.main()
