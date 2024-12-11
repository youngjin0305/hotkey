import tkinter as tk
from gui import HotkeyGUI
from hotkey_manager import HotkeyManager

def main():
    root = tk.Tk()

    hotkey_manager = HotkeyManager('config.json')

    gui = HotkeyGUI(
        root,
        hotkey_manager,
        on_close_callback=lambda: on_close(hotkey_manager, root)
    )

    hotkey_manager.start(gui)

    root.mainloop()

def on_close(hotkey_manager, root):
    hotkey_manager.stop()
    root.destroy()

if __name__ == "__main__":
    main()
