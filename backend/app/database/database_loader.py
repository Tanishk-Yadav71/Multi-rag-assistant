from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

VECTOR_STORE_DIR = BASE_DIR / "vector_store"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

papers_db = Chroma(
    persist_directory=str(
        VECTOR_STORE_DIR / "papers_db"
    ),
    embedding_function=embeddings
)

docs_db = Chroma(
    persist_directory=str(
        VECTOR_STORE_DIR / "docs_db"
    ),
    embedding_function=embeddings
)

notes_db = Chroma(
    persist_directory=str(
        VECTOR_STORE_DIR / "notes_db"
    ),
    embedding_function=embeddings
)