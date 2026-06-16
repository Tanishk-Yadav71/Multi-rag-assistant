from fastapi import FastAPI

from app.multi_rag.multi_rag import ask_question

app = FastAPI(
    title="Agentic Multi-RAG Research Assistant"
)

@app.get("/")
def home():
    return {
        "message": "Agentic Multi-RAG Research Assistant"
    }

@app.get("/ask")
def ask(query: str):

    return ask_question(query)