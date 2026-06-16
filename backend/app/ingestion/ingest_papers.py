from ingest_utils import ingest_folder

ingest_folder(
    "backend/data/papers",
    "backend/vector_store/papers_db"
)