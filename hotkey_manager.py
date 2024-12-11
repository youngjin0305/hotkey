class HotkeyManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.hotkeys = self.load_hotkeys()

    def load_hotkeys(self):
        pass

    def save_hotkeys(self):
        pass

    def add_hotkey(self, key_combo, action):
        pass

    def delete_hotkey(self, key_combo):
        pass