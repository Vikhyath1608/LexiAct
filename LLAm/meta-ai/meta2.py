from meta_ai_api import MetaAI

def get_user_input():
    """Get user input"""
    return input("Enter prompt: ")

def get_ai_response(ai, prompt):
    """Get AI response"""
    response = ai.prompt(message=prompt)
    return response['message']

def prompt_chaining(ai):
    """Main function for prompt chaining"""
    while True:
        # Get initial user prompt
        prompt = get_user_input()

        # Get AI response
        response = get_ai_response(ai, prompt)
        print("AI:", response)

        # Check if AI responded with a question or needs more information
        if response.endswith("?") or response.lower().startswith("please"):
            # Continue prompt chaining
            while True:
                # Get follow-up user prompt
                follow_up_prompt = get_user_input()
                # Get AI response
                follow_up_response = get_ai_response(ai, follow_up_prompt)
                print("AI:", follow_up_response)
                
                # Check if conversation can be terminated
                if not follow_up_response.endswith("?") and not follow_up_response.lower().startswith("please"):
                    break
        else:
            # Ask user if they want to continue
            cont = input("Do you want to continue? (y/n): ")
            if cont.lower() != "y":
                break

if __name__ == "__main__":
    ai = MetaAI()
    prompt_chaining(ai)