# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_runner import MatsRunner

class A11yTest1(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(config = 'winconfig.ini', webpage = 'file://./pages/test1.html')
        
    def test_whatever(self):
        self.marionette.navigate('file://./tests/test1.html')
        
    def tearDown(self):
        self.runner.stop()

if __name__ == '__main__':
    unittest.main()
