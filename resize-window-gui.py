import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import win32gui

window = tk.Tk()
window.title('Window Resizer')
style = ttk.Style(window)
style.theme_use('clam')

#region ==================== WINDOWS LIST

windowsFrame = tk.Frame(window)
# windowsFrame.grid(row=0, column=0)

tree = ttk.Treeview(windowsFrame, columns=('Width', 'Height', "X", "Y"))
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
def callback(window, extra):
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
win32gui.EnumWindows(callback, None)

windowsFrame.pack(anchor="w", padx=10, pady=(10, 0))

#endregion

#region ==================== SIZE APPLY

style.configure('padded.TEntry', padding=[5, 3, 5, 3])

sizeFrame = tk.Frame(window)
# sizeFrame.grid(row=0, column=0, padx=10, pady=5)

widthLabel = tk.Label(sizeFrame, text="Width").grid(sticky="W", row=1, column=0, padx=(0, 10))
widthInput = ttk.Entry(sizeFrame, style='padded.TEntry').grid(row=1, column=1, pady=2)

heightLabel = tk.Label(sizeFrame, text="Height").grid(sticky="W", row=2, column=0, padx=(0, 10))
heightInput = ttk.Entry(sizeFrame, style='padded.TEntry').grid(row=2, column=1, pady=2)

applyButton = tk.Button(
    sizeFrame,
    text="Apply",
    pady=2,
    padx=4,
    background="silver",
).grid(sticky="e", row=3, columnspan=2, pady=(5, 0))

sizeFrame.pack(anchor="e", padx=(0, 10), pady=10)

#endregion

window.mainloop()
