import json
import os
import uuid
import subprocess
import speech_recognition as sr
from meta_ai_api import MetaAI

class ConversationHistory:
    def __init__(self, history_file):
        """
        Initialize conversation history.

        Args:
        history_file (str): File path for storing conversation history.
        """
        self.history_file = history_file

    def load_history(self):
        """Load conversation history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except json.JSONDecodeError:
            print("Error loading conversation history.")
            return {}

    def save_history(self, history):
        """Save conversation history to file."""
        try:
            with open(self.history_file, 'w') as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"Error saving conversation history: {e}")

    def add_conversation(self, history, session_id, prompt, response):
        """Add conversation to history."""
        if session_id not in history:
            history[session_id] = []
        history[session_id].append({"prompt": prompt, "response": response})

    def get_conversation(self, history, session_id):
        """Retrieve conversation by session ID."""
        return history.get(session_id)

def recognize_voice():
    """Convert voice input to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a voice command...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
    return ""

def get_ai_response(ai, task_description):
    """Use MetaAI to generate the task description."""
    try:
        response = ai.prompt(message=task_description)
        return response['message']
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return ""

def save_to_robot_file(session_id, task):
    """Save task to a .robot file."""
    robot_file = f"{session_id}.robot"
    try:
        with open(robot_file, 'w') as file:
            file.write("*** Settings ***\nLibrary  BuiltIn\n\n")
            file.write("*** Test Cases ***\n")
            test_case_name = task[:30].replace(" ", "_").replace("\n", "_")
            file.write(f"{test_case_name}\n")
            file.write(f"    [Documentation]  {task}\n")
            file.write(f"    Log  Generated Robot Script for: {task}\n\n")

        print(f"Task saved to {robot_file}")
        return robot_file
    except Exception as e:
        print(f"Error saving to .robot file: {e}")
        return None

def execute_robot_script(robot_file):
    """Run the generated .robot script."""
    try:
        subprocess.run(["robot", robot_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the Robot Framework script: {e}")

def main():
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")

    # Step 1: Voice input
    task_description = recognize_voice()
    if not task_description:
        print("No valid voice command received. Exiting.")
        return

    # Step 2: MetaAI interaction
    ai = MetaAI()
    ai_response = get_ai_response(ai, task_description)
    if not ai_response:
        print("AI failed to generate a task description. Exiting.")
        return

    # Step 3: Save to .robot file
    robot_file = save_to_robot_file(session_id, ai_response)
    if not robot_file:
        return

    # Step 4: Execute .robot script
    execute_robot_script(robot_file)

if __name__ == "__main__":
    main()
