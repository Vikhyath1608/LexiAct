import json
import os
from meta_ai_api import MetaAI
import datetime
import uuid
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


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


class ConversationApp:
    def __init__(self, ai, history_folder, history_file):
        self.ai = ai
        self.conversation_history = ConversationHistory(history_folder, history_file)

    def get_user_input(self):
        return input("Enter prompt: ")

    def get_ai_response(self, prompt):
        try:
            response = self.ai.prompt(message=prompt)
            return response['message']
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return ""

    def extract_relevant_tokens(self, text):
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        relevant_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and len(token) > 3 and token not in stop_words]
        return relevant_tokens

    def prompt_chaining(self, session_id):
        history = self.conversation_history.load_history()

        print(f"Session ID: {session_id}")
        print("Conversation started. Type 'exit' to quit.\n")

        while True:
            prompt = self.get_user_input()

            if prompt.lower() == "exit":
                break

            response = self.get_ai_response(prompt)
            print("AI:", response)

            prompt_tokens = self.extract_relevant_tokens(prompt)
            response_tokens = self.extract_relevant_tokens(response)
            relevant_data = {
                "prompt": prompt_tokens,
                "response": response_tokens
            }
            self.conversation_history.add_conversation(history, session_id, relevant_data)
            self.conversation_history.save_history(history)


def generate_session_id():
    return str(uuid.uuid4())


def main():
    ai = MetaAI()
    history_folder = "conversation_history"
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    history_file = f"{current_date}.json"
    app = ConversationApp(ai, history_folder, history_file)

    session_id_option = input("Do you want to (1) generate a new session ID or (2) enter a custom session ID? ")
    
    if session_id_option == "1":
        session_id = generate_session_id()
    elif session_id_option == "2":
        session_id = input("Enter custom session ID: ")
    else:
        print("Invalid option. Generating a new session ID.")
        session_id = generate_session_id()

    app.prompt_chaining(session_id)


if __name__ == "__main__":
    main()