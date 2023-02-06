import win32gui
import math
import tkinter


#region ==================== WINDOW

IGNORED_WINDOWS = [
    "Default IME",
    "Microsoft Text Input Application",
    "Program Manager",
]

def get_window(window_title):
    window_id   = win32gui.FindWindowEx(None, None, None, window_title)
    window_rect = win32gui.GetWindowRect(window_id)
    window = {
        "id"     : window_id,
        "title"  : window_title,
        "x"      : window_rect[0],
        "y"      : window_rect[1],
        "width"  : window_rect[2] - window_rect[0],
        "height" : window_rect[3] - window_rect[1],
    }
    return window

def get_windows():
    windows = []
    def enum_windows(window, extra):
        if win32gui.IsWindowVisible(window):
            window_text = win32gui.GetWindowText(window)
            if window_text != "" and window_text not in IGNORED_WINDOWS:
                window = get_window(window_text)
                windows.append(window)
    win32gui.EnumWindows(enum_windows, None)
    return windows

def resize_window(window_title, width, height):
    window = get_window(window_title)
    win32gui.MoveWindow(
        window["id"],
        window["x"],
        window["y"],
        width,
        height,
        True,
    )

#endregion


#region ==================== TREE VIEW

def populate_treeview_with_windows(treeview):
    windows = get_windows()
    for window in windows:
        treeview.insert('', 'end', text=window["title"], values=(
            window['width'],
            window['height'],
        ))

#endregion


#region ==================== INT

def get_int_validity(value, min=-math.inf, max=math.inf):
    validity = {
        "is_valid"  : None,
        "is_empty"  : value == "",
        "is_nan"    : None,
        "underflow" : None,
        "overflow"  : None,
    }
    try:
        value = int(value)
    except ValueError:
        validity["is_nan"] = True
    if validity["is_nan"] is not True:
        if (min < value) is False:
            validity["underflow"] = True
        if (value < max) is False:
            validity["overflow"] = True
    checks = [
        validity["is_empty"],
        validity["is_nan"],
        validity["underflow"],
        validity["overflow"],
    ]
    validity["is_valid"] = all(c == None for c in checks)
    return validity

def validate_entry_value(entry, min=-math.inf, max=math.inf):
    value = entry.get()
    validity = get_int_validity(value, min, max)
    if validity["is_valid"] is False:
        if validity["is_empty"]:
            tkinter.messagebox.showwarning(
                title="Warning",
                message="The input box is empty.",
            )
            return False
        if validity["is_nan"]:
            tkinter.messagebox.showwarning(
                title="Warning",
                message="The entered value (%s) is not a number." % value,
            )
            return False
        if validity["underflow"] or validity["overflow"]:
            tkinter.messagebox.showwarning(
                title="Warning",
                message="Invalid value.\n\nThe value is out of range: [%d, %d]" % (min, max),
            )
            return False
    return True

#endregion
