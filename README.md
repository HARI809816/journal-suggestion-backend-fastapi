## 🔁 Forwarding Topics to a Chroma-Based RAG Service (No ML Model)

This backend **does not run any machine learning model**.

Instead, it forwards the topic to another **FastAPI microservice** that uses:

- 🧠 Embeddings (OpenAI / Sentence Transformers / any model)
- 🗂️ **ChromaDB** as the vector database
- 🔍 Top-K semantic similarity search

The microservice returns the most relevant journal topics using vector similarity.

---

## ⚙️ How the System Works

### **1️⃣ React Frontend → Main FastAPI Backend**
User enters a topic, which is received through:


POST /forward-topic/
---

### **2️⃣ Main FastAPI → RAG/Chroma Service**
Your backend forwards the topic to another FastAPI RAG service:

python
async with AsyncClient() as client:
    response = await client.post(
        RAG_SERVICE_URL,
        json={"query": topic, "top_k": top_k}
    )

3️⃣ RAG Service (ChromaDB) Processing

  1. The RAG microservice performs:

  2. Embedding generation for the query

  3. Vector search using ChromaDB

  4. Retrieves top-K similar results

Returns:

  - journal names

  - similarity scores

  - metadata from the Chroma collection

Example ChromaDB search:

results = collection.query(
    query_texts=[query],
    n_results=top_k
)
