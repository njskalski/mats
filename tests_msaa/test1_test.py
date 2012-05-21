# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
sys.path.append('../')

from mats_runner import MatsRunner
import unittest
from time import sleep
import os
from mats_runner import winconstants

class A11yTest1(unittest.TestCase):
    def setUp(self):
        url = 'file://./tests/test1.html'
        self.runner = MatsRunner(config_file = '../winconfig.ini', url = url)# = 'file://' + os.path.join(os.getcwd(), 'pages', 'test1.html'))
        self.runner.start()
        
    def test_whatever(self):
        button = self.runner.marionette.find_element(method = 'id', target = 'button1')
        button.click()
        self.runner.wait_for_event('EVENT_OBJECT_FOCUS')
        pass
        
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
