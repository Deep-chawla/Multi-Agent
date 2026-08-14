import io
import traceback
from contextlib import redirect_stdout

from langchain_core.tools import tool


BLOCKED_KEYWORDS = [
    "import os",
    "import subprocess",
    "import shutil",
    "import socket",
    "import requests",
    "__import__",
    "eval(",
    "exec(",
    "open(",
]


@tool
def python_executor(code: str) -> str:
    """
    Executes Python code and returns the output.

    Use this tool whenever the user asks to:
    - Run Python code
    - Execute a Python script
    - Verify Python output
    - Debug Python code
    """
    print("Executer Getting called")

    # Basic safety checks
    for keyword in BLOCKED_KEYWORDS:
        if keyword in code:
            return f"Execution blocked. '{keyword}' is not allowed."

    output = io.StringIO()

    try:
        with redirect_stdout(output):
            exec(code, {})

        result = output.getvalue().strip()

        if not result:
            return "Code executed successfully."

        return result

    except Exception:
        return traceback.format_exc()