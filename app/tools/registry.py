from app.tools.shared.calculator import calculator
from app.tools.shared.time_tool import current_time
from app.tools.coding.python_executor import python_executor
from app.tools.coding.filesystem.read_file import read_file, file_exists
from app.tools.coding.filesystem.list_directories import list_directory
from app.tools.research.web_search import web_search
from app.tools.research.wikipedia import wikipedia_search
from app.tools.research.url_reader import url_reader
from app.tools.knowledge.rag_tool import rag_tool



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

RESEARCH_TOOLS = [
    web_search,
    wikipedia_search,
    url_reader
]

RAG_TOOLS = [
    rag_tool
]