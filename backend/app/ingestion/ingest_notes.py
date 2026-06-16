from ingest_utils import ingest_folder

ingest_folder(
    "backend/data/notes",
    "backend/vector_store/notes_db"
)