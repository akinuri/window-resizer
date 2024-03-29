import tkinter
import tkinter.ttk
import tkinter.messagebox
from funcs import *

# pip install tk
# pip install win32gui


#region ==================== APP WINDOW

window = tkinter.Tk()
window.title('Window Resizer')
window.resizable(False, False)
style = tkinter.ttk.Style(window)
style.theme_use('clam')

def window_click_handler(event):
    if isinstance(event.widget, tkinter.Tk):
        window.focus()

window.bind("<ButtonRelease-1>", window_click_handler)

def handle_size_inputs_on_item_delete():
    global previous_selected_item
    set_size_inputs(
        width_input,
        height_input,
    )
    previous_selected_item = None

windows_refresh_delay = 1000
def after_tick_handler():
    global item_window_map
    item_window_map = populate_treeview_with_windows(treeview, item_window_map, handle_size_inputs_on_item_delete)
    window.after(windows_refresh_delay, after_tick_handler)

window.after(windows_refresh_delay, after_tick_handler)

#endregion


#region ==================== WINDOWS LIST

windows_frame = tkinter.Frame(window)

treeview = tkinter.ttk.Treeview(
    windows_frame,
    columns=('Width', 'Height', 'Scroll'),
    selectmode="browse",
    height=8,
)
treeview.grid(row=1)

treeview.heading('#0', text='Window')
treeview.heading('Width', text='Width')
treeview.heading('Height', text='Height')
treeview.heading('Scroll', text='')

treeview.column('#0', width=250)
treeview.column('Width', width=50)
treeview.column('Height', width=50)
treeview.column('Scroll', width=20)

vsb = tkinter.ttk.Scrollbar(windows_frame, orient="vertical", command=treeview.yview)
vsb.place(relx=0.95, rely=0, relheight=1, relwidth=0.05)
treeview.configure(yscrollcommand=vsb.set)

item_window_map = populate_treeview_with_windows(treeview)

def treeview_click_handler(event):
    global previous_selected_item
    selected_item = get_selected_treeview_item(treeview)
    if selected_item == previous_selected_item:
        for item in treeview.selection():
            treeview.selection_remove(item)
        set_size_inputs(
            width_input,
            height_input,
        )
        previous_selected_item = None
    elif selected_item:
        set_size_inputs(
            width_input,
            height_input,
            selected_item["values"][0],
            selected_item["values"][1],
        )
        previous_selected_item = selected_item
    common_listbox.selection_clear(0, tkinter.END)
    custom_listbox.selection_clear(0, tkinter.END)
    handle_apply_button_state(
        treeview,
        width_input,
        height_input,
        apply_button,
    )

previous_selected_item = None
treeview.bind("<ButtonRelease-1>", treeview_click_handler)

windows_frame.pack(anchor="w", padx=10, pady=10)

#endregion


#region ==================== BOTTOM FRAME

bottom_frame = tkinter.Frame(window)

def frame_click_handler(event):
    if event.widget == bottom_frame or event.widget == size_frame:
        window.focus()
bottom_frame.bind("<ButtonRelease-1>", frame_click_handler)

#endregion


#region ==================== DIMENSIONS

# dimensions are hard-coded temporarily

common_dimensions = [
    [1920, 1080],
    [1600, 900],
    [1536, 864],
    [1440, 900],
    [1366, 768],
    [1280, 720],
    [1024, 768],
    [800, 600],
]

custom_dimensions = [
    
]

dimensions_listbox_height = max(len(common_dimensions), len(custom_dimensions))

#endregion


#region ==================== COMMON DIMENSIONS

common_listbox = tkinter.Listbox(
    bottom_frame,
    height=dimensions_listbox_height,
    font=('Consolas', 10),
    width=12,
    activestyle="none",
)

for index, dimension in enumerate(common_dimensions):
    common_listbox.insert(
        index + 1,
        "%s × %s" % (str(dimension[0]).rjust(4, " "), str(dimension[1]))
    )

def listbox_blur_handler():
    common_listbox.selection_clear(0, tkinter.END)
    custom_listbox.selection_clear(0, tkinter.END)
    window.focus()

def listbox_select_handler(event):
    selection = event.widget.curselection()
    width = ""
    height = ""
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        dim = data.split(" × ")
        width = dim[0]
        height = dim[1]
        set_size_inputs(
            width_input,
            height_input,
            width,
            height,
        )
        window.after(1000, listbox_blur_handler)
    handle_apply_button_state(
        treeview,
        width_input,
        height_input,
        apply_button,
    )

common_listbox.bind("<<ListboxSelect>>", listbox_select_handler)

common_listbox.pack(side="left")

#endregion


#region ==================== CUSTOM DIMENSIONS

custom_listbox = tkinter.Listbox(
    bottom_frame,
    height=dimensions_listbox_height,
    font=('Consolas', 10),
    width=12,
    activestyle="none",
)

for index, dimension in enumerate(custom_dimensions):
    custom_listbox.insert(
        index + 1,
        "%s × %s" % (str(dimension[0]).rjust(4, " "), str(dimension[1]))
    )

custom_listbox.bind("<<ListboxSelect>>", listbox_select_handler)

custom_listbox.pack(side="left", anchor="n", padx=(10, 0))

#endregion


#region ==================== SIZE APPLY

style.configure('padded.TEntry', padding=[5, 3, 5, 3])

size_frame = tkinter.Frame(bottom_frame)

size_frame.bind("<ButtonRelease-1>", frame_click_handler)

width_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
width_input.grid(row=1, column=1, padx=1, pady=2)

def width_input_key_handler(event):
    handle_apply_button_state(
        treeview,
        width_input,
        height_input,
        apply_button,
    )
width_input.bind("<KeyRelease>", width_input_key_handler)

height_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
height_input.grid(row=1, column=2, padx=1, pady=2)

def height_input_key_handler(event):
    handle_apply_button_state(
        treeview,
        width_input,
        height_input,
        apply_button,
    )
height_input.bind("<KeyRelease>", height_input_key_handler)

apply_button = tkinter.Button(
    size_frame,
    text="Apply",
    pady=2,
    padx=4,
    background="silver",
)

def apply_button_click_handler(event):
    global item_window_map
    if event.widget["state"] == "disabled":
        return
    selected_item = get_selected_treeview_item(treeview)
    if selected_item is None:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="No window selected.\n\nSelect a window before applying size.",
        )
        return
    selected_window = get_selected_window(treeview, item_window_map)
    if window is None:
        return
    if validate_entry_value(width_input, 200, 2000) is False:
        return
    if validate_entry_value(height_input, 200, 2000) is False:
        return
    width  = int(width_input.get())
    height = int(height_input.get())
    resize_window(selected_window["id"], width, height)
    treeview.item(get_selected_treeview_item(treeview, True), values=(width, height))

apply_button.bind("<ButtonRelease-1>", apply_button_click_handler)
handle_apply_button_state(
    treeview,
    width_input,
    height_input,
    apply_button,
)
apply_button.grid(sticky="e", row=2, column=1, columnspan=2, pady=(10, 0))

size_frame.pack(anchor="n", side="right", fill="x", padx=(0, 20))

#endregion


bottom_frame.pack(side="top", fill="x", padx=10, pady=(0, 10))


window.mainloop()
