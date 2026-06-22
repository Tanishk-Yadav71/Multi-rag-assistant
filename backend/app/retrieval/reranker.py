import torch
import heapq
from typing import List, Any
from sentence_transformers import CrossEncoder

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device=device
)


def rerank(
    query: str,
    documents: List[Any],
    top_k: int = 5,
    min_relevance_score: float = -4.0  
) -> List[Any]:
    if not documents or not query.strip():
        return []

    pairs = [
        (query, doc.page_content)
        for doc in documents
    ]
    scores = reranker_model.predict(pairs, convert_to_numpy=True)
    top_k_pairs = heapq.nlargest(
        top_k,
        (
            (doc, score) 
            for doc, score in zip(documents, scores) 
            if score >= min_relevance_score
        ),
        key=lambda x: x[1]
    )

    return [doc for doc, _ in top_k_pairs]