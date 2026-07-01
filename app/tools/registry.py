from app.tools.shared.calculator import calculator
from app.tools.shared.time_tool import current_time
from app.tools.coding.python_executor import python_executor
from app.tools.coding.filesystem.read_file import read_file, file_exists
from app.tools.coding.filesystem.list_directories import list_directory



SHARED_TOOLS = [
    calculator,
    current_time
]

CODING_TOOLS = [
    *SHARED_TOOLS,
    python_executor,
    read_file,
    file_exists,
    list_directory
]