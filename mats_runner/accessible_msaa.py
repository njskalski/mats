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
import comtypes
import ctypes
from ctypes import c_long, byref
from comtypes.automation import IDispatch, VARIANT, VT_I4, POINTER, VT_DISPATCH, BSTR
import winconstants

def intToVariant(i):
    v = VARIANT()
    v.vt = VT_I4
    v.value = i
    assert( isinstance(i, int) )
    return v

def getAccessibleTreeFromMsaa(root):
    return AccessibleTree(getAccessibleElementFromMsaa(root, winconstants.CHILDID_SELF))

def getAccessibleElementFromMsaa(node, id):
    print (node, id)
    
    res = AccessibleElement(os_spec = ( node, id ),
                            attrib = {
                                      'name' : getName(node, id),
                                      'description' : getDescription(node, id),
                                      'role' : getRole(node, id),
                                      'default-action' : getDefaultAction(node,id),
                                      })
    
    location = getLocation(node, id)
    for k, v in location.iteritems():
        res.set(k, v)
            
    children = getMsaaChildren(node, id)
    
    res.extend([getAccessibleElementFromMsaa(node, id) for (node, id) in children])
            
    return res

def getRole(node, id):
    variant = intToVariant(id)
    res = VARIANT(0, VT_I4)
    HRESULT = node._IAccessible__com__get_accRole(variant, byref(res))
    if HRESULT == comtypes.hresult.S_OK:
        return str(res.value) #TODO map it to string 
    elif HRESULT == comtypes.hresult.E_INVALIDARG:
        raise Exception("Invalid argument")
    else:
        raise Exception("Unexpected behavior")
    
def getLocation(node, id):
    variant = intToVariant(id)
    res = [c_long(), c_long(), c_long(), c_long()] #left, top, width, height
    HRESULT = node._IAccessible__com_accLocation(byref(res[0]),
                                                  byref(res[1]),
                                                  byref(res[2]),
                                                  byref(res[3]),
                                                  variant)
    if HRESULT == comtypes.hresult.S_OK:
        return {'left'      : str(res[0].value),
                'top'       : str(res[1].value), 
                'width'     : str(res[2].value),
                'height'    : str(res[3].value)
                }
    elif HRESULT == comtypes.hresult.S_FALSE:
        return {}
    elif HRESULT == comtypes.hresult.DISP_E_MEMBERNOTFOUND:
        return {}
    elif HRESULT == comtypes.hresult.E_INVALIDARG:
        raise Exception("Invalid argument")
    else:
        raise Exception("Unexpected behavior: " + str(HRESULT))
    
def getDefaultAction(node, id):
    variant = intToVariant(id)
    s = BSTR()    
    
    HRESULT = node._IAccessible__com__get_accDefaultAction(variant, byref(s))
    
    if HRESULT == comtypes.hresult.S_OK:
        return s.value
    elif HRESULT == comtypes.hresult.S_FALSE:
        return None
    elif HRESULT == comtypes.hresult.DISP_E_MEMBERNOTFOUND:
        return None
    elif HRESULT == comtypes.hresult.E_INVALIDARG:
        raise Exception("Invalid argument")
    else:
        raise Exception("Unexpected behavior: " + str(HRESULT))
    
def getName(node, id):
    s = BSTR()
        
    variant = VARIANT(id, VT_I4)

    HRESULT = node._IAccessible__com__get_accName(variant, byref(s))
  
    if HRESULT == comtypes.hresult.S_OK:
        return s.value
    elif HRESULT == comtypes.hresult.S_FALSE:
        return None
    elif HRESULT == comtypes.hresult.E_INVALIDARG:
        raise Exception("Argument not valid")
    else:
        raise Exception("Function output not valid!")
    
def getDescription(node, id):
    if id != winconstants.CHILDID_SELF: #TODO not sure if that's correct
        return None
    else:
        s = BSTR()
        variant = intToVariant(id)
        HRESULT = node._IAccessible__com__get_accDescription(variant, byref(s))
          
        if HRESULT == comtypes.hresult.S_OK:
            return s.value
        elif HRESULT == comtypes.hresult.S_FALSE:
            return None
        elif HRESULT == comtypes.hresult.E_INVALIDARG:
            raise Exception("Arguemnt not valid")
        elif HRESULT == DISP_E_MEMBERNOTFOUND:
            raise Exception("Member not found, node = " + str(node) + " id = " + str(id) + ".")
        
def getChildCount(node, id):
    if id != winconstants.CHILDID_SELF:
        return 0 #leaves have no children
    else:
                
        num_c = ctypes.wintypes.LONG()
        HRESULT = node._IAccessible__com__get_accChildCount(byref(num_c))
        
        if HRESULT == comtypes.hresult.S_OK:
            return num_c.value
        else:
            raise Exception("Some unimplemented error")

def getMsaaChildren(node, id):
    if id != winconstants.CHILDID_SELF:
        return [] #leaves have no chlidren
    else:   
        numChildren = getChildCount(node, id)
        array = (VARIANT * numChildren)()
        rescount = c_long()
                
        HRESULT1 = comtypes.oledll.oleacc.AccessibleChildren(node, 0, numChildren, array, byref(rescount))
        
        if HRESULT1 == comtypes.hresult.E_INVALIDARG:
            raise Exception("Invalid argument")
        elif HRESULT1 == comtypes.hresult.S_FALSE:
            raise Exception("The function succeeded, but there are fewer elements in the array than requested.")
        
        assert(numChildren == rescount.value)
        
        children = [(x.value, winconstants.CHILDID_SELF) if x.vt == VT_DISPATCH else (node, x.value) for x in array] #see comment in the beginnning of the file        
        
        return children 
