from typing import Optional

def merge_results(left: Optional[dict[str, str]],right: Optional[dict[str, str]]) -> dict[str, str]:

    left = left or {}
    right = right or {}

    return {
        **left,
        **right,
    }