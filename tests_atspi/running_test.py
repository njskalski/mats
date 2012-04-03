# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class BasicA11yTester(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_whatever(self):
        self.assertTrue(True, 'some weird stuff just happened')
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
