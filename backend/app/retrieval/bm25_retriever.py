import heapq
import re
from typing import List, Any
from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, docs: List[Any]):
        if not docs:
            raise ValueError("Document pool cannot be empty.")
            
        self.docs = docs
        self.tokenized_docs = [
            self._tokenize(doc.page_content)
            for doc in docs
        ]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def _tokenize(self, text: str) -> List[str]:
        """Lowercases and strips punctuation for accurate text matching."""
        return re.findall(r'\w+', text.lower())

    def retrieve(self, query: str, k: int = 5) -> List[Any]:
        """
        Retrieves the top-k relevant documents.
        Filters out completely irrelevant (0 or lower score) results.
        """
        if not query.strip():
            return []

        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        top_k_pairs = heapq.nlargest(
            k,
            ((doc, score) for doc, score in zip(self.docs, scores) if score > 0.0),
            key=lambda x: x[1]
        )

        return [doc for doc, _ in top_k_pairs]