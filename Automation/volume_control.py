import sys
import re
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return interface.QueryInterface(IAudioEndpointVolume)

def change_volume(increase=True):
    volume = get_volume_interface()
    current_volume = volume.GetMasterVolumeLevelScalar()
    step = 0.05  # Adjust step size for volume change

    if increase:
        new_volume = min(current_volume + step, 1.0)
    else:
        new_volume = max(current_volume - step, 0.0)

    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume set to: {new_volume * 100:.0f}%")

def set_volume(level):
    volume = get_volume_interface()

    if 0 <= level <= 100:
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        print(f"Volume set to: {level}%")
    else:
        print("Please enter a value between 0 and 100.")

while True:
    user_input = input("Enter command (volume up/down or set volume to X percent): ").strip().lower()

    if user_input == "exit":
        print("Exiting program.")
        sys.exit()
    
    if user_input == "volume up":
        change_volume(True)
    elif user_input == "volume down":
        change_volume(False)
    else:
        match = re.match(r"set volume to (\d+)\s*percent", user_input)
        if match:
            set_volume(int(match.group(1)))
        else:
            print("Invalid command! Use 'volume up', 'volume down', or 'set volume to X percent'.")
