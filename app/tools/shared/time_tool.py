from datetime import datetime
from langchain_core.tools import tool


@tool
def current_time() -> str:
    """
    Returns the current local date and time.
    Useful for answering questions about the current time or date.
    """

    now = datetime.now()

    return now.strftime("%d %B %Y, %I:%M:%S %p")