
from sentence_transformers import CrossEncoder
class re_rank:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


    def rerank(self,query: str,docs_with_scores: list,top_k: int = 5):
        if not docs_with_scores:
            return []

        documents = [doc for doc in docs_with_scores]

        pairs = [
                (query, doc.page_content)
                for doc in documents
            ]

        rerank_scores = self.model.predict(pairs)

        ranked_docs = list(
            zip(
                documents,
                rerank_scores
            )
            )

        ranked_docs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, score in ranked_docs[:top_k]]





