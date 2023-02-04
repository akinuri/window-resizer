import tkinter
import tkinter.ttk
import tkinter.messagebox
import win32gui

window = tkinter.Tk()
window.title('Window Resizer')
style = tkinter.ttk.Style(window)
style.theme_use('clam')

#region ==================== WINDOWS LIST

windows_frame = tkinter.Frame(window)
# windows_frame.grid(row=0, column=0)

tree = tkinter.ttk.Treeview(
    windows_frame,
    columns=('Width', 'Height', "X", "Y"),
    selectmode="browse",
)
tree.grid(row=1)
tree.heading('#0', text='Window')
tree.heading('Width', text='Width')
tree.heading('Height', text='Height')
tree.heading('X', text='X')
tree.heading('Y', text='Y')

tree.column('#0', width=400)
tree.column('Width', width=100)
tree.column('Height', width=100)
tree.column('X', width=50)
tree.column('Y', width=50)

ignored_windows = [
    "Program Manager",
    "Microsoft Text Input Application",
]
def enum_windows(window, extra):
    if win32gui.IsWindowVisible(window):
        window_text = win32gui.GetWindowText(window)
        if window_text != "" and window_text not in ignored_windows:
            window_id = win32gui.FindWindowEx(None, None, None, window_text)
            window_rect = win32gui.GetWindowRect(window_id)
            window = {
                "title"  : window_text,
                "x"      : window_rect[0],
                "y"      : window_rect[1],
                "width"  : window_rect[2] - window_rect[0],
                "height" : window_rect[3] - window_rect[1],
            }
            tree.insert('', 'end', text=window_text, values=(
                window['width'],
                window['height'],
                window['x'],
                window['y'],
            ))
win32gui.EnumWindows(enum_windows, None)

def tree_click_handler(event):
    selected_item = get_selected_window()
    if selected_item is not None:
        apply_button["state"] = "normal"
        width_input.delete(0, tkinter.END)
        height_input.delete(0, tkinter.END)
        width_input.insert(0, selected_item["values"][0])
        height_input.insert(0, selected_item["values"][1])

tree.bind("<ButtonRelease-1>", tree_click_handler)

windows_frame.pack(anchor="w", padx=10, pady=(10, 0))

def get_selected_window():
    selected_item_id = tree.focus()
    if selected_item_id == "":
        return None
    return tree.item(selected_item_id)

#endregion

#region ==================== SIZE APPLY

style.configure('padded.TEntry', padding=[5, 3, 5, 3])

size_frame = tkinter.Frame(window)
# size_frame.grid(row=0, column=0, padx=10, pady=5)

width_label = tkinter.Label(size_frame, text="Width")
width_label.grid(sticky="W", row=1, column=0, padx=(0, 10))
width_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry')
width_input.grid(row=1, column=1, pady=2)

height_label = tkinter.Label(size_frame, text="Height")
height_label.grid(sticky="W", row=2, column=0, padx=(0, 10))
height_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry')
height_input.grid(row=2, column=1, pady=2)

apply_button = tkinter.Button(
    size_frame,
    text="Apply",
    pady=2,
    padx=4,
    background="silver",
)

def apply_button_click_handler(event):
    if event.widget["state"] == "disabled":
        return
    selected_window = get_selected_window()
    if selected_window is None:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="No window selected.\n\nSelect a window before applying size.",
        )
    width  = width_input.get()
    height = height_input.get()
    if width == "":
        tkinter.messagebox.showwarning(
            title="Warning",
            message="The width input box is empty.",
        )
        return
    if height == "":
        tkinter.messagebox.showwarning(
            title="Warning",
            message="The height input box is empty.",
        )
        return
    try:
        width = int(width)
    except ValueError:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="The entered value for width is not a number.",
        )
        return
    try:
        height = int(height)
    except ValueError:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="The entered value for height is not a number.",
        )
        return
    if (200 < width < 2000) is False:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="Invalid width.\n\nThe width is out of range: [200, 2000]",
        )
        return
    if (200 < height < 2000) is False:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="Invalid height.\n\nThe width is out of range: [200, 2000]",
        )
        return
    resize_window(selected_window["text"], width, height)
    width_input.delete(0, tkinter.END)
    height_input.delete(0, tkinter.END)
    tree.delete(*tree.get_children())
    win32gui.EnumWindows(enum_windows, None)

def resize_window(window_title, width, height):
    window_id = win32gui.FindWindowEx(None, None, None, window_title)
    window_rect = win32gui.GetWindowRect(window_id)
    window_rect2 = {
        "x"      : window_rect[0],
        "y"      : window_rect[1],
        "width"  : window_rect[2] - window_rect[0],
        "height" : window_rect[3] - window_rect[1],
    }
    win32gui.MoveWindow(
        window_id,
        window_rect2["x"],
        window_rect2["y"],
        width,
        height,
        True,
    )

apply_button.bind("<ButtonRelease-1>", apply_button_click_handler)
apply_button["state"] = "disabled"
apply_button.grid(sticky="e", row=3, columnspan=2, pady=(5, 0))

size_frame.pack(anchor="e", padx=(0, 10), pady=10)

#endregion

window.mainloop()
