from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

papers_db = Chroma(
    persist_directory="backend/vector_store/papers_db",
    embedding_function=embeddings
)

docs_db = Chroma(
    persist_directory="backend/vector_store/docs_db",
    embedding_function=embeddings
)

notes_db = Chroma(
    persist_directory="backend/vector_store/notes_db",
    embedding_function=embeddings
)