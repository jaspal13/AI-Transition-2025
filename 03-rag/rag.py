Jimport os
from openai import OpenAI
import numpy as np

client = OpenAI()

# -----------------------------
# 1. SIMPLE TEXT CHUNKING
# -----------------------------
def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size

    return chunks

# -----------------------------
# 2. EMBEDDING FUNCTION
# -----------------------------
def embed(text):
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(resp.data[0].embedding)

# -----------------------------
# 3. LOAD + CHUNK + EMBED DOCS
# -----------------------------
def build_knowledge_base():
    kb_chunks = []
    kb_embeddings = []

    for filename in os.listdir("docs"):
        path = os.path.join("docs", filename)
        if not filename.endswith(".txt"):
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for c in chunks:
            kb_chunks.append(c)
            kb_embeddings.append(embed(c))

    return kb_chunks, kb_embeddings


# -----------------------------
# 4. COSINE SIMILARITY
# -----------------------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -----------------------------
# 5. RETRIEVE TOP-K CHUNKS
# -----------------------------
def retrieve_relevant_chunks(query, kb_chunks, kb_embeddings, top_k=3):
    q_emb = embed(query)

    similarities = [
        cosine_similarity(q_emb, emb)
        for emb in kb_embeddings
    ]

    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [kb_chunks[i] for i in top_indices]


# -----------------------------
# 6. CALL LLM WITH CONTEXT
# -----------------------------
def ask_llm(question, context_chunks):
    context = "\n\n".join([f"[CHUNK] {c}" for c in context_chunks])

    prompt = f"""
You are an expert assistant.

Use ONLY the information from the context below to answer the question.
If the answer is not present, say "I don't know."

Context:
{context}

Question:
{question}

Answer with citations from the chunks.
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0
    )

    return resp.choices[0].message.content


# -----------------------------
# 7. MAIN FLOW
# -----------------------------
if __name__ == "__main__":
    print("Loading knowledge base...")
    kb_chunks, kb_embeddings = build_knowledge_base()
    print(f"Loaded {len(kb_chunks)} chunks.")

    while True:
        q = input("\nAsk a question: ")
        if q.lower() in ["exit", "quit"]:
            break

        relevant = retrieve_relevant_chunks(q, kb_chunks, kb_embeddings)

        print("\nRetrieved Chunks:")
        for c in relevant:
            print("----")
            print(c[:200], "...")

        print("\nAI Answer:")
        print(ask_llm(q, relevant))
