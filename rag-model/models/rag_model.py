from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Load the T5 model and tokenizer
model_name = 't5-large'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Function to generate a response using the current and previous prompts
def generate_response_from_model(current_prompt, previous_prompts):
    # Combine the current prompt with previous prompts
    combined_input = f"Current Prompt: {current_prompt}\n"
    if previous_prompts:
        combined_input += f"Previous Prompts: {' '.join(previous_prompts)}\n"
    
    # Tokenize the input
    input_ids = tokenizer.encode(combined_input, return_tensors='pt')
    
    # Generate a response from the model
    outputs = model.generate(input_ids, max_length=100, num_beams=5, early_stopping=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response
