import os
import json
import shutil
import subprocess
import re
from dotenv import load_dotenv
load_dotenv()
APP_PATHS_FILE = os.getenv("APP_PATHS_FILE")
print(APP_PATHS_FILE)
user_home = os.getenv("USERPROFILE")

apps_to_find = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "device manager": "devmgmt.msc",
    "registry editor": "regedit.exe",
    "paint": "mspaint.exe",
    "wordpad": "write.exe",
    "file explorer": "explorer.exe",
    "settings": "ms-settings:",

    # Browsers
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    "edge": "msedge.exe",
    "opera": "opera.exe",

    # Office
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "outlook": "outlook.exe",
    "onenote": "onenote.exe",

    # Communication
    "whatsapp": "whatsapp.exe",
    "telegram": "telegram.exe",
    "zoom": "zoom.exe",
    "discord": "discord.exe",

    # Media
    "vlc": "vlc.exe",
    "windows media player": "wmplayer.exe",

    # Development
    "vs code": "code.exe",
    "vscode": "code.exe",
    "pycharm": "pycharm64.exe",
    "android studio": "studio64.exe",
    "eclipse": "eclipse.exe",

    # Others
    "spotify": "spotify.exe",
    "steam": "steam.exe",
    "epic games": "epicgameslauncher.exe"
}


def find_executable(name, search_paths):
    for base_dir in search_paths:
        for root, dirs, files in os.walk(base_dir):
            if name.lower() in (file.lower() for file in files):
                return os.path.join(root, name)
    return None


def build_app_paths():
    search_paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        os.path.join(user_home, "AppData", "Local"),
        os.path.join(user_home, "AppData", "Roaming"),
    ]

    paths = {}
    for key, exe in apps_to_find.items():
        if exe.startswith("ms-settings"):
            paths[key] = exe
        else:
            path = shutil.which(exe) or find_executable(exe, search_paths)
            if path:
                paths[key] = path

    with open(APP_PATHS_FILE, "w") as f:
        json.dump(paths, f, indent=4)
    return paths


def load_app_paths():
    if os.path.exists(APP_PATHS_FILE):
        print("found.....")
        with open(APP_PATHS_FILE, "r") as f:
            return json.load(f)
    else:
        print("not found.....")
        return build_app_paths()


def parse_command(user_input):
    user_input = user_input.lower().strip()
    match = re.search(r"(open|start|launch)\s+([\w\s]+?)(?:\s+app)?$", user_input)
    if match:
        return match.group(2).strip()
    return user_input


def open_application(command, app_paths):
    command = parse_command(command)
    app_path = app_paths.get(command)

    if app_path:
        try:
            if app_path.startswith("ms-settings"):
                os.startfile(app_path)
            elif os.path.exists(app_path):
                os.startfile(app_path)
            else:
                subprocess.Popen(app_path, shell=True)
            return f"Opening {command}..."
        except Exception as e:
            return f"Error opening {command}: {e}"
    elif os.path.isfile(command):
        try:
            os.startfile(command)
            return f"Opening file: {command}"
        except Exception as e:
            return f"Error opening file: {e}"
    else:
        return f"Unknown application: '{command}'. Available: {', '.join(app_paths.keys())}"


# For external use
def run_open_app(user_command):
    print(user_command)
    app_paths = load_app_paths()
    return open_application(user_command, app_paths)


# If run directly
if __name__ == "__main__":
    user_command = input("Enter command: ").strip()
    result = run_open_app(user_command)
    print(result)
