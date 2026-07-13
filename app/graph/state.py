from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.graph.reducer import merge_results



class PlanStep(TypedDict):
    agent: str
    task: str


class GraphState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Execution plan
    plan: list[PlanStep]


    # Store outputs from each agent
    results:Annotated[dict[str, str],merge_results]