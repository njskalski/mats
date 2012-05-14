import win32gui
import ctypes
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

def getWindowsByName(name):
    result = []
    def getNightliesCallback(hwnd, res):
        title = win32gui.GetWindowText(hwnd)
        if name in title:
            res.append( (hwnd, title))
    win32gui.EnumWindows(getNightliesCallback, result)
    return result

def getNightlies():
    return getWindowsByName('Nightly')

def getAccessibleObjectFromWindow(hwnd):
    ptr = ctypes.POINTER(comtypes.gen.Accessibility.IAccessible)()
    res = ctypes.oledll.oleacc.AccessibleObjectFromWindow(
        hwnd,
        0,
        ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
        ctypes.byref(ptr))
    return ptr
