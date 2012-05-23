# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/. 

import win32gui
import win32process
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.client

def loadIAccessible():
    '''
    Imports oleacc.dll into comtypes.gen namcespace, creating Accessibility
    sub-namespace along with IAccessible interface. Then returns a reference
    to IAccessible for further usage
    '''
    comtypes.client.GetModule('oleacc.dll')
    return comtypes.gen.Accessibility.IAccessible

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
