# Multi-RAG Research Assistant

An Agentic Retrieval-Augmented Generation (RAG) platform combining hybrid retrieval, corrective self-reflection (CRAG), cross-encoder re-ranking, and automated research workflows.

---

## Overview

Traditional RAG implementations tend to fail silently when retrieval context is incomplete, noisy, or irrelevant. This project implements an agentic architecture that actively evaluates retrieval relevance, detects context gaps, and applies corrective recovery strategies before generating responses.

The system indexes and routes queries across distinct knowledge collections:
- Research papers (academic literature and preprints)
- Technical documentation (frameworks, APIs, and libraries)
- Personal notes and subject summaries

---

## Architecture and Core Mechanics

The pipeline is organized around multi-stage retrieval, self-evaluation, and recovery:

1. **Query Routing**: Classifies incoming prompts to select the appropriate retrieval mode (Standard Q&A, Literature Review, or Multi-entity Comparison) and target knowledge base.
2. **Hybrid Retrieval**: Executes dual-path retrieval merging dense vector similarity (ChromaDB with BGE embeddings) and sparse keyword matching (BM25Okapi) using reciprocal rank fusion.
3. **Cross-Encoder Re-ranking**: Evaluates document-query pairs using `cross-encoder/ms-marco-MiniLM-L-6-v2` to filter out low-scoring documents and optimize context window relevance.
4. **Corrective RAG (CRAG)**: Evaluates context relevance scores against a confidence threshold. If retrieval quality is insufficient, it triggers dynamic recovery routines before LLM synthesis.
5. **LLM Generation**: Synthesizes the final output with inline citations and grounded references using Llama 3.3 70B via Groq.

<img width="1512" height="1600" alt="System Architecture Diagram" src="https://github.com/user-attachments/assets/b743b093-68fb-4787-be89-05a4c24b285f" />

---

## Key Capabilities

### Multi-Agent Query Routing
Incoming queries are classified into specialized execution branches:
- **Standard RAG**: Direct retrieval and grounded question answering.
- **Literature Review**: Synthesizes key findings, methodological trends, gaps, and future research directions from indexed papers.
- **Comparison Mode**: Uses Maximum Marginal Relevance (MMR) retrieval to contrast architectures, methods, or models while maximizing source diversity.

### Hybrid Retrieval Engine
- **Dense Semantic Search**: ChromaDB vector store backed by HuggingFace BGE embeddings.
- **Sparse Lexical Search**: BM25 ranking for exact keyword, acronym, and identifier matching.

### Cross-Encoder Re-ranking
Raw candidate documents from hybrid search are scored jointly with the query through a cross-encoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2`), removing irrelevant passages and ensuring top-ranked context fits within the model's high-attention tokens.

### Corrective RAG (CRAG) Recovery Workflows
When retrieval confidence drops below acceptable thresholds, the system executes one or more recovery policies:

| Failure Mode | Diagnosis | Recovery Action |
| --- | --- | --- |
| `wrong_database` | Query domain mismatches current collection | Switch to appropriate knowledge base |
| `bad_query` | Query is ambiguous or poorly framed | Rephrase and expand query terms |
| `insufficient_context` | Candidate passages lack depth | Deepen retrieval k-factor and query ArXiv / web fallback |

---

## User Interface

The frontend provides an interactive workspace built with React, Vite, and Tailwind CSS.

<img width="1500" height="802" alt="Web Application Interface" src="https://github.com/user-attachments/assets/3824db6d-8cbd-4ea7-b493-0599f18f5980" />

Features:
- Real-time grounded responses with expandable source citations
- Dedicated literature review generator with structured sections
- Side-by-side comparative analysis view
- Modern dark-themed dashboard

### Literature Review Workspace Example

<img width="1302" height="570" alt="Literature Review Workspace" src="https://github.com/user-attachments/assets/d7ca4e1d-afa7-4768-b593-de5b7c9857e6" />

Outputs include:
- Executive summary
- Core methodology and key findings
- Current research trends
- Identified gaps and limitations
- Suggested future work
- Verified reference links

---

## Tech Stack

### Backend and Orchestration
- **Runtime**: Python 3.10+
- **Framework**: FastAPI, Uvicorn
- **Orchestration**: LangChain, custom CRAG state graphs

### Retrieval and Ranking
- **Vector Store**: ChromaDB
- **Dense Embeddings**: HuggingFace BGE (`BAAI/bge-small-en-v1.5` / `bge-base-en-v1.5`)
- **Lexical Search**: BM25Okapi
- **Re-ranking**: Cross-Encoder (`ms-marco-MiniLM-L-6-v2`)

### Inference and Fallback
- **LLM**: Llama 3.3 70B (via Groq API)
- **External Retrieval**: ArXiv API, Web Search fallback

### Frontend
- **Framework**: React 19, Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios

---

## Project Structure

```text
agentic-multi-rag-research-assistant/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI endpoints and routes
│   │   ├── core/            # Config, settings, and logging
│   │   ├── rag/             # Retrieval, reranking, and CRAG pipelines
│   │   └── services/        # Query routing, ArXiv, and web integration
│   ├── data/                # Document sources and raw texts
│   ├── vector_store/        # Persisted ChromaDB indexes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # UI widgets and inputs
│   │   ├── pages/           # Chat, Literature Review, and Compare views
│   │   └── services/        # API integration clients
│   ├── package.json
│   └── vite.config.js
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm
- Groq API key

### 1. Backend Setup

Navigate to the `backend` directory, create a virtual environment, and install dependencies:

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory with your API credentials:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the FastAPI backend server:

```bash
uvicorn app.api.main:app --reload
```

- API Base URL: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

In a separate terminal, navigate to the `frontend` directory and start the development server:

```bash
cd frontend
npm install
npm run dev
```

- Web UI: `http://localhost:5173`

---

## Example Queries

### Research Paper Query
```text
Explain the self-attention mechanism in Vision Transformers and its computational scaling.
```

### Literature Review Synthesis
```text
Generate a structured literature review on Vision Transformers in medical image segmentation.
```

### Comparative Analysis
```text
Compare Vision Transformer (ViT) and Swin Transformer regarding architectural hierarchy and computational complexity.
```

### Documentation and Reference Retrieval
```text
How does FastAPI handle dependency injection with yield statements?
```

### Concepts and Course Notes
```text
Explain Boyce-Codd Normal Form (BCNF) decomposition with an example.
```

---

## Roadmap

- Conversational memory with session persistence
- Streaming token responses via WebSockets / SSE
- In-browser PDF upload and automated chunking/indexing
- Automated citation hallucination verification
- Export reports to Markdown and PDF formats
- Multi-agent planner for complex multi-hop queries
- Containerized deployment with Docker and Docker Compose

---

## Author

**Tanishk Yadav**

- GitHub: [Tanishk-Yadav71](https://github.com/Tanishk-Yadav71)
- Repository: [Multi-rag-assistant](https://github.com/Tanishk-Yadav71/Multi-rag-assistant)
