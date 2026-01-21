# 1. Load documents
# 2. Chunk text
# 3. Generate embeddings for chunks
# 4. Store vectors in memory
# 5. Generate embedding for user query
# 6. Find similarity between embeddings
# 7. Select top-k chunks
# 8. Build prompt with context
# 9. Call LLM
# 10. Return answer
import os
import logging
from openai import OpenAI
import numpy as np

client = OpenAI()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

def load_documents(path):
    logging.info("Started load documents")
    docs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path,file)) as f:
                docs.append(f.read())
    return docs

def chunk_text(text, chunk_size = 200):
    logging.info("Started chunk text")
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

def embed_text(text):
    logging.info("Started embed text")
    response = client.embeddings.create(model="text-embedding-3-small",
                             input=text)
    return response.data[0].embedding

def build_index(docs):
    logging.info("Started build index")
    index=[]
    for doc in docs:
        chunks = chunk_text(doc)
        for chunk in chunks:
            index.append({
                "text": chunk,
                "embedding": embed_text(chunk)
            })
    return index
    
def cosine_similarity(a,b):
    logging.info("Started cos similarity")
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query, index, k=3):
    logging.info("Started retrieve")
    q_emb = embed_text(query)
    scored = [
        (cosine_similarity(q_emb, item["embedding"]), item["text"])
        for item in index
    ]
    scored.sort(reverse=True)
    return [text for _, text in scored[:k]]

def generate_answer(query, context):
    logging.info("Started generate answer")
    prompt = f"""
    Use the context below to answer the question.
    
    Context:
    {context}
    
    Question:
    {query}
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("hello")
    docs = load_documents("docs")
    index = build_index(docs)
    
    query = "What does the policy say about fraud?"
    context = retrieve(query, index)
    
    answer = generate_answer(query, context)
    print(answer)

    