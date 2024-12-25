import logging
import os
import json
import uuid
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from meta_ai_api import MetaAI

class ConversationHistory:
    def __init__(self, history_file):
        self.history_file = history_file
        self.logger = logging.getLogger(__name__)

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except json.JSONDecodeError:
            self.logger.error("Error loading conversation history.")
            return {}

    def save_history(self, history):
        try:
            with open(self.history_file, 'w') as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            self.logger.error(f"Error saving conversation history: {e}")

    def add_conversation(self, history, session_id, prompt, response):
        if session_id not in history:
            history[session_id] = []
        history[session_id].append({"prompt": prompt, "response": response})
        self.logger.info(f"Conversation added for session ID: {session_id}")

    def get_conversation(self, history, session_id):
        conversation = history.get(session_id)
        self.logger.info(f"Conversation retrieved for session ID: {session_id}")
        return conversation


def get_user_input():
    while True:
        user_input = input("Enter prompt: ")
        if user_input.strip():
            return user_input
        print("Please enter a non-empty prompt.")
        logging.getLogger(__name__).warning("Empty prompt entered.")


def get_ai_response(ai, prompt):
    try:
        response = ai.prompt(message=prompt)
        return response['message']
    except Exception as e:
        logging.getLogger(__name__).error(f"Error getting AI response: {e}")
        return ""


def extract_keywords(prompt):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(prompt.lower())
    keywords = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    logging.getLogger(__name__).debug(f"Keywords extracted: {keywords}")
    return keywords


def prompt_chaining(ai, conversation_history, session_id):
    history = conversation_history.load_history()
    logging.getLogger(__name__).info(f"Session ID: {session_id}")
    logging.getLogger(__name__).info("Conversation started.")

    previous_keywords = []

    while True:
        prompt = get_user_input()

        if prompt.lower() == "exit":
            break

        current_keywords = extract_keywords(prompt)

        context_keywords = previous_keywords + current_keywords

        context = "Context: " + ", ".join(context_keywords)
        prompt = f"{context}\n{prompt}"

        response = get_ai_response(ai, prompt)
        logging.getLogger(__name__).info(f"AI response: {response}")
        print("AI:", response)

        conversation_history.add_conversation(history, session_id, prompt, response)
        conversation_history.save_history(history)

        previous_keywords = context_keywords


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    history_file = "conversation_history.json"
    conversation_history = ConversationHistory(history_file)
    
    try:
        from meta_ai import MetaAI  # Assume MetaAI is a custom AI class
        ai = MetaAI()
    except ImportError as e:
        logging.getLogger(__name__).error("MetaAI module not found.")
        return

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
