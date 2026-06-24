from typing import List, Optional
from langchain_core.documents import Document
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.reranker import rerank

_CACHED_BM25: Optional[BM25Retriever] = None
_CACHED_DOC_COUNT: int = 0


def hybrid_search(
    query: str,
    db: any,
    k_vector: int = 5,
    k_bm25: int = 5
) -> List[Document]:
    global _CACHED_BM25, _CACHED_DOC_COUNT

    if not query.strip():
        return []

    vector_docs = db.similarity_search(query, k=k_vector)
    try:
        if _CACHED_BM25 is None:
            db_data = db.get()
            all_docs = db_data.get("documents", [])
            all_metadatas = db_data.get("metadatas", [])
            
            docs = [
                Document(page_content=text, metadata=metadata or {})
                for text, metadata in zip(all_docs, all_metadatas)
            ]
            
            _CACHED_BM25 = BM25Retriever(docs)
            _CACHED_DOC_COUNT = len(docs)
            
        bm25_docs = _CACHED_BM25.retrieve(query, k=k_bm25)
    except Exception as e:
        print(f"Warning: BM25 retrieval failed, falling back to vector search. Error: {e}")
        bm25_docs = []

    seen = set()
    merged = []

    for doc in (vector_docs + bm25_docs):
        doc_id = doc.metadata.get("id") or doc.page_content
        if doc_id not in seen:
            merged.append(doc)
            seen.add(doc_id)

    print(f"Vector Docs: {len(vector_docs)}")
    print(f"BM25 Docs: {len(bm25_docs)}")
    print(f"Merged Docs: {len(merged)}")

    # 4. Rerank
    reranked_docs = rerank(
        query,
        merged,
        top_k=5
    )

    print(f"Reranked Docs: {len(reranked_docs)}")

    return reranked_docs