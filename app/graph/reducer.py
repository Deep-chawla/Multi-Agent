from typing import Optional
from typing import List
from app.agents.superviser.schema import TaskExecution

def merge_results(left: Optional[dict[str, str]],right: Optional[dict[str, str]]) -> dict[str, str]:

    left = left or {}
    right = right or {}

    return {
        **left,
        **right,
    }

def merge_completed_steps(left: Optional[list[int]],right: Optional[list[int]],) -> list[int]:
    left = left or []
    right = right or []

    merged = list(left)

    for step in right:
        if step not in merged:
            merged.append(step)

    return merged



def merge_ready_steps(left: Optional[list], right: Optional[list]) -> list:
    return right or []

from typing import Optional

def merge_executions(left: Optional[dict[int, TaskExecution]],right: Optional[dict[int, TaskExecution]],) -> dict[int, TaskExecution]:

    left = left or {}
    right = right or {}

    merged = dict(left)

    for task_id, execution in right.items():
        merged[task_id] = execution

    return merged