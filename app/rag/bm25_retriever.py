from langchain_core.documents import Document
from qdrant_client import QdrantClient
from langchain_community.retrievers import BM25Retriever
from app.config.settings import settings


class BM25Manager:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        

    def load_documents_from_qdrant(self):
        offset = None
        records =[]
        while True:
            record, offset = self.client.scroll(
                collection_name="documents",
                limit=5,
                offset= offset,
                with_payload=True,
                with_vectors=False
            )
            records.extend(record)
            if offset is None:
                break


        docs = []
        for record in records:
            doc = Document(
                page_content=record.payload["text"],
                metadata = {
                    key:value
                    for key,value in record.payload.items()
                    if key!='text'
                }
            )

            docs.append(doc)

        return docs

    def build_index(self):
        if not self.collection_exists():
            print("Documents collection not found.")
            self.bm25 = None
            return

        docs = self.load_documents_from_qdrant()

        if not docs:
            print("No documents found.")
            self.bm25 = None
            return

        self.bm25 = BM25Retriever.from_documents(docs)
        print("BM25 Index Built Successfully")

    def retrieve(self, query):

        if self.bm25 is None:
            return []
        return self.bm25.invoke(query)
    
    def refresh_index(self):
        self.build_index()
    

    def collection_exists(self):
        collections = self.client.get_collections()
        collection_names = [
            c.name
            for c in collections.collections
        ]
        return "documents" in collection_names

# b = BM25Manager()
# b.build_index()

# results = b.retrieve(
#     "battery lifespan"
# )

# print(type(results))
# print(type(results[0]))