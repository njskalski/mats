# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is an abstraction layer representing an Accessible Object, os-independetly

#xml <accessible> node "mapping" attribute is always an integer, used to identify
#the node in order to re-bound os_spec field (used by accessible methods) each
#time node's python representation is reconstructed. lxml does it a lot.
#the mapping is held in AccessibleTree, which is singleton (now). 

from lxml import etree


import ctypes
import comtypes

from platform import system
osname = system()

if osname == 'Linux':
    raise Exception("Not implemented for platform " + osname + ".") 
elif osname == 'Windows':
    import accessible_msaa as accessible_system
else:
    raise Exception("Unsupported platform " + osname + ".")


class AccessibleElement(etree.ElementBase):
    
    #to understand this, see http://lxml.de/element_classes.html#element-initialization
    def _init(self):
        self.os_spec = AccessibleTree._singleInstance.getOsSpec(int(self.get('mapping')))
    
    def do_default_action(self):
        print 'doing default action with ' + str(self.get('mapping'))
        return accessible_system.doDefaultAction(self.os_spec)
        
    def put_value(self, input_string):
        return accessible_system.putValue(self.os_spec, input_string)
    
    def select(self, flag):
        return accessible_system.select(self.os_spec, flag)
    
    def get_states(self):
        return accessible_system.getAccStateSetFromInt(int(self.get('state')))
    
    def update(self):
        mapping = AccessibleTree._singleInstance.mapping
        accessible_system.updateElement(self, mapping) 
            
class AccessibleTree(etree._ElementTree):
    '''
    for now this is singleton :(
    '''
    _singleInstance = None
     
    
    def __new__(cls, *args, **kwargs):
        if not cls._singleInstance:
            cls._singleInstance = super(AccessibleTree, cls).__new__(
                                cls, *args, **kwargs)

        return cls._singleInstance
    
    def __init__(self, element = None, file = None, mapping = None):
        etree._ElementTree.__init__(self, element, file)
        assert(mapping != None)
        self.mapping = mapping
        
    def getOsSpec(self, num):
        return self.mapping[num]
    
