import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_chroma import Chroma


def ingest_folder(data_path, persist_directory):

    documents = []

    for file in os.listdir(data_path):

        file_path = os.path.join(data_path, file)

        if file.endswith(".pdf"):

            loader = PyPDFLoader(file_path)

        elif file.endswith(".txt"):

            loader = TextLoader(file_path,encoding="utf-8")

        else:
            continue

        docs = loader.load()

        documents.extend(docs)

    print(f"Loaded documents: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Generated chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    try:
        db.persist()
    except:
        pass

    print(f"Database created successfully at: {persist_directory}")