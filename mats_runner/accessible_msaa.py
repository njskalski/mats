# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is born in frustration of COM in python. Welcome to code-glue hell.

#oh, btw, and guy who couln't have decided once if there should be one or two
#underscores after each 'com' infix - make up your mind!

from accessible import AccessibleElement

from ctypes import *
from comtypes.automation import IDispatch

def getAccessibleElementFromMsaa(msaa):
    res = AccessibleElement(getName(msaa))
    
def getName(msaa):
    #TODO unwrap it to native com call
    return msaa.accName()

def getChildrenCount(msaa):
    num_c = c_long()
    assert(msaa._IAccessible__com__accChildCount(byref(num_c)) == 0)
    return num_c.value

def getMsaaChild(msaa, childnum):
    '''
    I guess there is no difference if childnum is Integer or c_int/c_long here.
    '''
    ptr = POINTER(IDispatch)() #creating null pointer of IDispatch type
    msaa._IAccessible__com__getChild(childnum, byref(ptr)) #and passing it as **
    
    #_IAccessible__com__