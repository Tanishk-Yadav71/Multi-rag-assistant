# Agentic Multi-RAG Research Assistant

An advanced Retrieval-Augmented Generation (RAG) system that routes queries across multiple knowledge sources, retrieves relevant information, and generates source-backed answers using LLMs.

## Features

- Multi-RAG Architecture
- Multiple Vector Databases (Papers, Docs, Notes)
- Intelligent Query Routing
- Research Paper Question Answering
- Research Paper Comparison
- Source Citation Generation
- Groq LLM Integration

## Tech Stack

- Python
- FastAPI
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq (Llama 3.3 70B)

## Project Structure

```text
backend/
├── app/
│   ├── comparison/
│   ├── database/
│   ├── ingestion/
│   └── multi_rag/
│
├── data/
│   ├── papers/
│   ├── docs/
│   └── notes/
│
└── vector_store/
```

## Setup

```bash
git clone https://github.com/enx29/agentic-multi-rag-research-assistant.git

cd agentic-multi-rag-research-assistant

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

## Run

```bash
python backend/app/multi_rag/multi_rag.py
```

## Example Queries

```text
What is Vision Transformer?

How do FastAPI routes work?

What is BCNF?

Compare Vision Transformer and Swin Transformer
```

## Current Features

✅ Multi-RAG

✅ Query Routing

✅ Multiple Vector Databases

✅ Research Paper QA

✅ Paper Comparison

✅ Citation Generation

## Upcoming

- Hybrid Retrieval (BM25 + Embeddings)
- Reranking
- Literature Review Generation
- Web Search Integration
- Conversation Memory
- LangGraph Agents

## Author

Aditya Yadav

GitHub: https://github.com/enx29
