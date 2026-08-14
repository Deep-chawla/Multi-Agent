from langchain_text_splitters import RecursiveCharacterTextSplitter 
class chunking:
    def __init__(self, chunk_size=800, chunk_overlap=150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def chunk_documents(self, documents):
        chunks = self.splitter.split_documents(documents)
        return chunks

