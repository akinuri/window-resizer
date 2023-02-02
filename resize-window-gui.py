import tkinter as tk
import tkinter.ttk as ttk
import win32gui

ignored_windows = [
    "Program Manager",
    "Microsoft Text Input Application",
]

window = tk.Tk()
window.title('Window Resizer')

s = ttk.Style()
s.theme_use('clam')

tree = ttk.Treeview(window, columns=('Width', 'Height', "X", "Y"))
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

tree.pack()

window.mainloop()
