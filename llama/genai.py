# from transformers import LlamaForCausalLM, LlamaTokenizer
from huggingface_hub import login
import torch

# Login to Hugging Face
login('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')  # Replace with your Hugging Face token

# Load pre-trained LLaMA model and tokenizer from Hugging Face
# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# Function to generate response from the prompt
def generate_response(prompt, max_length=256):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=max_length)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example prompt
prompt = input("Enter your prompt: ")

# Generate response
response = generate_response(prompt)
print("Response:", response)
