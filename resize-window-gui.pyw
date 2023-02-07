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
        for item in treeview.selection():
            treeview.selection_remove(item)
        reset_size_inputs(
            width_input,
            height_input,
            apply_button,
        )

window.bind("<ButtonRelease-1>", window_click_handler)

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

populate_treeview_with_windows(treeview)

def treeview_click_handler(event):
    global previous_selected_item
    selected_item = get_selected_treeview_item(treeview)
    if selected_item == previous_selected_item:
        for item in treeview.selection():
            treeview.selection_remove(item)
        reset_size_inputs(
            width_input,
            height_input,
            apply_button,
        )
        previous_selected_item = None
    else:
        reset_size_inputs(
            width_input,
            height_input,
            apply_button,
        )
        width_input.insert(0, selected_item["values"][0])
        height_input.insert(0, selected_item["values"][1])
        apply_button["state"] = "normal"
        previous_selected_item = selected_item

previous_selected_item = None
treeview.bind("<ButtonRelease-1>", treeview_click_handler)

windows_frame.pack(anchor="w", padx=10, pady=10)

#endregion


#region ==================== SIZE APPLY

style.configure('padded.TEntry', padding=[5, 3, 5, 3])

size_frame = tkinter.Frame(window)

width_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
width_input.grid(row=1, column=1, padx=1, pady=2)

def width_input_key_handler(event):
    if width_input.get() == "":
        apply_button["state"] = "disabled"
    else:
        apply_button["state"] = "normal"
width_input.bind("<KeyRelease>", width_input_key_handler)

height_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
height_input.grid(row=1, column=2, padx=1, pady=2)

def height_input_key_handler(event):
    if height_input.get() == "":
        apply_button["state"] = "disabled"
    else:
        apply_button["state"] = "normal"
height_input.bind("<KeyRelease>", height_input_key_handler)

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
    selected_window = get_selected_treeview_item(treeview)
    if selected_window is None:
        tkinter.messagebox.showwarning(
            title="Warning",
            message="No window selected.\n\nSelect a window before applying size.",
        )
        return
    if validate_entry_value(width_input, 200, 2000) is False:
        return
    if validate_entry_value(height_input, 200, 2000) is False:
        return
    width  = int(width_input.get())
    height = int(height_input.get())
    resize_window(selected_window["text"], width, height)
    treeview.item(get_selected_treeview_item(treeview, True), values=(width, height))

apply_button.bind("<ButtonRelease-1>", apply_button_click_handler)
apply_button["state"] = "disabled"
apply_button.grid(sticky="e", row=2, column=1, columnspan=2, pady=(5, 0))

size_frame.pack(anchor="e", padx=10, pady=(0, 10))

#endregion


window.mainloop()
