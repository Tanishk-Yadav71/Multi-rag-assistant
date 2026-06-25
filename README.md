# Agentic Multi-RAG Research Assistant

> An advanced Agentic Retrieval-Augmented Generation (RAG) system featuring Hybrid Search, Corrective RAG (CRAG), Cross-Encoder Re-ranking, Multi-Agent Routing, Literature Review Generation, and Autonomous Recovery Workflows.


## 🚀 Overview

Agentic Multi-RAG is a research-focused AI assistant designed to overcome the limitations of traditional RAG systems.

Unlike standard retrieval pipelines that fail silently when context is poor, this system actively evaluates retrieval quality, diagnoses failures, and executes corrective actions before generating a response.

The assistant can intelligently search across multiple knowledge domains including:

* 📄 Research Papers
* 📚 Documentation
* 📝 Personal Notes

and automatically route queries to the most relevant knowledge source.

---

## ✨ Key Features

### 🔀 Multi-Agent Query Routing

Automatically classifies incoming queries and routes them to specialized workflows:

* Standard RAG
* Literature Review Mode
* Comparison Mode

---

### 🔍 Hybrid Retrieval Engine

Combines:

* Dense Semantic Search (ChromaDB + BGE Embeddings)
* Sparse Lexical Search (BM25)

to maximize retrieval quality.

---

### 🎯 Cross-Encoder Re-ranking

Uses:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

to remove noisy retrievals and prioritize highly relevant context before generation.

---

### 🧠 Corrective RAG (CRAG)

The system performs confidence evaluation before final response generation.

When retrieval quality is low, a self-correction workflow is triggered.

Supported recovery actions:

| Failure Type         | Recovery Action                  |
| -------------------- | -------------------------------- |
| wrong_database       | Switch knowledge base            |
| bad_query            | Rewrite query                    |
| insufficient_context | Deep retrieval + external search |

---

### 📖 Literature Review Workspace

Automatically generates:

* Research Summary
* Key Findings
* Research Trends
* Research Gaps
* Future Directions
* Source Citations

---

### ⚖️ Comparison Mode

Uses Maximum Marginal Relevance (MMR) retrieval to compare:

* Models
* Research Papers
* Architectures
* Methods

while maximizing information diversity.

---

## 🏗 Architecture

The retrieval pipeline combines routing, hybrid search, reranking, confidence evaluation, and corrective recovery.

<img width="1512" height="1600" alt="image" src="https://github.com/user-attachments/assets/b743b093-68fb-4787-be89-05a4c24b285f" />


---

## 🖥 Frontend

Modern React + Tailwind interface for interacting with the assistant.

<img width="1500" height="802" alt="image" src="https://github.com/user-attachments/assets/3824db6d-8cbd-4ea7-b493-0599f18f5980" />


Features:

* Real-time responses
* Source citations
* Literature review generation
* Comparison workspace
* Dark modern UI

---

## 🔄 Corrective RAG Workflow

When confidence falls below threshold:

The system can:

1. Rewrite the query
2. Switch vector databases
3. Increase retrieval depth
4. Escalate to ArXiv or web search

before generating the final response.

---

## 📚 Literature Review Example

<img width="1302" height="570" alt="image" src="https://github.com/user-attachments/assets/d7ca4e1d-afa7-4768-b593-de5b7c9857e6" />


Example output includes:

* Summary
* Key Findings
* Research Trends
* Research Gaps
* Future Work
* References

---

## ⚙️ Tech Stack

### Backend

* Python
* FastAPI
* LangChain

### Retrieval

* ChromaDB
* BM25Okapi
* HuggingFace Embeddings

### Re-ranking

* Cross Encoder
* MS MARCO MiniLM

### LLM

* Llama 3.3 70B
* Groq API

### Frontend

* React
* Vite
* Tailwind CSS

### Research Sources

* ArXiv API
* Web Search Fallback

---

## 📂 Project Structure

```text
agentic_multi_rag/
│
├── assets/
│   ├── architecture.png
│   ├── frontend.png
│   ├── crag.png
│   └── literature-review.png
│
├── backend/
│   ├── app/
│   ├── data/
│   └── vector_store/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
└── README.md
```

---

## 🚀 Getting Started

### Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.api.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 💡 Example Queries

### Research Paper Search

```text
What is Vision Transformer?
```

### Literature Review

```text
Generate a literature review on Vision Transformers.
```

### Comparison Mode

```text
Compare Vision Transformer and Swin Transformer.
```

### Documentation Search

```text
What is FastAPI?
```

### Notes Search

```text
Explain BCNF.
```

---

## 🎯 Future Roadmap

* Conversational Memory
* Streaming Responses
* PDF Uploads
* Citation Verification
* Research Report Export
* Multi-Agent Planning
* Docker Deployment

---

## ⭐ Author

**Aditya Yadav**

GitHub:
https://github.com/enx29

If you find this project interesting, consider giving it a star ⭐
