# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is a base class for AT controllers used by MATS

class MatsBaseController(object):
    def __init__(self):
        self.FirefoxInstance = None
        pass

    def initFirefoxInstance(self):
        raise Exception("Unimplemented method in " + self.__class__.__name__)