import os
import json

class HotkeyManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.hotkeys = self.load_hotkeys()

    def load_hotkeys(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}

    def save_hotkeys(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.hotkeys, f, ensure_ascii=False, indent=2)

    def add_hotkey(self, key_combo, action):
        # key_combo 예: '<ctrl>+<shift>+x'
        # action 예: 'show_message' 같은 키로 특정함수나 실행동작 매핑
        self.hotkeys[key_combo] = action
        self.save_hotkeys()

    def delete_hotkey(self, key_combo):
        if key_combo in self.hotkeys:
            del self.hotkeys[key_combo]
            self.save_hotkeys()