from app.rag.hybrid_retriever import HybridRetriever
from app.rag.re_ranking import re_rank


class RagService:

    def __init__(self):
        self.hybrid = HybridRetriever()
        self.reranker = re_rank()

    def retrieve(self, query: str):

        result = self.hybrid.retrieve(query)

        if not result:
            return []

        top_docs = self.reranker.rerank(
            query,
            result,
            top_k=5
        )

        return top_docs