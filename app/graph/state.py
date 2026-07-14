from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from app.graph.reducer import merge_completed_steps,merge_results,merge_ready_steps,merge_executions
from app.agents.superviser.schema import TaskExecution




class PlanStep(TypedDict):
    id: int
    agent: str
    task: str
    depends_on: list[int]



class GraphState(TypedDict):

    # Conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Execution plan
    plan: list[PlanStep]

    # Execution state
    executions: Annotated[dict[int, TaskExecution],merge_executions]

    # Current task being executed
    current_task: PlanStep | None

    # Agent results
    results: Annotated[dict[str, str], merge_results]