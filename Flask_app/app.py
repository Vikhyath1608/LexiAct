from flask import Flask, request, jsonify, render_template
import json
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from meta_ai_api import MetaAI

app = Flask(__name__)

class ConversationHistory:
    def __init__(self, history_file):
        """
        Initialize conversation history.
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


# Initialize conversation history
conversation_history = ConversationHistory("conversation_history.json")
ai = MetaAI()


def extract_keywords(prompt):
    """Extract keywords from the prompt."""
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(prompt.lower())
    keywords = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return keywords


@app.route('/')
def index():
    return render_template('bot.html')

@app.route('/get_session_ids', methods=['GET'])
def get_session_ids():
    """Fetch session IDs from the conversation history."""
    history = conversation_history.load_history()
    session_ids = list(history.keys())  # Get all session IDs
    return jsonify({'session_ids': session_ids})


@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data.get('prompt')
    session_id = data.get('session_id')

    # Load conversation history
    history = conversation_history.load_history()

    # Extract keywords from the user's prompt
    keywords = extract_keywords(prompt)

    # Pass prompt to AI and get response
    response = ai.prompt(message=prompt)

    # Store conversation in history
    conversation_history.add_conversation(history, session_id, prompt, response['message'])
    conversation_history.save_history(history)

    return jsonify({
        'response': response['message'],
        'session_id': session_id  # Include session_id in response
    })


if __name__ == "__main__":
    app.run(debug=True)
