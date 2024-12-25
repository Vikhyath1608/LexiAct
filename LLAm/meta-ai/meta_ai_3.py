import json
import os
from meta_ai_api import MetaAI
import datetime
import uuid


class ConversationHistory:
    def __init__(self, history_file):
        self.history_file = history_file

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as file:
                return json.load(file)
        else:
            return {}

    def save_history(self, history):
        with open(self.history_file, 'w') as file:
            json.dump(history, file, indent=4)

    def add_conversation(self, history, session_id, prompt, response):
        if session_id not in history:
            history[session_id] = []
        history[session_id].append({"prompt": prompt, "response": response})

    def get_conversation(self, history, session_id):
        return history.get(session_id)


def get_user_input():
    """Get user input"""
    return input("Enter prompt: ")


def get_ai_response(ai, prompt):
    """Get AI response"""
    response = ai.prompt(message=prompt)
    return response['message']


def prompt_chaining(ai, conversation_history, session_id):
    """Main function for prompt chaining"""
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

        # Store conversation
        conversation_history.add_conversation(history, session_id, prompt, response)
        conversation_history.save_history(history)

        # Check if AI responded with a question or needs more information
        if response.endswith("?") or response.lower().startswith("please"):
            # Continue prompt chaining
            while True:
                # Get follow-up user prompt
                follow_up_prompt = get_user_input()
                if follow_up_prompt.lower() == "exit":
                    break

                # Get AI response
                follow_up_response = get_ai_response(ai, follow_up_prompt)
                print("AI:", follow_up_response)

                # Store follow-up conversation
                conversation_history.add_conversation(history, session_id, follow_up_prompt, follow_up_response)
                conversation_history.save_history(history)

                # Check if conversation can be terminated
                if not follow_up_response.endswith("?") and not follow_up_response.lower().startswith("please"):
                    break


def main():
    ai = MetaAI()
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    history_file = f"conversation_history_{current_date}.json"
    conversation_history = ConversationHistory(history_file)

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