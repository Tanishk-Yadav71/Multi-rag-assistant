from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, docs):

        self.docs = docs

        self.tokenized_docs = [
            doc.page_content.lower().split()
            for doc in docs
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_docs
        )

    def retrieve(
        self,
        query,
        k=5
    ):

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(self.docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, score in ranked[:k]
        ]