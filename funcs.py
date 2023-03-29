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

def get_window(window_id):
    window_rect = win32gui.GetWindowRect(window_id)
    window_placement = win32gui.GetWindowPlacement(window_id)
    window = {
        "id"        : window_id,
        "title"     : win32gui.GetWindowText(window_id),
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
    windows = {}
    def enum_windows(window_id, extra):
        if win32gui.IsWindowVisible(window_id):
            window_text = win32gui.GetWindowText(window_id)
            if window_text != "" and window_text not in IGNORED_WINDOWS:
                window = get_window(window_id)
                if window["normal"]:
                    windows[window_id] = window
    win32gui.EnumWindows(enum_windows, None)
    windows = dict(sorted(windows.items(), key=lambda item: item[1]["title"].lower()))
    return windows

def resize_window(window_id, width, height):
    window = get_window(window_id)
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

def find_treeview_item_id_by_window_id(item_window_map, window_id):
    item_id = None
    for map_item_id, map_window in item_window_map.items():
        if map_window["id"] == window_id:
            item_id = map_item_id
            break
    return item_id

def clear_invalid_windows(treeview, windows, item_window_map, delete_selected_callback=None):
    children = treeview.get_children()
    for item_id in children:
        old_window = item_window_map.get(item_id, None)
        if old_window:
            new_window = windows.get(old_window["id"], None)
            if new_window is None:
                treeview.delete(item_id)
                del item_window_map[item_id]
                if delete_selected_callback:
                    delete_selected_callback()

def populate_treeview_with_windows(treeview, item_window_map = {}, delete_selected_callback=None):
    windows = get_windows()
    clear_invalid_windows(treeview, windows, item_window_map, delete_selected_callback)
    for window_id, window in windows.items():
        item_id = find_treeview_item_id_by_window_id(item_window_map, window_id)
        if item_id:
            treeview.item(item_id, values=(window['width'], window['height']))
        else:
            item_id = treeview.insert('', 'end', text=window["title"], values=(
                window['width'],
                window['height'],
            ))
            item_window_map[item_id] = window
    return item_window_map

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
