from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Agentic Multi-RAG Research Assistant",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def home():

    return {
        "message":
        "Agentic Multi-RAG API Running"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)