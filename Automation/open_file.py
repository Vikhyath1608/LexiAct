import os
import re
import pyttsx3
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Get system username dynamically for user folders
USERNAME = os.getenv("USERNAME") or os.getlogin()
print(USERNAME)
def extract_file_details(command):
    # Define common locations
    common_locations = {
    "desktop": os.getenv("DESKTOP").replace("%USERNAME%", USERNAME),
    "downloads": os.getenv("DOWNLOADS").replace("%USERNAME%", USERNAME),
    "documents": os.getenv("DOCUMENTS").replace("%USERNAME%", USERNAME),
    "videos": os.getenv("VIDEOS").replace("%USERNAME%", USERNAME),
    "music": os.getenv("MUSIC").replace("%USERNAME%", USERNAME),
    "audio": os.getenv("AUDIO").replace("%USERNAME%", USERNAME),
    "pictures": os.getenv("PICTURES").replace("%USERNAME%", USERNAME),
    "d drive": os.getenv("D_DRIVE"),
    "c drive": os.getenv("C_DRIVE"),
    }

    # Extract file name using regex
    match = re.search(r'open the (.+) in the (.+)', command.lower())
    print(match)
    if match:
        file_name = match.group(1).strip()  # Extract file name
        location = match.group(2).strip()  # Extract location
        print(file_name,location)
        # Convert location to actual path
        file_path = common_locations.get(location, location)

        return file_name, file_path
    return None, None

def open_file(command):
    file_name, folder_path = extract_file_details(command)

    if file_name and folder_path:
        # Search for the file in the given directory
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file_name.lower() in file.lower():  # Case-insensitive match
                    file_path = os.path.join(root, file)
                    os.startfile(file_path)  # Open the file
                    speak_text(f"Opening {file_name}")
                    return
        speak_text("File not found!")
    else:
        speak_text("Invalid command format!")

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage
#command = input("Enter your command: ")  # Example: "open the demo video in the d drive"
#open_file(command)
