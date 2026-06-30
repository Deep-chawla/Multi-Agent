from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Next node selected by Supervisor
    next: str