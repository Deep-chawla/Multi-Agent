from typing import Optional
from typing import List

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