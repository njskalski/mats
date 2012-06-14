# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this tests starts MATS and dumps Accessible tree to "XML_output.xml" file for
#reference

import sys
sys.path.append('../')

from mats_runner import MatsRunner, pyshell 
import unittest
from time import sleep
from mats_runner import winconstants
import os
from mats_runner import accessible_msaa as ma

class A11yTest1(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(config_file = '../winconfig.ini', url = 'file://' + os.path.join(os.getcwd(), 'pages', 'test1.html'))
        self.runner.start()
        
    def test_tree_to_xml_works(self):
        tree = self.runner.controller.getAccessibleTree()
        
        xml_output = open("XML_output.xml", "w")
        tree.write(xml_output)
        xml_output.close()
        
    def tearDown(self):
        self.runner.stop()
        pass
        

if __name__ == '__main__':
    unittest.main()
