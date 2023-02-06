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

def tree_click_handler(event):
    selected_item = get_selected_window()
    if selected_item is not None:
        apply_button["state"] = "normal"
        width_input.delete(0, tkinter.END)
        height_input.delete(0, tkinter.END)
        width_input.insert(0, selected_item["values"][0])
        height_input.insert(0, selected_item["values"][1])

treeview.bind("<ButtonRelease-1>", tree_click_handler)

windows_frame.pack(anchor="w", padx=10, pady=10)

def get_selected_window():
    selected_item_id = treeview.focus()
    if selected_item_id == "":
        return None
    return treeview.item(selected_item_id)

#endregion


#region ==================== SIZE APPLY

style.configure('padded.TEntry', padding=[5, 3, 5, 3])

size_frame = tkinter.Frame(window)

width_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
width_input.grid(row=1, column=1, padx=1, pady=2)

height_input = tkinter.ttk.Entry(size_frame, style='padded.TEntry', width=6)
height_input.grid(row=1, column=2, padx=1, pady=2)

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
        return
    if validate_entry_value(width_input, 200, 2000) is False:
        return
    if validate_entry_value(height_input, 200, 2000) is False:
        return
    width  = int(width_input.get())
    height = int(height_input.get())
    resize_window(selected_window["text"], width, height)
    width_input.delete(0, tkinter.END)
    height_input.delete(0, tkinter.END)
    treeview.delete(*treeview.get_children())
    populate_treeview_with_windows(treeview)

apply_button.bind("<ButtonRelease-1>", apply_button_click_handler)
apply_button["state"] = "disabled"
apply_button.grid(sticky="e", row=2, column=1, columnspan=2, pady=(5, 0))

size_frame.pack(anchor="e", padx=10, pady=(0, 10))

#endregion


window.mainloop()
