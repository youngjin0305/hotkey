import subprocess
import webbrowser

def show_message_action(gui, params):
    message = params.get("message", "단축키가 눌렸습니다!")
    gui.show_message(message)

def run_program_action(gui, params):
    command = params.get("command")
    if command:
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            gui.show_message(f"명령어 실행 실패: {e}")
    else:
        gui.show_message("실행할 명령어가 지정되지 않았습니다.")

def open_url_action(gui, params):
    url = params.get("url")
    if url:
        try:
            webbrowser.open(url)
            gui.show_message(f"URL '{url}'을 열었습니다.")
        except Exception as e:
            gui.show_message(f"URL 열기 실패: {e}")


ACTION_HANDLERS = {
    "show_message": show_message_action,
    "run_program": run_program_action,
    "open_url": open_url_action,
}
