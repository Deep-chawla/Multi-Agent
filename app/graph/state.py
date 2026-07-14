from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.graph.reducer import merge_completed_steps,merge_results,merge_ready_steps



class PlanStep(TypedDict):
    id: int
    agent: str
    task: str
    depends_on: list[int]

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
    completed_steps: Annotated[list[int],merge_completed_steps]
    current_task: PlanStep | None
    ready_steps: Annotated[list[PlanStep], merge_ready_steps]