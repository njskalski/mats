# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this test tests, whether if Firefox stops once 'x' is clicked :)

#this test presently fails, don't know why

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
        
    def test_msaa_focus(self):
        
        self.assertEqual(True, self.runner.instantiate_a11y())

        tree = self.runner.controller.getAccessibleTree()

        button = tree.xpath('//*[@name="Click me" and @role="43"]')
        
        self.assertEqual(len(button), 1)
        button = button[0]
        
        self.assertTrue(
            self.runner.wait_for_event('EVENT_OBJECT_FOCUS', button.do_default_action, timeout = 10)
            )
        pass
            
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
