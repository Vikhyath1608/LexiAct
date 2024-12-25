from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Model configuration
# MODEL_NAME = "meta-llama/Llama-3.1-8B"
MODEL_NAME = "meta-llama/Llama-3.2-3b" 

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("CUDA available:", torch.cuda.is_available())

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the model with mixed precision and efficient memory management
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # Use FP16 for GPU
    device_map="auto",  # Automatically map layers to GPU/CPU based on available memory
    low_cpu_mem_usage=True  # Reduce CPU memory usage during model load
)

# Function to generate response
def generate_response(prompt, max_length=100, repetition_penalty=1.1, temperature=0.5, top_p=0.7, do_sample=False):
    # Tokenize input and move to the same device as the model
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # If using GPU, enable automatic mixed precision
    with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        # Generate response
        output = model.generate(
            **inputs,
            max_new_tokens=max_length,  # Reduce token generation length for faster output
            repetition_penalty=repetition_penalty,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            use_cache=True  # Speed up generation by caching attention
        )
    
    # Decode and return the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
prompt = input("Enter your prompt: ")
response = generate_response(prompt)
print("Response:", response)
