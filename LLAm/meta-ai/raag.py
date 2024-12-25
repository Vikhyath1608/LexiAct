# Import required libraries
import sqlite3
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity

# Database Setup
def setup_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('prompts_responses.db')
    cursor = conn.cursor()

    # Create table to store prompts and responses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT,
        response TEXT
    )
    ''')
    conn.commit()
    return conn, cursor

# Model Setup
def setup_models():
    # Model configuration
    MODEL_NAME = "meta-llama/Llama-3.2-3b"  # Update with correct path if needed

    # Check if GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Load the model with FP16 precision if GPU is available
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)

    # Move model to the appropriate device
    model.to(device)

    # Load the retriever model
    retriever_model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')  # Update with a suitable model

    return device, tokenizer, model, retriever_model

# Setup FAISS Index
def setup_faiss_index(retriever_model, documents):
    # Encode the documents to get embeddings
    document_embeddings = retriever_model.encode(documents, convert_to_tensor=False)

    # Create an index using faiss
    index = faiss.IndexFlatL2(document_embeddings.shape[1])
    index.add(np.array(document_embeddings))
    return index

# Function to retrieve top-k similar documents
def retrieve_documents(index, retriever_model, query, documents, top_k=5):
    query_embedding = retriever_model.encode([query], convert_to_tensor=False)
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [documents[i] for i in indices[0]]

# Function to check if prompts are linked based on cosine similarity
def are_prompts_linked(current_prompt, previous_prompt, retriever_model, threshold=0.7):
    # Generate embeddings for both prompts
    current_embedding = retriever_model.encode([current_prompt])
    previous_embedding = retriever_model.encode([previous_prompt])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(current_embedding, previous_embedding)[0][0]
    return similarity >= threshold

# Function to generate response and store it in the database
def generate_rag_response_with_linked_memory(prompt, cursor, device, tokenizer, model, retriever_model, index, documents, max_length=250, repetition_penalty=1.2, temperature=0.7, top_p=0.9, top_k_retrievals=3, similarity_threshold=0.7):
    # Check if there are any previous prompts and responses in the database
    cursor.execute('SELECT prompt, response FROM conversation ORDER BY id DESC LIMIT 1')
    last_row = cursor.fetchone()
    
    # Determine context based on prompt linking
    context = ""
    if last_row:
        last_prompt, last_response = last_row
        if are_prompts_linked(prompt, last_prompt, retriever_model, threshold=similarity_threshold):
            # If linked, build context with previous prompt-response
            context = f"User: {last_prompt} Bot: {last_response} "
    
    # Append the current prompt to the context
    context += f"User: {prompt} "
    
    # Retrieve relevant documents based on the current prompt
    retrieved_docs = retrieve_documents(index, retriever_model, prompt, documents, top_k=top_k_retrievals)
    
    # Combine the context and retrieved documents
    final_context = " ".join(retrieved_docs) + " " + context
    
    # Tokenize input and move to the same device as the model
    inputs = tokenizer(final_context, return_tensors="pt").to(device)
    
    # Generate response
    output = model.generate(
        **inputs, 
        max_new_tokens=max_length,
        repetition_penalty=repetition_penalty,
        temperature=temperature,
        top_p=top_p,
        do_sample=True
    )
    
    # Decode and return the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Store the current prompt and response in the database
    cursor.execute('INSERT INTO conversation (prompt, response) VALUES (?, ?)', (prompt, response))
    conn.commit()
    
    return response

# Main function to initialize and interact
def main():
    # Setup database
    conn, cursor = setup_database()
    
    # Sample documents (corpus) for the retriever
    documents = [
        "The sun is the star at the center of the Solar System.",
        "Machine learning is a subset of artificial intelligence.",
        "The capital of France is Paris.",
        # Add more documents here...
    ]
    
    # Setup models and device
    device, tokenizer, model, retriever_model = setup_models()
    
    # Setup FAISS index for document retrieval
    index = setup_faiss_index(retriever_model, documents)
    
    # Main interaction loop
    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break

        # Generate response with linked memory
        response = generate_rag_response_with_linked_memory(prompt, cursor, device, tokenizer, model, retriever_model, index, documents)
        print("Response:", response)

if __name__ == "__main__":
    main()
