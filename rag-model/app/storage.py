'''
# In-memory storage for prompts
prompt_store = []

# Function to store a new prompt
def store_prompt(prompt):
    prompt_store.append(prompt)

# Function to retrieve similar prompts (using TF-IDF)
def retrieve_similar_prompts(query, top_n=3):
    if len(prompt_store) == 0:
        return []
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # Vectorize the stored prompts and the query
    vectorizer = TfidfVectorizer().fit_transform(prompt_store + [query])
    vectors = vectorizer.toarray()

    # Compute similarity between the query and stored prompts
    cosine_matrix = cosine_similarity(vectors[-1:], vectors[:-1]).flatten()
    
    '''

import sqlite3

# Initialize SQLite connection
conn = sqlite3.connect('data/prompts.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS prompts (id INTEGER PRIMARY KEY, prompt TEXT)''')
conn.commit()

# Store prompt in SQLite
def store_prompt(prompt):
    c.execute("INSERT INTO prompts (prompt) VALUES (?)", (prompt,))
    conn.commit()

# Retrieve all prompts from SQLite
def get_all_prompts():
    c.execute("SELECT prompt FROM prompts")
    return [row[0] for row in c.fetchall()]

    # Get top N similar prompts
    similar_indices = cosine_matrix.argsort()[-top_n:][::-1]
    similar_prompts = [prompt_store[i] for i in similar_indices if cosine_matrix[i] > 0]

    return similar_prompts
import sqlite3

# Initialize SQLite connection
conn = sqlite3.connect('data/prompts.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS prompts (id INTEGER PRIMARY KEY, prompt TEXT)''')
conn.commit()

# Store prompt in SQLite
def store_prompt(prompt):
    c.execute("INSERT INTO prompts (prompt) VALUES (?)", (prompt,))
    conn.commit()

# Retrieve all prompts from SQLite
def get_all_prompts():
    c.execute("SELECT prompt FROM prompts")
    return [row[0] for row in c.fetchall()]
