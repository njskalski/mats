# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

#http://forums.codeguru.com/showthread.php?t=392273 - usefull 

import win32gui
import win32process
import ctypes
import ctypes.wintypes
import comtypes
import comtypes.client
import winconstants
import event

from threading import Lock


class WindowsListener(object):
    _singleInstance = None
    
    # WindowsListener needs to be global (singleton pattern), since
    # WinEventProc cannot receive additional 'self' argument, so it
    # cannot be bound with a particular object instance.
    # Sorry, MS discovered delegates 10 years later.
    def __new__(cls, *args, **kwargs):
        if not cls._singleInstance:
            cls._singleInstance = super(WindowsListener, cls).__new__(
                                cls, *args, **kwargs)
        return cls._singleInstance
    
    def __init__(self, hwnd, pid):
        
        self.hwnd = hwnd
        self.pid = pid
         
        self._tmpQueue = []
        
        #TODO this lock can be removed, provided that PumpWaitingMessages returns AFTER all WinProc calls
        self._tmpQueueLock = Lock()
        
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
        
    def start(self):
        '''
        registers listener
        '''
        
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
        
    def stop(self):
        unhook_result = ctypes.windll.user32.UnhookWinEvent(self.callback_function_hook)
        print "Unhooking result: " + str(ctypes.c_bool(unhook_result))
        
    def pump_messages(self):
        win32gui.PumpWaitingMessages() #TODO rethink that
        
    def block_until_message(self): #TODO test that!
        win32gui.WaitMessage()
        
    def put_event_in_tmp_queue(self, event):
        '''
        Blocking function, thread safe adding events to temporary Queue, local to WindowsListener.
        '''
        with self._tmpQueueLock:
            self._tmpQueue.append(event)
            
    def get_queued_events(self):
        '''
        Blocking function, thread safe adding events to temporary Queue, local to WindowsListener.
        '''
        with self._tmpQueueLock:
            events = self._tmpQueue
            self._tmpQueue = []
        return events
            
#http://msdn.microsoft.com/en-us/library/windows/desktop/dd373885%28v=vs.85%29.aspx    
def WinEventProc(_hWinEventHook, _event, _hwnd, _idObject, _idChild, _dwEventThread, _dwmsEventTime):
    WindowsListener._singleInstance.put_event_in_tmp_queue(event.Event(
                                                            id = _event,
                                                            hwnd = _hwnd,
                                                            idObject = _idObject,
                                                            idChild = _idChild,
                                                            dwEventThread = _dwEventThread,
                                                            dwmsEventTime = _dwmsEventTime
                                                                      ))                                                          
