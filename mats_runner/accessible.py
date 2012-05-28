# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is an abstraction layer representing an Accessible Object, os-independetly
# it is written now only to support MSAA, abstraction is to be added later

from xml.etree.ElementTree import Element, ElementTree

class AccessibleElement(Element):
    def __init__(self, IAccessibleNode, attrib = {}):
        nonEmptyAttrib = {k : v for k,v in attrib.iteritems() if v != None}
        
        Element.__init__(self, 'accessible', nonEmptyAttrib)
        self.node = IAccessibleNode
        
class AccessibleTree(ElementTree):
    def __init__(self, element = None, file = None):
        ElementTree.__init__(self, element, file)

    
