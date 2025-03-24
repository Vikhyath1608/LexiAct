from datetime import datetime

def announce_date_time(type):
    """Fetches and announces the current date and time."""
    now = datetime.now()
    date_str = now.strftime("%B %d, %Y, %A")  # Example: Monday, March 11, 2025
    time_str = now.strftime("%I:%M %p")  # Example: 02:30 PM
    if type=="date":
        message = f"Today's date is {date_str}"
    elif type=="time":
        message = f"current time is {time_str}."
   # print(message)  # Display in console
    return message

