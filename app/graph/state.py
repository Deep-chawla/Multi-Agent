from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages



class PlanStep(TypedDict):
    agent: str
    task: str


class GraphState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Current node to execute
    next: str

    # Execution plan
    plan: list[PlanStep]

    # Current step in the plan
    current_step: int

    # Store outputs from each agent
    results: dict[str, str]