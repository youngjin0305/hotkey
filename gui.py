import tkinter as tk
from tkinter import messagebox, Toplevel, ttk

class HotkeyGUI:
    def __init__(self, root, hotkey_manager, on_close_callback=None, test_action_callback=None):
        self.root = root
        self.hotkey_manager = hotkey_manager
        self.root.title("단축키 설정 프로그램")
        self.root.geometry("400x400")

        # 현재 등록된 핫키 목록 표시용
        self.label = tk.Label(root, text="현재 등록된 단축키 목록:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.hotkey_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.hotkey_listbox.pack(pady=10, fill='both', expand=True)
        self.refresh_hotkey_list()

        # 단축키 추가 버튼 (팝업창)
        self.start_record_button = tk.Button(root, text="단축키 지정 시작", command=self.open_hotkey_popup)
        self.start_record_button.pack(pady=10)

        # 선택한 핫키 삭제 버튼
        self.delete_button = tk.Button(root, text="선택한 핫키 삭제", command=self.delete_selected_hotkey)
        self.delete_button.pack(pady=10)

        # 종료 버튼
        if on_close_callback:
            self.exit_button = tk.Button(root, text="종료", command=on_close_callback)
            self.exit_button.pack(pady=10)

        # 창 닫기
        if on_close_callback:
            self.root.protocol("WM_DELETE_WINDOW", on_close_callback)

    def show_message(self, msg):
        messagebox.showinfo("알림", msg)

    def refresh_hotkey_list(self):
        self.hotkey_listbox.delete(0, tk.END)
        for key_combo, action_data in self.hotkey_manager.hotkeys.items():
            action = action_data.get("action")
            self.hotkey_listbox.insert(tk.END, f"{key_combo} -> {action}")

    def open_hotkey_popup(self):
        self.popup = Toplevel(self.root)
        self.popup.title("단축키 지정")
        self.popup.geometry("400x400")
        
        instruction_label = tk.Label(self.popup, text="원하는 단축키를 누르세요 (엔터로 확정)")
        instruction_label.pack(pady=5)
        
        self.recorded_keys_label = tk.Label(self.popup, text="현재 인식된 키: ")
        self.recorded_keys_label.pack(pady=5)

        # 액션 선택
        action_frame = tk.Frame(self.popup)
        action_frame.pack(pady=10, fill='x', padx=10)

        tk.Label(action_frame, text="액션 선택:").grid(row=0, column=0, sticky='w', pady=2)
        self.action_var = tk.StringVar()
        self.action_combobox = ttk.Combobox(action_frame, textvariable=self.action_var,
                                            values=["show_message", "run_program", "open_url"], state="readonly")
        self.action_combobox.grid(row=0, column=1, sticky='we', pady=2, padx=5)
        self.action_combobox.bind("<<ComboboxSelected>>", self.on_action_selected)

        # 파라미터 입력
        self.param_frame = tk.Frame(self.popup)
        self.param_frame.pack(pady=10, fill='x', padx=10)

        # 버튼
        btn_frame = tk.Frame(self.popup)
        btn_frame.pack(pady=10)

        self.confirm_button = tk.Button(btn_frame, text="확정", command=self.confirm_hotkey)
        self.confirm_button.grid(row=0, column=0, padx=5)

        self.retry_button = tk.Button(btn_frame, text="다시 시도(키입력)", command=self.retry_hotkey)
        self.retry_button.grid(row=0, column=1, padx=5)

        self.is_recording = True
        self.recorded_keys = []
        self.pressed_keys = set()

        self.param_entries = {}

        # 키 이벤트 바인딩
        self.popup.bind("<KeyPress>", self.on_key_press_popup)
        self.popup.bind("<KeyRelease>", self.on_key_release_popup)
        self.popup.focus_set()

    def on_key_press_popup(self, event):
        if event.keysym == 'Return':
            # 키입력 종료
            self.is_recording = False
            return

        keysym = event.keysym.lower()
        if self.is_recording and keysym not in self.pressed_keys:
            self.pressed_keys.add(keysym)
            self.recorded_keys.append(keysym)
            self.update_recorded_keys_label()

    def on_key_release_popup(self, event):
        keysym = event.keysym.lower()
        if keysym in self.pressed_keys:
            self.pressed_keys.remove(keysym)

    def update_recorded_keys_label(self):
        self.recorded_keys_label.config(text=f"현재 인식된 키: {' + '.join(self.recorded_keys)}")

    def retry_hotkey(self):
        self.recorded_keys = []
        self.pressed_keys = set()
        self.is_recording = True
        self.update_recorded_keys_label()

    def on_action_selected(self, event):
        self.update_param_fields()

    def update_param_fields(self):
        # 기존 파라미터 위젯 제거
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        selected_action = self.action_var.get()
        self.param_entries = {}

        # 액션별로 필요한 파라미터 필드 추가
        if selected_action == "show_message":
            tk.Label(self.param_frame, text="메세지:").grid(row=0, column=0, sticky='w')
            msg_entry = tk.Entry(self.param_frame)
            msg_entry.grid(row=0, column=1, sticky='we', padx=5)
            self.param_entries["message"] = msg_entry

        elif selected_action == "run_program":
            tk.Label(self.param_frame, text="명령어(프로그램):").grid(row=0, column=0, sticky='w')
            cmd_entry = tk.Entry(self.param_frame)
            cmd_entry.grid(row=0, column=1, sticky='we', padx=5)
            self.param_entries["command"] = cmd_entry

        elif selected_action == "open_url":
            tk.Label(self.param_frame, text="URL:").grid(row=0, column=0, sticky='w')
            url_entry = tk.Entry(self.param_frame)
            url_entry.grid(row=0, column=1, sticky='we', padx=5)
            self.param_entries["url"] = url_entry

        self.param_frame.columnconfigure(1, weight=1)

    def confirm_hotkey(self):
        # recorded_keys를 <ctrl>+<shift>+x 형태로 변환
        mapping = {
            'control_l': '<ctrl>',
            'control_r': '<ctrl>',
            'shift_l': '<shift>',
            'shift_r': '<shift>',
            'alt_l': '<alt>',
            'alt_r': '<alt>'
        }

        converted_keys = []
        for k in self.recorded_keys:
            if k in mapping:
                converted_keys.append(mapping[k])
            else:
                converted_keys.append(k)

        if not converted_keys:
            self.show_message("인식된 키가 없습니다. 다시 시도하세요.")
            return

        hotkey_combo = '+'.join(converted_keys)

        # 액션 및 파라미터 가져오기
        action = self.action_var.get()
        if not action:
            self.show_message("액션을 선택해주세요.")
            return

        params = {}
        for key, entry in self.param_entries.items():
            params[key] = entry.get().strip()

        # 필수 파라미터 체크
        if action == "show_message" and not params.get("message"):
            self.show_message("메세지를 입력해주세요.")
            return
        if action == "run_program" and not params.get("command"):
            self.show_message("명령어를 입력해주세요.")
            return
        if action == "open_url" and not params.get("url"):
            self.show_message("URL을 입력해주세요.")
            return

        # 액션과 파라미터를 함께 저장
        action_data = {"action": action, "params": params}
        self.hotkey_manager.add_hotkey(hotkey_combo, action_data)
        self.show_message(f"'{hotkey_combo}' 단축키가 '{action}'로 추가되었습니다.")
        self.refresh_hotkey_list()

        self.popup.destroy()

    def delete_selected_hotkey(self):
        selection = self.hotkey_listbox.curselection()
        if selection:
            item = self.hotkey_listbox.get(selection[0])
            # item 형식: "<ctrl>+<shift>+c -> run_program"
            # ' -> '로 split하여 첫번째 부분은 key_combo
            key_combo = item.split(' -> ')[0]
            if key_combo in self.hotkey_manager.hotkeys:
                self.hotkey_manager.delete_hotkey(key_combo)
                self.show_message(f"'{key_combo}' 단축키가 삭제되었습니다.")
                self.refresh_hotkey_list()
            else:
                self.show_message("선택한 핫키가 존재하지 않습니다.")
        else:
            self.show_message("삭제할 핫키를 목록에서 선택해주세요.")
