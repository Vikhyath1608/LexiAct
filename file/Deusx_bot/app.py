import os
import json
from flask import Flask, render_template, request, jsonify
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from conversation_history import ConversationHistory
from meta_ai_api import MetaAI
import datetime
import uuid

app = Flask(__name__)

# Initialize the AI model and conversation history
ai = MetaAI()
history_folder = "conversation_history"
current_date = datetime.date.today().strftime("%Y-%m-%d")
history_file = f"{current_date}.json"
conversation_history = ConversationHistory(history_folder, history_file)

# Function to generate session ID
def generate_session_id():
    return str(uuid.uuid4())

# Route for the chat UI
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling user chat prompts
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('message')
    session_id = data.get('session_id', generate_session_id())  # Generate session ID if not provided

    # Get AI response
    response = ai.prompt(message=prompt)
    ai_response = response.get('message', '')

    # Tokenize prompt and response for saving relevant conversation
    prompt_tokens = extract_relevant_tokens(prompt)
    response_tokens = extract_relevant_tokens(ai_response)
    relevant_data = {
        "prompt": prompt_tokens,
        "response": response_tokens
    }

    # Save the conversation history
    history = conversation_history.load_history()
    conversation_history.add_conversation(history, session_id, relevant_data)
    conversation_history.save_history(history)

    return jsonify({"response": ai_response, "session_id": session_id})

# Extract relevant tokens from the prompt and response
def extract_relevant_tokens(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    relevant_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and len(token) > 3 and token not in stop_words]
    return relevant_tokens

if __name__ == '__main__':
    app.run(debug=True)
