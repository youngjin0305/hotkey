import tkinter as tk
from tkinter import messagebox

class HotkeyGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("단축키 설정 프로그램")
        
        self.hotkey_list = tk.Listbox(self.root, width=30, height=10)
        self.hotkey_list.pack(pady=10)

        tk.Button(self.root, text="단축키 추가", command=self.add_hotkey).pack(pady=5)
        tk.Button(self.root, text="단축키 삭제", command=self.delete_hotkey).pack(pady=5)

        self.load_hotkeys()

    def load_hotkeys(self):
        self.hotkey_list.delete(0, tk.END)
        for key_combo, action in self.manager.hotkeys.items():
            self.hotkey_list.insert(tk.END, f"{key_combo}: {action}")

    def add_hotkey(self):
        key_combo = tk.simpledialog.askstring("단축키 추가", "원하는 키를 입력:")
        action = tk.simpledialog.askstring("단축키 삭제", "임시 삭제:")
        if key_combo and action:
            if self.manager.add_hotkey(key_combo, action):
                self.load_hotkeys()
            else:
                messagebox.showerror("Error", "중복된 키입니다")

    def delete_hotkey(self):
        selected = self.hotkey_list.curselection()
        if selected:
            key_combo = self.hotkey_list.get(selected[0]).split(":")[0].strip()
            self.manager.delete_hotkey(key_combo)
            self.load_hotkeys()
        else:
            messagebox.showwarning("Warning", "임시")

    def run(self):
        self.root.mainloop()

