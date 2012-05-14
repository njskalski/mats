import win32gui
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.client
import winconstants
from time import sleep

from threading import Thread, Lock

class ListenerThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._active = True
        self._activeLock = Lock()
        
        #http://msdn.microsoft.com/en-us/library/windows/desktop/aa383751%28v=vs.85%29.aspx
        self.callback_function_prototype = ctypes.WINFUNCTYPE(
            #first argument is THE RETURN TYPE as in documentation of ctypes.
            None,
            #now here are the real arguments
            ctypes.wintypes.HANDLE, #hWinEventHook, actually HWINEVENTHOOK, which is defined as HANDLE in WinNT.h
            ctypes.wintypes.DWORD, #event
            ctypes.wintypes.HWND, #hwnd
            ctypes.wintypes.LONG, #idObject
            ctypes.wintypes.LONG, #idChild
            ctypes.wintypes.DWORD, #dwEventThread
            ctypes.wintypes.DWORD, #dwmsEventTime
            )
        
        print dir(self.callback_function_prototype)
        
        self.callback_function = self.callback_function_prototype(WinEventProc)
        print dir(self.callback_function)
        print 'callback res:' + str(self.callback_function.restype)
        print 'callback args:' + str(self.callback_function.argtypes)
    
    def run(self):
        print 'Starting Listener'
        #http://msdn.microsoft.com/en-us/library/windows/desktop/dd373640%28v=vs.85%29.aspx
        self.callback_function_hook = ctypes.windll.user32.SetWinEventHook(
            ctypes.wintypes.UINT(winconstants.eventNameToInt['EVENT_MIN']),
            ctypes.wintypes.UINT(winconstants.eventNameToInt['EVENT_MAX']),
            ctypes.wintypes.UINT(0),
            self.callback_function,
            ctypes.wintypes.UINT(0), # 0 means all processes #TODO narrow that
            ctypes.wintypes.UINT(0), # 0 means all threads
            ctypes.wintypes.UINT(winconstants.WINEVENT_OUTOFCONTEXT)
            )                                
        
        print 'callback function hook: ' + str(self.callback_function_hook)
        
        while True:
            with self._activeLock:
                if not self._active:
                    break
            win32gui.PumpWaitingMessages() #TODO rethink that
            sleep(2)
            #print('e'),
        print ''
        
        unhook_result = ctypes.windll.user32.UnhookWinEvent(self.callback_function_hook)
        print "Unhooking result: " + str(ctypes.c_bool(unhook_result))
        
    def stop(self):
        '''
        This is called by a separate thread!
        '''
        with self._activeLock:
            self._active = False
        
        self.join(20) #TODO think this down
        print 'Listener stopped'
    
#http://msdn.microsoft.com/en-us/library/windows/desktop/dd373885%28v=vs.85%29.aspx    
def WinEventProc(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    if event in winconstants.eventIntToName.keys():
        print winconstants.eventIntToName[event]
    else:
        print '.',

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

def getProcessFromHwnd(hwnd):
    return ctypes.oledll.oleacc.GetProcessHandleFromHwnd(ctypes.wintypes.HWND(hwnd))

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
