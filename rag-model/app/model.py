from .storage import store_prompt, retrieve_similar_prompts
from models.rag_model import generate_response_from_model

# Main function to process the user's query
def handle_user_query(user_prompt):
    # Step 1: Store the current prompt
    store_prompt(user_prompt)

    # Step 2: Retrieve similar prompts from storage
    similar_prompts = retrieve_similar_prompts(user_prompt)

    # Step 3: Generate a response using the current and previous prompts
    response = generate_response_from_model(user_prompt, similar_prompts)
    
    return response
