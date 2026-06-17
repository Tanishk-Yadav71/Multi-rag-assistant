from retrieval.bm25_retriever import BM25Retriever
from retrieval.reranker import rerank
from langchain_core.documents import Document


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

    # Load all documents for BM25
    all_docs = db.get()["documents"]
    all_metadatas = db.get()["metadatas"]

    docs = [
        Document(
            page_content=text,
            metadata=metadata
        )
        for text, metadata in zip(
            all_docs,
            all_metadatas
        )
    ]

    # BM25 Search
    bm25 = BM25Retriever(docs)

    bm25_docs = bm25.retrieve(
        query,
        k_bm25
    )

    # Merge and Deduplicate
    seen = set()
    merged = []

    for doc in vector_docs + bm25_docs:

        if doc.page_content not in seen:

            merged.append(doc)

            seen.add(
                doc.page_content
            )

    print(
        f"Vector Docs: {len(vector_docs)}"
    )

    print(
        f"BM25 Docs: {len(bm25_docs)}"
    )

    print(
        f"Merged Docs: {len(merged)}"
    )

    # Rerank
    reranked_docs = rerank(
        query,
        merged,
        top_k=5
    )

    print(
        f"Reranked Docs: {len(reranked_docs)}"
    )

    return reranked_docs