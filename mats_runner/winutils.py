import win32gui

def getNightlies():
    result = []
    def getNightliesCallback(hwnd, res):
        title = win32gui.GetWindowText(hwnd)
        if 'Nightly' in title:
            res.append( (hwnd, title))
    win32gui.EnumWindows(getNightliesCallback, result)
    return result