import win32gui
import ctypes
import comtypes
import comtypes.client
import winconstants
from time import sleep

from threading import Thread, Lock

class ListenerThread(Thread):
    def __init__(self):
        self._active = True
        self._activeLock = Lock()
        
        #http://msdn.microsoft.com/en-us/library/windows/desktop/aa383751%28v=vs.85%29.aspx
        self.callback_function_prototype = ctypes.CFUNCTYPE(
            ctypes.c_voidp, #hWinEventHook, actually HWINEVENTHOOK, which is defined as HANDLE in WinNT.h = void*
            ctypes.c_uint32, #event, actually DWORD
            ctypes.c_uint32, #hwnd
            ctypes.c_int32, #idObject
            ctypes.c_int32, #idChild
            ctypes.c_uint32, #dwEventThread, actually DWORD
            ctypes.c_uint32, #dwmsEventTime, actually DWORD
            )
        self.callback_function = self.callback_function_prototype(WinEventProc)
    
    def run(self):
        print 'Starting Listener'
        #http://msdn.microsoft.com/en-us/library/windows/desktop/dd373640%28v=vs.85%29.aspx
        self.callback_function_hook = ctypes.windll.user32.SetWinEventHook(
            ctypes.c_uint32(winconstants.eventNameToInt['EVENY_MIN']),
            ctypes.c_uint32(winconstants.eventNameToInt['EVENY_MAX']),
            0,
            self.callback_function,
            0, # 0 means all processes #TODO narrow that
            0, # 0 means all threads
            winconstants.WINEVENT_OUTOFCONTEXT
            )                                
        
        while True:
            with self._activeLock:
                if not self._active:
                    break
            comtypes.client.PumpEvents(5) #TODO rethink that
            pass
        
    def stop(self):
        with self._activeLock:
            self._active = False
        
        unhook_result = ctypes.windll.user32.UnhookWinEvent(self.callback_function_hook)
        print "Unhooking result = " + str(unhook_result)
        self.join(20) #TODO think this down
        print 'Listener stopped'
    
#http://msdn.microsoft.com/en-us/library/windows/desktop/dd373885%28v=vs.85%29.aspx    
def WinEventProc(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    print str(event)

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
