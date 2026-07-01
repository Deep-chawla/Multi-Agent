from pathlib import Path
from langchain_core.tools import tool

@tool
def read_file(file_path: str) -> str:
    """
    Reads the contents of a text file.

    Use this tool whenever the user asks to:
    - Read a file
    - Open a file
    - Show a file
    - Display file contents
    - Explain a file
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"File '{file_path}' does not exist."

        if not path.is_file():
            return f"'{file_path}' is not a file."

        return path.read_text(encoding="utf-8")

    except Exception as e:
        return f"Error reading file: {e}"
    

@tool
def file_exists(file_path: str) -> bool:
    """
    Checks whether a file or directory exists.

    Use this tool whenever the user asks:
    - Does this file exist?
    - Is this path valid?
    - Check if a file exists.
    """

    return Path(file_path).exists()