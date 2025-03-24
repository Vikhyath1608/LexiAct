import datetime
import time
import pygame # type: ignore
import re
import os
def alarm_time_set(input_string):
    """Extracts time from input string and converts it to 24-hour format."""
    match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm|a.m.|p.m.)?', input_string)
    if match:
        hours, minutes, period = match.groups()
        hours, minutes = int(hours), int(minutes)
        
        if period:
            period = period.upper()
            if period == "PM" and hours != 12:
                hours += 12
            elif period == "AM" and hours == 12:
                hours = 0
        
        return f"{hours:02}:{minutes:02}"
    return None

def set_alarm(user_input):
    alarm_time = alarm_time_set(user_input)
    """Sets an alarm for the given time in HH:MM format."""
    if not alarm_time:
        print("Invalid time format.")
        return

    print(f"Alarm set for {alarm_time}.")

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == alarm_time:
            print("⏰ Alarm ringing!")

            # Play an alarm sound
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(BASE_DIR, "alarm.mp3")) 
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)
            break
        time.sleep(10)  # Check every 10 seconds to avoid excessive CPU usage

# Example usage
#user_input = "Set an alarm for 7:30 PM"
#set_alarm(user_input)
