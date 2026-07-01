from pathlib import Path
from langchain_core.tools import tool


@tool
def list_directory(directory_path: str = ".") -> str:
    """
    Lists all files and folders inside a directory.

    Use this tool whenever the user asks to:
    - List files
    - Show project structure
    - Show folder contents
    - Display files in a directory
    """

    try:
        path = Path(directory_path)

        if not path.exists():
            return f"Directory '{directory_path}' does not exist."

        if not path.is_dir():
            return f"'{directory_path}' is not a directory."

        items = []

        for item in sorted(path.iterdir()):
            if item.is_dir():
                items.append(f"[DIR]  {item.name}")
            else:
                items.append(f"[FILE] {item.name}")

        if not items:
            return "Directory is empty."

        return "\n".join(items)

    except Exception as e:
        return f"Error: {e}"