from pynput import keyboard
import json
import os
from actions import ACTION_HANDLERS

class HotkeyManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.hotkeys = self.load_hotkeys()
        self.listener = None
        self.gui = None

    def load_hotkeys(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                hotkeys = json.load(f)
                return hotkeys
        else:
            return {}

    def save_hotkeys(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.hotkeys, f, ensure_ascii=False, indent=2)

    def add_hotkey(self, key_combo, action_data):
        """핫키 추가: key_combo은 '<ctrl>+<shift>+x' 형식, action_data는 {'action': ..., 'params': ...} 딕셔너리"""
        self.hotkeys[key_combo] = action_data
        self.save_hotkeys()
        self.restart_listener()

    def delete_hotkey(self, key_combo):
        if key_combo in self.hotkeys:
            del self.hotkeys[key_combo]
            self.save_hotkeys()
            self.restart_listener()

    def start(self, gui):
        self.gui = gui
        self.listener = keyboard.GlobalHotKeys(self._create_hotkey_mapping())
        self.listener.start()

    def stop(self):
        if self.listener is not None:
            self.listener.stop()

    def restart_listener(self):
        self.stop()
        self.start(self.gui)

    def _create_hotkey_mapping(self):
        hotkey_mapping = {}
        for key_combo, action_data in self.hotkeys.items():
            hotkey_mapping[key_combo] = lambda a=action_data: self.on_hotkey_action(a)
        return hotkey_mapping

    def on_hotkey_action(self, action_data):
        action = action_data.get("action")
        params = action_data.get("params", {})
        handler = ACTION_HANDLERS.get(action)
        if handler:
            handler(self.gui, params)
        else:
            self.gui.show_message(f"알 수 없는 액션: {action}")
