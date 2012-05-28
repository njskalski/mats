# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
sys.path.append('../')

from mats_runner import MatsRunner, pyshell 
import unittest
from time import sleep
import os
from mats_runner import winconstants

from mats_runner import accessible_msaa as ma

class A11yTest1(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(config_file = '../winconfig.ini', url = 'file://' + os.path.join(os.getcwd(), 'pages', 'test1.html'))
        self.runner.start()
        
    def test_whatever(self):
        
        tree = None
        try:
            tree = ma.getAccessibleTreeFromMsaa(self.runner.controller.AccessibleObject)
            print str(tree)
        except Exception as e:
            pyshell.falle(e, {'runner' : self.runner,
                              'I' : self.runner.controller.IAccessible,
                              'O' : self.runner.controller.AccessibleObject,
                              'ma' : ma
                              })
            
        pyshell.runShellHere({'runner' : self.runner,
                              'I' : self.runner.controller.IAccessible,
                              'O' : self.runner.controller.AccessibleObject,
                              'ma' : ma,
                              'tree': tree,
                              })
        
        
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
