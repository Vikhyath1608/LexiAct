import os
import subprocess

# Get the user's home directory dynamically
user_home = os.getenv("USERPROFILE")

# Dictionary to map commands to application paths or direct executable names
app_commands = {
    # System Apps (Use subprocess for built-in Windows tools)
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
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "opera": os.path.join(user_home, "AppData", "Local", "Programs", "Opera", "launcher.exe"),

    # Microsoft Office Apps
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
    "onenote": r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",

    # Communication Apps
    "whatsapp": os.path.join(user_home, "AppData", "Local", "Microsoft", "WindowsApps", "WhatsApp.exe"),
    "telegram": os.path.join(user_home, "AppData", "Roaming", "Telegram Desktop", "Telegram.exe"),
    "zoom": os.path.join(user_home, "AppData", "Roaming", "Zoom", "bin", "Zoom.exe"),
    "discord": os.path.join(user_home, "AppData", "Local", "Discord", "Update.exe"),

    # Media Players
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "windows media player": "wmplayer.exe",

    # Development Tools
    "vs code": os.path.join(user_home, "AppData", "Local", "Programs", "Microsoft VS Code", "Code.exe"),
    "pycharm": r"C:\Program Files\JetBrains\PyCharm Community Edition 2023.3\bin\pycharm64.exe",
    "android studio": r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
    "eclipse": os.path.join(user_home, "eclipse", "java-2023-03", "eclipse", "eclipse.exe"),

    # Others
    "spotify": os.path.join(user_home, "AppData", "Roaming", "Spotify", "Spotify.exe"),
    "steam": r"C:\Program Files (x86)\Steam\steam.exe",
    "epic games": r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
}

def open_application(command):
    command = command.lower().strip()  # Normalize input
    app_path = app_commands.get(command)

    if app_path:
        if app_path.endswith(".exe") or app_path.startswith("ms-settings"):  # Use os.startfile for .exe and Windows settings
            if os.path.exists(app_path) or app_path.startswith("ms-settings"):
                try:
                    os.startfile(app_path)  # Open the application
                    print(f"Opening {command}...")
                except Exception as e:
                    print(f"Error opening {command}: {e}")
            else:
                print(f"Application '{command}' not found at expected location: {app_path}")
        else:  # Use subprocess for system utilities
            try:
                subprocess.Popen(app_path, shell=True)
                print(f"Opening {command}...")
            except Exception as e:
                print(f"Error opening {command}: {e}")
    elif os.path.isfile(command):  # If user provides a valid file path
        try:
            os.startfile(command)
            print(f"Opening file: {command}")
        except Exception as e:
            print(f"Error opening file: {e}")
    else:
        print(f"Command '{command}' not recognized or application not found. Available commands: {list(app_commands.keys())}")

# Example: Take user input and open the corresponding app
user_command = input("Enter application name or file path: ").strip()
open_application(user_command)
