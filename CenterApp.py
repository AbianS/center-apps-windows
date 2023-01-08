from PIL import Image
from pynput import keyboard
import ctypes
import pystray
import threading
import win32api
import win32con
import win32gui
import os
import webbrowser

def get_foreground_window_title():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value

def get_window_dimensions(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    return (width, height)

def center_window(hwnd):
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    window_width, window_height = get_window_dimensions(hwnd)
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)

    win32gui.SetWindowPos(hwnd, 0, int(x_coordinate), int(y_coordinate), 0, 0, win32con.SWP_NOSIZE)

def on_press(key):
    if key in combination:
        current.add(key)
        if all(k in current for k in combination):
            title = get_foreground_window_title()
            hwnd = win32gui.FindWindow(None, title)
            center_window(hwnd)

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

def listener_center_screen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def window_tray():
    image_path = os.path.join("images", "logo.png")
    image = Image.open(image_path)
    icon = pystray.Icon("GFG", image, "Simple Screen Center", menu=pystray.Menu(
    pystray.MenuItem("Documentation", lambda: webbrowser.open("https://github.com/AbianS/center-apps-windows")),
    pystray.MenuItem("Exit", lambda: icon.stop())))
    
    # Thread
    hilo = threading.Thread(target=listener_center_screen, daemon=True)
    hilo.start()

    icon.run()



if __name__ == "__main__":
    combination = {keyboard.Key.ctrl_l, keyboard.Key.alt_l}
    current = set()
    window_tray()

    
