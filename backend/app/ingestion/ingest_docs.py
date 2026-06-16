from ingest_utils import ingest_folder

ingest_folder(
    "backend/data/docs",
    "backend/vector_store/docs_db"
)