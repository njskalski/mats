# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/. 

import win32gui
import win32process
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.client

ia2interfaceNames = [
    'IAccessible2',
    'IAccessibleAction',
    'IAccessibleApplication',
    'IAccessibleComponent',
    'IAccessibleEditableText',
    'IAccessibleHyperlink',
    'IAccessibleHypertext',
    'IAccessibleImage',
    'IAccessibleRelation',
    'IAccessibleTable',
    'IAccessibleTable2',
    'IAccessibleTableCell',
    'IAccessibleText',
    'IAccessibleValue',
    ]

def getIA2InterfacesFromModule(m):
    res = {}
    for name in ia2interfaceNames:
        iface = getattr(m, name)
        res[name] = iface
    return res

def loadIAccessible():
    '''
    Imports oleacc.dll into comtypes.gen namcespace, creating Accessibility
    sub-namespace along with IAccessible interface. Then returns a reference
    to IAccessible for further usage
    '''
    comtypes.client.GetModule('oleacc.dll')
    return comtypes.gen.Accessibility.IAccessible

def loadIAccessible2Module():
    '''
    Loads entire IAccessible2 API from ia2_api_all.tlb, and returns
    the entire gen MODULE (NOT just interface), since the module name is 
    generated weirdly
    '''
    comtypes.client.GetModule('../ia2_api_all.tlb')
    return comtypes.gen._C974E070_3787_490A_87B0_E333B06CA1E2_0_1_2

def getNightliesByPID(PID):
    result = []
    def getWindowCallback(hwnd, res):
        tmpPID = getPIDFromHWND(hwnd)
        if tmpPID == PID:
            title = win32gui.GetWindowText(hwnd)
            if 'Nightly' in title:
                res.append( (hwnd, title) )
    win32gui.EnumWindows(getWindowCallback, result)
    return result

def getPIDFromHWND(hwnd):
    TId, PId = win32process.GetWindowThreadProcessId(hwnd)
    return PId

def getAccessibleObjectFromWindow(hwnd):
    ptr = ctypes.POINTER(comtypes.gen.Accessibility.IAccessible)()
    res = ctypes.oledll.oleacc.AccessibleObjectFromWindow(
        hwnd,
        0,
        ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
        ctypes.byref(ptr))
    return ptr

def getAccessible2ObjectFromMSAA(msaa):
    ia = msaa
    ia2m = comtypes.gen._C974E070_3787_490A_87B0_E333B06CA1E2_0_1_2
    
    sp = ia.QueryInterface(comtypes.IServiceProvider)
    
    #void_ptr = ctypes.c_void_p()

    impls = [] 
    nif = getIA2InterfacesFromModule(ia2m)
    for name, iface in nif.iteritems():
        try:
          ugabugaggagagaga!
            impl = sp.QueryService(ia2m.IUnknown._iid_, iface)
            #impl = sp._IServiceProvider__com_QueryService(byref(iface._iid_))
            dir(sp)
            
            impls.append(impl)
            print "SUCCESS interface " + name + " is implemented."
        except Exception as e:
            if hasattr(e, 'text'):
                if e.text.startswith("No such interface supported"): #or\
                    #e.text.startswith("The parameter is incorrect."):
                    pass
                else:
                    print e
            #import pyshell 
            #pyshell.falle(e, {'sp' : sp, 'nif': nif })
            
    return impls
    

