import sys
import win32gui
import time

print("Select the window you want to resize")
print("")

open_windows = []

def callback(window, extra):
    if win32gui.IsWindowVisible(window):
        window_text = win32gui.GetWindowText(window)
        if window_text != "":
            open_windows.append(window_text)
win32gui.EnumWindows(callback, None)

index_length = len(str(len(open_windows)))

for i, title in enumerate(open_windows):
    print((str(i + 1) + " ").ljust(index_length + 2, " ") + title)

print("")

user_choice_window = input("Your window choice (enter the number): ")
user_choice_window = int(user_choice_window)

if (0 < user_choice_window and user_choice_window < len(open_windows) + 2) is False:
    print("Invalid choice: " + str(user_choice_window))
    print("Program is closing.")
    time.sleep(2)
    sys.exit()

print("")

user_choice_size = input("The new size for the window (enter two space seperated numbers): ")
user_choice_size = user_choice_size.split(" ")
user_choice_size = [int(size) for size in user_choice_size]

if len(user_choice_size) != 2:
    print("Invalid size: " + " ".join(user_choice_size))
    print("Program is closing.")
    time.sleep(2)
    sys.exit()

for size in user_choice_size:
    if (100 < size and size < 4000) is False:
        print("Size is out of bounds: " + "100 < %s < 4000" % str(size))
        print("Program is closing.")
        time.sleep(2)
        sys.exit()

window_select = open_windows[user_choice_window - 1]

window_id = win32gui.FindWindowEx(None, None, None, window_select)
window_rect = win32gui.GetWindowRect(window_id)
window_rect = {
    "x"      : window_rect[0],
    "y"      : window_rect[1],
    "width"  : window_rect[2] - window_rect[0],
    "height" : window_rect[3] - window_rect[1],
}

new_size = {
    "width"  : user_choice_size[0],
    "height" : user_choice_size[1],
}
size_offset = {
    "width"  : 0,
    "height" : 0,
}
size_scale = {
    "width"  : 1,
    "height" : 1,
}

new_size_calc = {
    "width"  : int((new_size["width"]  + size_offset["width"])  * size_scale["width"]),
    "height" : int((new_size["height"] + size_offset["height"]) * size_scale["height"]),
}

win32gui.MoveWindow(
    window_id,
    window_rect["x"],
    window_rect["y"],
    new_size_calc["width"],
    new_size_calc["height"],
    True,
)

print("")
print("The window has been resized.")

print("")
print("Program is closing.")
time.sleep(2)
sys.exit()
