from langchain_core.tools import tool
from app.rag.rag_service import RagService

rag_service = RagService()


@tool
def rag_tool(query: str) -> str:
    """
    Retrieve relevant information from the knowledge base.
    """

    docs = rag_service.retrieve(query)

    if not docs:
        return "No relevant information found."

    context = ""

    for doc in docs:

        source = doc.metadata.get("source", "Unknown")

        page = doc.metadata.get("page", "N/A")

        context += (
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {doc.page_content}\n\n"
        )

    return context