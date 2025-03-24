import time
import pygame # type: ignore
import os
import re

def parse_time_input(user_input):
    """Parses user input like '50 seconds', '1 minute', or '1 hour' and converts it into seconds."""
    user_input = user_input.lower().strip()
    match = re.search(r"(\d+)\s*(second|minute|hour)s?", user_input)
    print(match)

    if match:
        value = int(match.group(1))
        unit = match.group(2)

        if unit == "second":
            return value
        elif unit == "minute":
            return value * 60
        elif unit == "hour":
            return value * 3600
    return None  # Invalid input

def set_timer(user_input):
    """Sets a countdown timer based on the parsed input."""
    print(user_input)
    seconds = parse_time_input(user_input)
    
    if seconds is None:
        print("Invalid input. Please enter time in format like '50 seconds', '1 minute', or '1 hour'.")
        return
    
    print(f"Timer set for {user_input}.")

    for remaining in range(seconds, 0, -1):
        print(f"Time left: {remaining} sec", end="\r")
        time.sleep(1)

    print("\n⏰ Time's up!")

    # Initialize pygame mixer
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Check if the alarm file exists
    if os.path.exists(os.path.join(BASE_DIR, "alarm.mp3")):
        pygame.mixer.music.load(os.path.join(BASE_DIR, "alarm.mp3"))
        pygame.mixer.music.play()

        # Wait until the alarm sound finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        print("Error: alarm.mp3 not found.")
    message=f"⏲️ Timer set for {seconds} seconds."
    return message

# Example Usage:
#user_input = input("Set a timer for: ")  # e.g., "1 minute", "50 seconds", "1 hour"
#set_timer(user_input)
