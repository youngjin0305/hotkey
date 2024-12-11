from gui import HotkeyGUI
from hotkey_manager import HotkeyManager

if __name__ == "__main__":
    manager = HotkeyManager()
    app = HotkeyGUI(manager)
    app.run()