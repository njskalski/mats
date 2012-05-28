# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#this file is born in frustration of COM in python. Welcome to code-glue hell.

#oh, btw, and guy who couln't have decided once if there should be one or two
#underscores after each 'com' infix - make up your mind!

# there are two important things to remeber while working with MSAA:
# 1) not every accessible node in tree is actually IAccessible. some of leafs in the tree
# are represented solely as an child_id to partent IAccessible, and do not implement the
# interface themself. In this implementation therefore, an AccessibleElement is identified
# as pair of (IAccessible , integer)
# 2) child_id is 1-based, 0 means "node itself". You know, just so you make more mistakes.

from accessible import AccessibleElement, AccessibleTree

import ctypes
from ctypes import c_long, byref
import comtypes
from comtypes import BSTR
from comtypes.automation import IDispatch, VARIANT, VT_I4, POINTER, VT_DISPATCH
import winconstants

def isMsaaNode(obj):
    return obj.__class__ == POINTER(comtypes.gen.Accessibility.IAccessible)

def intToVariant(i):
    return VARIANT(i, VT_I4)

def getAccessibleTreeFromMsaa(root):
    return AccessibleTree(getAccessibleElementFromMsaa(root))

def getAccessibleElementFromMsaa(node, id):
    res = AccessibleElement(os_spec = ( node, id ),
                            attrib = {
                                      'name' : getName(node),
                                      'description' : getDescription(node),
                                      })
            
    children = getMsaaChildren(node, id)
    res.extend([getAccessibleElementFromMsaa(child) for child in children])
            
    return res
    
def getName(node):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    HRESULT = node._IAccessible__com__get_accName(variant, byref(s))
    #TODO add HRESULT->error desription mapping?  
    if HRESULT == comtypes.hresult.S_OK:
        return s.value
    elif HRESULT == comtypes.hresult.S_FALSE:
        return None
    else:
        return 'HRESULT = ' + str(HRESULT)
    
def getDescription(node):
    s = BSTR()
    variant = VARIANT(c_long(winconstants.CHILDID_SELF),VT_I4)
    HRESULT = node._IAccessible__com__get_accDescription(variant, byref(s))
    #TODO add HRESULT->error desription mapping?  
    if HRESULT == comtypes.hresult.S_OK:
        return s.value
    elif HRESULT == comtypes.hresult.S_FALSE:
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
    
    HRESULT1 = comtypes.oledll.oleacc.AccessibleChildren(node, 0, numChildren, array, byref(rescount))
    
    if HRESULT1 == comtypes.hresult.E_INVALIDARG:
        raise Exception("Invalida argument")
    elif HRESULT1 == comtypes.hresult.S_FALSE:
        raise Exception("The function succeeded, but there are fewer elements in the array than requested.")
    
    assert(numChildren == rescount.value)
    
    #children = [x.value if x.vt == VT_DISPATCH else getMsaaChildFromId(node, x.value) for x in array]
    children = []
    for x in array:
        if x.vt == VT_DISPATCH:
            assert(isMsaaNode(x.value))
            children.append(x.value)
        elif x.vt == VT_I4:
            ch = getMsaaChildFromVariant(node, x)
            assert(isMsaaNonde(ch))
            children.append(ch)
    
    return children 

def getMsaaChildFromVariant(parent_node, variant):    
    ptr = POINTER(IDispatch)() #creating null pointer of IDispatch type    
    HRESULT1 = parent_node._IAccessible__com__get_accChild(variant, byref(ptr)) #and passing it as **

    if HRESULT1 == comtypes.hresult.S_FALSE:
        raise Exception("Not an accessible object: variant = " + str(variant) + ".")
    elif HRESULT1 == comtypes.hresult.E_INVALIDARG:
        raise Exception("Invalid argument") 
    
    res = POINTER(comtypes.gen.Accessibility.IAccessible)()
    HRESULT2 = ptr._IUnknown__com_QueryInterface(byref(comtypes.gen.Accessibility.IAccessible._iid_), byref(res))
    
    if HRESULT2 == comtypes.hresult.S_OK:
        return res
    else: #TODO some real exception handling
        print 'WARNING: integers still meaningless'
        return None