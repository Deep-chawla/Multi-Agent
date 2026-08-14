from app.rag.bm25_retriever import BM25Manager
from app.rag.retrieving_data import Retriever

class HybridRetriever:
    def __init__(self):
        self.qdrant = Retriever()
        self.bm25 = BM25Manager()
        self.bm25.build_index()
        

    def retrieve(self, query):
        bm25_docs = self.bm25.retrieve(query)

        qdrant_docs = self.qdrant.retrieve(query)
        merged_docs = bm25_docs + qdrant_docs

        unique_doc = []
        seen = set()

        for doc in merged_docs:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_doc.append(doc)

        return unique_doc

        

# h = HybridRetriever()
# h.retrieve("Battery lifespan")