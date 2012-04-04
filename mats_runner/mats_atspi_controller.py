# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from mats_base_controller import MatsBaseController
import pyatspi

class MatsAtspiController(MatsBaseController):
    def __init__(self):
        MatsBaseController.__init__(self)
        pass

    def initFirefoxInstance(self):        
        raise Exception("This is a placeholder")