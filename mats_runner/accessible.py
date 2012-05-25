# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is an abstraction layer representing an Accessible Object, os-independetly

from xml.etree.ElementTree import Element

class AccessibleElement(Element):
    def __init__(self, name):
        Element.__init__(self, name)
    
