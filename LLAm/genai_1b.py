from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Model configuration
MODEL_NAME = "meta-llama/Llama-3.2-1B"
QUANTIZE = False  # Set to True if you want to use quantization

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the model with optional quantization
if QUANTIZE:
    # Quantize the model to int8 for faster and lighter inference (requires bitsandbytes library)
    from transformers import BitsAndBytesConfig
    
    quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, quantization_config=quantization_config)
else:
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Move model to the appropriate device
model.to(device)

# Function to generate response
def generate_response(prompt, max_length=256, repetition_penalty=1.2, temperature=0.7):
    # Tokenize input and move to the same device as the model
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate response
    output = model.generate(
        **inputs, 
        max_new_tokens=max_length,
        repetition_penalty=repetition_penalty,  # Helps reduce repetition in response
        temperature=temperature,  # Controls randomness (0.7 is a good balance)
        do_sample=True,  # Allows more diverse responses
        top_k=50  # Limits sampling to top k options
    )
    
    # Decode and return the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
prompt = input("Enter your prompt: ")
response = generate_response(prompt)
print("Response:", response)
