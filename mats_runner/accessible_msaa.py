# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is born in frustration of COM in python. Welcome to code-glue hell.

#oh, btw, and guy who couln't have decided once if there should be one or two
#underscores after each 'com' infix - make up your mind!

from accessible import AccessibleElement

from ctypes import *
from comtypes import BSTR
from comtypes.automation import IDispatch
import winconstants

def getAccessibleElementFromMsaa(msaa, IAccessible):
    res = AccessibleElement(getName(msaa))
    
    #functional programming frenzy!
    children = [getMsaaChild(msaa, i, IAccessible) for i in range(0, getChildCount(msaa))]
    res.extend([getAccessibleElementFromMsaa(child) for child in children])


def getName(msaa):
    s = BSTR()
    msaa._IAccessible__com__get_accName(winconstants.CHILDID_SELF, byref(s))
    return s.value
    #return msaa.accName()

def getChildCount(msaa):
    num_c = c_long()
    assert(msaa._IAccessible__com__get_accChildCount(byref(num_c)) == 0)
    return num_c.value

def getMsaaChild(msaa, childnum, IAccessible):
    '''
    I guess there is no difference if childnum is Integer or c_int/c_long here.
    '''
    ptr = POINTER(IDispatch)() #creating null pointer of IDispatch type
    msaa._IAccessible__com__get_accChild(childnum, byref(ptr)) #and passing it as **
    
    res = POINTER(IAccessible)()
    ptr._IUnknown__com_QueryInterface(byref(IAccessible._iid_), byref(res)) #the only thing worse
    #than dynamic programming, is dynamic programming with windows.
    
    return res