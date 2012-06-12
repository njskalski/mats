# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# this is an abstraction layer representing an Accessible Object, os-independetly
# it is written now only to support #TODO investigate why it never works MSAA, abstraction is to be added later


from lxml import etree


import ctypes
import comtypes

from platform import system
osname = system()

if osname == 'Linux':
    pass #TODO implement accessible_atspi 
elif osname == 'Windows':
    import accessible_msaa as accessible_system
else:
    raise Exception("Unsupported platform " + osname + ".")


class AccessibleElement(etree.ElementBase):
    def _init(self):
        self.os_spec = AccessibleTree._singleInstance.getOsSpec(int(self.get('mapping')))
    
    def do_default_action(self):
        return accessible_system.doDefaultAction(self.os_spec)
        
    def put_value(self, input_string):
        return accessible_system.putValue(self.os_spec, input_string)
    
class AccessibleTree(etree.ElementTree):
    '''
    for now this is singleton :(
    '''
    _singleInstance = None
     
    
    def __new__(cls, *args, **kwargs):
        if not cls._singleInstance:
            cls._singleInstance = super(AccessibleTree, cls).__new__(
                                cls, *args, **kwargs)

            # from http://lxml.de/element_classes.html#setting-up-a-class-lookup-scheme
            # TODO: should this be here?            
            parser_lookup = etree.ElementDefaultClassLookup(element=AccessibleTree)
            parser = etree.XMLParser()
            parser.set_element_class_lookup(parser_lookup)

        return cls._singleInstance
    
    def __init__(self, element = None, file = None, mapping = None):
        ElementTree.__init__(self, element, file)
        assert(mapping != None)
        self.mapping = mapping
        
    def getOsSpec(self, num):
        return self.mapping[num]
    
