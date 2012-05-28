# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is born in frustration of COM in python. Welcome to code-glue hell.

#oh, btw, and guy who couln't have decided once if there should be one or two
#underscores after each 'com' infix - make up your mind!

from accessible import AccessibleElement, AccessibleTree

import ctypes
from ctypes import c_long, byref
import comtypes
from comtypes import BSTR
from comtypes.automation import IDispatch, VARIANT, VT_I4, POINTER
import winconstants

def getAccessibleTreeFromMsaa(root):
    return AccessibleTree(getAccessibleElementFromMsaa(root))

def getAccessibleElementFromMsaa(node):
    if node.__class__ == POINTER(comtypes.gen.Accessibility.IAccessible):
                    
                    
        res = AccessibleElement(node, {
                                       'name' : getName(node),
                                       'description' : getDescription(node),
                                       })
            
        children = getMsaaChildren(node)
        res.extend([getAccessibleElementFromMsaa(child) for child in children])
            
        return res
    else:
        return AccessibleElement(None, {'type' : node.__class__.__name__})
    
def getName(node):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    HRESULT = node._IAccessible__com__get_accName(variant, byref(s))
    #TODO add HRESULT->error desription mapping?  
    if HRESULT == winconstants.S_OK:
        return s.value
    elif HRESULT == winconstants.S_FALSE:
        return None
    else:
        return 'HRESULT = ' + str(HRESULT)
    
def getDescription(node):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    HRESULT = node._IAccessible__com__get_accDescription(variant, byref(s))
    #TODO add HRESULT->error desription mapping?  
    if HRESULT == winconstants.S_OK:
        return s.value
    elif HRESULT == winconstants.S_FALSE:
        return None
    else:
        return 'HRESULT = ' + str(HRESULT)
    
    
def getChildCount(node):
    num_c = c_long()
    assert(node._IAccessible__com__get_accChildCount(byref(num_c)) == 0)
    return num_c.value

def getMsaaChildren(node):
    numChildren = getChildCount(node)
    array = (VARIANT * numChildren)()
    rescount = c_long()
    print comtypes.oledll.oleacc.AccessibleChildren(node, 0, numChildren, array, byref(rescount))
    assert(numChildren == rescount.value)
    
    print [str(x) for x in array] 
    return [x.value for x in array]
