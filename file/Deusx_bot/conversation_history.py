import os
import json

class ConversationHistory:
    def __init__(self, history_folder, history_file):
        self.history_folder = history_folder
        self.history_file = history_file

        # Create folder if it doesn't exist
        if not os.path.exists(self.history_folder):
            os.makedirs(self.history_folder)

    def load_history(self):
        try:
            file_path = os.path.join(self.history_folder, self.history_file)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error loading history: {e}")
        return {}

    def save_history(self, history):
        file_path = os.path.join(self.history_folder, self.history_file)
        with open(file_path, 'w') as file:
            json.dump(history, file, indent=4)

    def add_conversation(self, history, session_id, data):
        if session_id not in history:
            history[session_id] = []
        history[session_id].append(data)
