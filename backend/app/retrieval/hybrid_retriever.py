from retrieval.bm25_retriever import (
    BM25Retriever
)


def hybrid_search(
    query,
    db,
    k_vector=5,
    k_bm25=5
):

    # Vector Search

    vector_docs = db.similarity_search(
        query,
        k=k_vector
    )

    # BM25 Search

    all_docs = db.get()["documents"]

    all_metadatas = db.get()["metadatas"]

    from langchain_core.documents import (
        Document
    )

    docs = []

    for text, metadata in zip(
        all_docs,
        all_metadatas
    ):

        docs.append(
            Document(
                page_content=text,
                metadata=metadata
            )
        )

    bm25 = BM25Retriever(
        docs
    )

    bm25_docs = bm25.retrieve(
        query,
        k_bm25
    )

    # Merge

    seen = set()

    merged = []

    for doc in vector_docs + bm25_docs:

        text = doc.page_content

        if text not in seen:

            merged.append(doc)

            seen.add(text)

    return merged