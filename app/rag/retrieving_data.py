from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from langchain_core.documents import Document
from app.config.settings import settings

class Retriever:
    def __init__(self):

        
        self.embeddings = (
            HuggingFaceEmbeddings(
                model_name=
                "sentence-transformers/all-MiniLM-L6-v2"
                # "BAAI/bge-large-en-v1.5"
            )
        )

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )



    # def retrieve(self, query, k=15):

    #     docs_with_scores = self.vectorstore.similarity_search_with_score(query, k=k)
    #     return docs_with_scores

    def retrieve(self, query, k=15):

        query_vector = self.embeddings.embed_query(
            query
        )

        results = self.client.query_points(
            collection_name="documents",
            query=query_vector,
            limit=k
        )


        docs = []

        for point in results.points:

            doc = Document(
                page_content=point.payload["text"],
                metadata={
                    key: value
                    for key, value in point.payload.items()
                    if key != "text"
                }
            
            )

            docs.append(
                (
                    doc
                )
            )

        return docs
    