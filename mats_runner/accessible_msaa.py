# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is born in frustration of COM in python. Welcome to code-glue hell.

#oh, btw, and guy who couln't have decided once if there should be one or two
#underscores after each 'com' infix - make up your mind!

from accessible import AccessibleElement

from ctypes import *
from comtypes import BSTR
from comtypes.automation import IDispatch, VARIANT, VT_I4
import winconstants

def getAccessibleElementFromMsaa(msaa):        
    res = AccessibleElement({'name': getName(msaa)})
        
    children = getMsaaChildren(msaa)
    res.extend([getAccessibleElementFromMsaa(child) for child in children])
        
    return res
    
def getName(msaa):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    if msaa._IAccessible__com__get_accName(variant, byref(s)) == 0:
        return s.value
    else:
        return None

def getChildCount(msaa):
    num_c = c_long()
    assert(msaa._IAccessible__com__get_accChildCount(byref(num_c)) == 0)
    return num_c.value

def getMsaaChildren(msaa):
    numChildren = getChildCount(msaa)
    array = (VARIANT * numChildren)()
    rescount = c_long()
    oledll.oleacc.AccessibleChildren(msaa, 0, numChildren, array, byref(rescount))
    assert(numChildren == rescount.value)
    
    print [x.value for x in array]
    return []
