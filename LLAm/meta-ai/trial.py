# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Model configuration
# MODEL_NAME = "meta-llama/Llama-3.2-3b"

# # Check if GPU is available
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# print("CUDA available:", torch.cuda.is_available())

# # Load the tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# # Load the model with mixed precision and memory efficiency
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,  # Use FP16 for GPU
#     device_map="auto",  # Automatically map layers to GPU/CPU based on available memory
#     low_cpu_mem_usage=True  # Reduce CPU memory usage during model load
# )

# # Function to generate response
# def generate_response(prompt):
#     # Tokenize input and move to the same device as the model
#     inputs = tokenizer(prompt, return_tensors="pt").to(device)

#     # Use `torch.no_grad()` to reduce memory usage and speed up computation
#     with torch.no_grad():
#         # Use mixed precision only on GPU
#         if torch.cuda.is_available():
#             with torch.cuda.amp.autocast():
#                 output = model.generate(
#                     **inputs,
#                     max_new_tokens=100,  # Hardcoded max token generation
#                     repetition_penalty=1.1,
#                     temperature=0.5,
#                     top_p=0.7,
#                     do_sample=False,
#                     use_cache=True  # Enable caching for faster generation
#                 )
#         else:
#             # For CPU, no need for mixed precision
#             output = model.generate(
#                 **inputs,
#                 max_new_tokens=100,
#                 repetition_penalty=1.1,
#                 temperature=0.5,
#                 top_p=0.7,
#                 do_sample=False,
#                 use_cache=True
#             )

#     # Decode and return the response
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response

# # Example usage
# prompt = input("Enter your prompt: ")
# response = generate_response(prompt)
# print("Response:", response)

import nltk_utils
nltk_utils.download('punkt')
nltk_utils.download('stopwords')
nltk_utils.download('wordnet')
nltk_utils.download('averaged_perceptron_tagger')
nltk_utils.download('punkt_tab')