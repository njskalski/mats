# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is an abstraction layer representing an Accessible Object, os-independetly
# it is written now only to support #TODO investigate why it never works MSAA, abstraction is to be added later

from xml.etree.ElementTree import Element, ElementTree

from accessible_msaa import doDefaultAction, putValue

class AccessibleElement(Element):
    def __init__(self, os_spec, attrib = {}):
        '''
        os_spec is OS-specific data
        '''
        
        nonEmptyAttrib = {k : v for k,v in attrib.iteritems() if v != None and v != ''}
        
        if os_spec[1] != 0: #not an IAccessible, but a child of it
            name = 'accessibleChild'
        else:
            name = 'accessible'
            
        Element.__init__(self, name, nonEmptyAttrib)
        self.node = os_spec
    
    def do_default_action(self):
        doDefaultAction(self.os_spec)
        
    
    
class AccessibleTree(ElementTree):
    def __init__(self, element = None, file = None):
        ElementTree.__init__(self, element, file)

    
