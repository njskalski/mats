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
                    
        res = AccessibleElement({'name': getName(node)})
            
        children = getMsaaChildren(node)
        res.extend([getAccessibleElementFromMsaa(child) for child in children])
            
        return res
    else:
        print node.__class__
        return AccessibleElement({'type' : str(node.__class__)})
    
def getName(node):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    if node._IAccessible__com__get_accName(variant, byref(s)) == 0:
        return s.value
    else:
        return 'error'

def getChildCount(node):
    num_c = c_long()
    assert(node._IAccessible__com__get_accChildCount(byref(num_c)) == 0)
    return num_c.value

def getMsaaChildren(node):
    numChildren = getChildCount(node)
    array = (VARIANT * numChildren)()
    rescount = c_long()
    comtypes.oledll.oleacc.AccessibleChildren(node, 0, numChildren, array, byref(rescount))
    assert(numChildren == rescount.value)
    
    return [x.value for x in array]
