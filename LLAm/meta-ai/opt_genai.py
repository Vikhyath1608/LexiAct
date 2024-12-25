from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import bitsandbytes as bnb
# Model configuration
MODEL_NAME = "meta-llama/Llama-3.1-8B"  # Replace with the correct path if the model is under a different namespace or name.

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("CUDA available:", torch.cuda.is_available())

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the model with mixed precision and efficient memory management
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # Use FP16 for GPU
#     device_map="auto",  # Automatically map layers to GPU/CPU based on available memory
#     low_cpu_mem_usage=True  # Reduce CPU memory usage during model load
# )


# Load the model with 8-bit quantization for faster inference and lower memory usage
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    load_in_8bit=True  # Enables 8-bit quantization
)

# Remove model.to(device) because Accelerate handles device mapping automatically

# Function to generate response
def generate_response(prompt, max_length=250, repetition_penalty=1.2, temperature=0.7, top_p=0.9):
    # Tokenize input and move to the same device as the model
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # If using GPU, enable automatic mixed precision
    with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        # Generate response
        output = model.generate(
            **inputs,
            max_new_tokens=max_length,
            repetition_penalty=repetition_penalty,  # Helps reduce repetition in response
            temperature=temperature,  # Controls randomness (0.7 is a good balance)
            top_p=top_p,  # Limits sampling to top p options (nucleus sampling)
            do_sample=True  # Allows more diverse responses
        )
    
    # Decode and return the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
prompt = input("Enter your prompt: ")
response = generate_response(prompt)
print("Response:", response)
