from langchain_huggingface import HuggingFaceEmbeddings
from app.rag.loading_data import DocumentLoader
from app.rag.cleaning_data import TextCleaner
from app.rag.chunking_data import chunking 
from app.config.settings import settings
from qdrant_client.models import PointStruct
from qdrant_client.models import Distance, VectorParams
import uuid
from qdrant_client import QdrantClient
import os
from qdrant_client.models import Filter, FieldCondition, MatchValue
from langchain_core.documents import Document
class VectorDB:
    def __init__(self):
        self.embeddings = (
            HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
                # "BAAI/bge-large-en-v1.5"
            )
        )
         
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

        if not self.client.collection_exists("documents"):
            self.client.create_collection(
                collection_name="documents",
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

    
    def storing_data(self,path):
        loader = DocumentLoader(path)
        docs = loader.load()

        cleaner = TextCleaner()
        cleaned_docs = cleaner.clean_documents(docs)
        cleaned_docs = cleaner.remove_duplicate_lines(cleaned_docs)

        chunker = chunking()
        chunks = chunker.chunk_documents(cleaned_docs)
        

        points=[]
        for chunk in chunks:

            vector = self.embeddings.embed_query(
                chunk.page_content
            )

            payload = {
                    "text": chunk.page_content,
                    **chunk.metadata
                }
            if "source" in payload:
                payload["source"] = payload["source"].replace("\\", "/")
            point = PointStruct(
                id = str(uuid.uuid4()),
                vector = vector,
                payload = payload

            )
            points.append(point)

        self.client.upsert(
            collection_name="documents",
            points=points
        )

    def storing_folder(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(
                folder_path,
                file_name
            )
            # Skip folders
            if not os.path.isfile(file_path):
                continue
            # Check duplicate
            if self.file_exists(file_path):

                print(
                    f"{file_name} already stored."
                )
                continue
            try:
                self.storing_data(file_path)
                print(
                    f"{file_name} stored successfully."
                )

            except Exception as e:
                print(
                    f"Error storing {file_name}: {e}"
                )
    
    def file_exists(self, file_path):
        normalized_path = str(file_path).replace("\\",'/')

        records, _ = self.client.scroll(
            collection_name="documents",
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=normalized_path)
                    )
                ]
            ),
            limit=1
        )
        return len(records) > 0
    
    def test_scroll(self):
        pass
    
    

# vector = VectorDB()
# # vector.storing_folder("documents")
# # vector.retrieve("insaurance coverage")
# vector.test_scroll()