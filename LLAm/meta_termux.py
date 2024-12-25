import json
import os
import subprocess
from meta_ai_api import MetaAI
import uuid
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Check if nltk data is downloaded, download if not
subprocess.run(["python", "-m", "nltk", "download", "punkt"])
subprocess.run(["python", "-m", "nltk", "download", "wordnet"])
subprocess.run(["python", "-m", "nltk", "download", "stopwords"])


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


def get_user_input():
    """Get user input."""
    while True:
        user_input = input("Enter prompt: ")
        if user_input.strip():
            return user_input
        print("Please enter a non-empty prompt.")


def get_ai_response(ai, prompt):
    """Get AI response."""
    try:
        response = ai.prompt(message=prompt)
        return response['message']
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return ""


def extract_keywords(prompt):
    """Extract keywords from prompt."""
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(prompt.lower())
    keywords = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return keywords


def prompt_chaining(ai, conversation_history, session_id):
    """Main function for prompt chaining."""
    history = conversation_history.load_history()

    print(f"Session ID: {session_id}")
    print("Conversation started. Type 'exit' to quit.\n")

    previous_keywords = []

    while True:
        # Get initial user prompt
        prompt = get_user_input()

        if prompt.lower() == "exit":
            break

        # Extract keywords from current prompt
        current_keywords = extract_keywords(prompt)

        # Combine previous and current keywords
        context_keywords = previous_keywords + current_keywords

        # Inform AI about context keywords
        context = "Context: " + ", ".join(context_keywords)
        prompt = f"{context}\n{prompt}"

        # Get AI response
        response = get_ai_response(ai, prompt)
        print("AI:", response)

        # Store conversation
        conversation_history.add_conversation(history, session_id, prompt, response)
        conversation_history.save_history(history)

        # Update previous keywords
        previous_keywords = context_keywords


def main():
    history_file = "conversation_history.json"
    conversation_history = ConversationHistory(history_file)
    ai = MetaAI()

    session_id_option = input("Do you want to (1) generate a new session ID or (2) enter a custom session ID? ")
    
    if session_id_option == "1":
        session_id = str(uuid.uuid4())
    elif session_id_option == "2":
        session_id = input("Enter custom session ID: ")
    else:
        print("Invalid option. Generating a new session ID.")
        session_id = str(uuid.uuid4())

    prompt_chaining(ai, conversation_history, session_id)


if __name__ == "__main__":
    main()