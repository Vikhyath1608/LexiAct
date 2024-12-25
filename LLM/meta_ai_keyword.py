
import json
import os
import uuid
import spacy
from transformers import pipeline
from meta_ai_api import MetaAI

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class ConversationHistory:
    def __init__(self, history_file):
        """Initialize conversation history."""
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

    def add_conversation(self, history, session_id, prompt, response, key_points):
        """Add conversation with key points to history."""
        if session_id not in history:
            history[session_id] = {
                "conversation": [],
                "context_summary": {}
            }

        # Store prompt and key points in conversation history
        history[session_id]["conversation"].append({
            "prompt": prompt,
            "key_points": key_points
        })

        # Update context summary with new key points
        for category, items in key_points.items():
            if category not in history[session_id]["context_summary"]:
                history[session_id]["context_summary"][category] = []
            history[session_id]["context_summary"][category].extend(items)

    def get_conversation(self, history, session_id):
        """Retrieve conversation by session ID."""
        return history.get(session_id, {}).get("conversation", [])

    def get_context_summary(self, history, session_id):
        """Retrieve the context summary for a session."""
        return history.get(session_id, {}).get("context_summary", {})


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


def dynamic_extract_key_points(text):
    """Extract dynamic key points from text using NER and summarization."""
    doc = nlp(text)

    # Categorize entities based on NER results
    key_points = {
        "locations": [],
        "dates": [],
        "organizations": [],
        "people": [],
        "activities": [],
    }

    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            key_points["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            key_points["dates"].append(ent.text)
        elif ent.label_ == "ORG":
            key_points["organizations"].append(ent.text)
        elif ent.label_ == "PERSON":
            key_points["people"].append(ent.text)

    # Use summarization to capture the most important information
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    summary_text = summary[0]['summary_text']
    key_points["summary"] = [summary_text]

    return key_points


def prompt_chaining(ai, conversation_history, session_id):
    """Main function for prompt chaining."""
    history = conversation_history.load_history()

    print(f"Session ID: {session_id}")
    print("Conversation started. Type 'exit' to quit.\n")

    while True:
        # Get initial user prompt
        prompt = get_user_input()

        if prompt.lower() == "exit":
            break

        # Get AI response
        response = get_ai_response(ai, prompt)
        print("AI:", response)

        # Dynamically extract and categorize key points from AI response
        key_points = dynamic_extract_key_points(response)

        # Store conversation with categorized key points
        conversation_history.add_conversation(history, session_id, prompt, response, key_points)
        conversation_history.save_history(history)

        # Display context summary dynamically
        context_summary = conversation_history.get_context_summary(history, session_id)
        print("\nContext Summary:")
        for category, items in context_summary.items():
            print(f"{category.capitalize()}: {', '.join(items)}")
        print("\n")


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