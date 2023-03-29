import win32gui
import win32con
import math
import tkinter


#region ==================== WINDOW

IGNORED_WINDOWS = [
    "Default IME",
    "Microsoft Text Input Application",
    "Program Manager",
    "Window Resizer",
]

def get_window(window_title):
    window_id   = win32gui.FindWindowEx(None, None, None, window_title)
    window_rect = win32gui.GetWindowRect(window_id)
    window_placement = win32gui.GetWindowPlacement(window_id)
    window = {
        "id"        : window_id,
        "title"     : window_title,
        "x"         : window_rect[0],
        "y"         : window_rect[1],
        "width"     : window_rect[2] - window_rect[0],
        "height"    : window_rect[3] - window_rect[1],
        "minimized" : window_placement[1] == win32con.SW_SHOWMINIMIZED,
        "maximized" : window_placement[1] == win32con.SW_SHOWMAXIMIZED,
        "normal"    : window_placement[1] == win32con.SW_SHOWNORMAL
    }
    return window

def get_windows():
    windows = []
    def enum_windows(window, extra):
        if win32gui.IsWindowVisible(window):
            window_text = win32gui.GetWindowText(window)
            if window_text != "" and window_text not in IGNORED_WINDOWS:
                window = get_window(window_text)
                if window["normal"]:
                    windows.append(window)
    win32gui.EnumWindows(enum_windows, None)
    windows = sorted(windows, key=lambda d: d["title"].lower()) 
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

def find_treeview_item(treeview, text):
    children = treeview.get_children()
    for child_id in children:
        child = treeview.item(child_id)
        if child["text"] == text:
            return child_id
    return None

def clear_closed_windows(treeview, windows, delete_selected_callback=None):
    children = treeview.get_children()
    for child_id in children:
        child = treeview.item(child_id)
        if child["text"] not in windows:
            treeview.delete(child_id)
            if delete_selected_callback:
                delete_selected_callback()

def populate_treeview_with_windows(treeview, delete_selected_callback=None):
    windows = get_windows()
    windows_titles = []
    for window in windows:
        windows_titles.append(window["title"])
        item = find_treeview_item(treeview, window["title"])
        if item:
            treeview.item(item, values=(window['width'], window['height']))
        else:
            treeview.insert('', 'end', text=window["title"], values=(
                window['width'],
                window['height'],
            ))
    clear_closed_windows(treeview, windows_titles, delete_selected_callback)

def get_selected_treeview_item(treeview, return_item_id=False):
    selected_item_id = (treeview.selection()[0:1] or (None,))[0]
    if return_item_id:
        return selected_item_id
    if selected_item_id:
        return treeview.item(selected_item_id)
    return None

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


#region ==================== SIZE

def set_size_inputs(
    width_input,
    height_input,
    width_value = "",
    height_value = "",
):
    width_input.delete(0, tkinter.END)
    height_input.delete(0, tkinter.END)
    if width_value != "":
        width_input.insert(0, width_value)
    if height_value != "":
        height_input.insert(0, height_value)

def handle_apply_button_state(
    treeview,
    width_input,
    height_input,
    apply_button,
):
    state = "disabled"
    if get_selected_treeview_item(treeview) is not None and width_input.get() != "" and height_input.get() != "":
        state = "normal"
    apply_button["state"] = state

#endregion
