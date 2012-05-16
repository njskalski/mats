# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class BasicA11yTester(unittest.TestCase):
    def setUp(self):
        self.runner = MatsRunner(webpage = 'file://./pages/test1.html')
        
    def test_whatever(self):
        pass
        
    def tearDown(self):
        self.runner.stop()

if __name__ == '__main__':
    unittest.main()
