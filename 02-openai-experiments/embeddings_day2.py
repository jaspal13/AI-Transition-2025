from openai import OpenAI
import numpy as np

client = OpenAI()

def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

# Step 1 - sample docs  
docs = [
    "Car insurance covers collision and liability.",
    "Home insurance protects against fire and theft.",
    "Life insurance provides financial support.",
    "Travel insurance covers trip cancellations and emergencies."
]

# Step 2 - embed all docs  
doc_embeddings = [embed(d) for d in docs]

# Step 3 - embed a query  
query = "What covers trip issues?"
query_emb = embed(query)

# Step 4 - compute similarity  
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

scores = [cosine_similarity(query_emb, d) for d in doc_embeddings]

# Step 5 - get best match  
best_index = np.argmax(scores)
print("Query:", query)
print("Best Match:", docs[best_index])
print("Similarity Score:", scores[best_index])
