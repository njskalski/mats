# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import win32gui
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.client
import winconstants
from time import sleep

from threading import Thread, Event

class NightlyWindowNotFoundException(Exception):
    pass

class ListenerThread(Thread):
    _singleInstance = None
    
    # ListenerThread needs to be global (singleton pattern), since
    # WinEventProc cannot receive additional 'self' argument, so it
    # cannot be bound with a particular object instance.
    # Sorry, MS discovered delegates 10 years later.
    def __new__(cls, *args, **kwargs):
        if not cls._singleInstance:
            cls._singleInstance = super(ListenerThread, cls).__new__(
                                cls, *args, **kwargs)
        return cls._singleInstance
    
    def __init__(self, hwnd, pid):
        Thread.__init__(self)
        
        self._activeEvent = Event()
        self.hwnd = hwnd
        self.pid = pid
        #self.processId = getProcessFromHwnd(self.hwnd)
        
        Listener = self
        
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
        
        self.callback_function = self.callback_function_prototype(WinEventProc)
        
    def run(self):
        print 'Starting Listener for process ' + str(self.pid)
        #http://msdn.microsoft.com/en-us/library/windows/desktop/dd373640%28v=vs.85%29.aspx
        self.callback_function_hook = ctypes.windll.user32.SetWinEventHook(
            ctypes.wintypes.UINT(winconstants.eventNameToInt['EVENT_MIN']),
            ctypes.wintypes.UINT(winconstants.eventNameToInt['EVENT_MAX']),
            None,#ctypes.wintypes.UINT(0), #null, since we use WINEVENT_OUTOFCONTEXT
            self.callback_function,
            ctypes.wintypes.DWORD(self.pid), #were watching only Nightly's process
            ctypes.wintypes.UINT(0), # 0 means all threads
            ctypes.wintypes.UINT(winconstants.WINEVENT_OUTOFCONTEXT)
            )                                
        
        print 'callback function hook: ' + str(self.callback_function_hook)
        
        self._activeEvent.set()
        while self._activeEvent.is_set():
            win32gui.PumpWaitingMessages() #TODO rethink that
            sleep(1)
    
        unhook_result = ctypes.windll.user32.UnhookWinEvent(self.callback_function_hook)
        print "Unhooking result: " + str(ctypes.c_bool(unhook_result))
    
    def wait_for_ready(self, timeout = None):
        self._activeEvent.wait(timeout)
    
    def stop(self):
        '''
        This is called by a separate thread!
        '''
        self._activeEvent.clear()   #shutting down the loop
        self.join(20)               #waiting ListenerThread to finish
        print 'Listener stopped'
    
#http://msdn.microsoft.com/en-us/library/windows/desktop/dd373885%28v=vs.85%29.aspx    
def WinEventProc(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    pass
#    if event in winconstants.eventIntToName.keys():
#        print winconstants.eventIntToName[event],
#    
#        if hwnd == ListenerThread._singleInstance.hwnd:
#            print '\t\t (HWND match)',
#        
#        print '\n'
#        return
#    
#    if hwnd == ListenerThread._singleInstance.hwnd:
#        print 'unknown event, but HWND matches'
    
    

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
    def getWindowCallback(hwnd, res):
        title = win32gui.GetWindowText(hwnd)
        if name in title:
            res.append( (hwnd, title) )
    win32gui.EnumWindows(getWindowCallback, result)
    return result

def getProcessFromHwnd(hwnd):
    return ctypes.oledll.oleacc.GetProcessHandleFromHwnd(hwnd)

def getNightlies():
    nightlies = getWindowsByName('Nightly') 
    if len(nightlies) > 0:
        return nightlies
    else: 
        raise NightlyWindowNotFoundException("Nightly window not found")

def getAccessibleObjectFromWindow(hwnd):
    ptr = ctypes.POINTER(comtypes.gen.Accessibility.IAccessible)()
    res = ctypes.oledll.oleacc.AccessibleObjectFromWindow(
        hwnd,
        0,
        ctypes.byref(comtypes.gen.Accessibility.IAccessible._iid_),
        ctypes.byref(ptr))
    return ptr
