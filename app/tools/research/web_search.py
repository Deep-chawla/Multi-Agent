from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from app.config.settings import Settings

client = TavilySearch(api_key=Settings.TAVILY_API_KEY)

@tool
def web_search(query: str) -> str:
    """
    Search the internet.

    Use this tool whenever the user asks about:

    - latest news
    - sports results
    - companies
    - people
    - current events
    - technologies
    - products
    - anything requiring internet access

    Do NOT answer these questions from memory.
    """
    results = client.invoke(query)
    sources = []
    for index, item in enumerate(results.get("results", [])[:5], start=1):
        sources.append(
            f"""
    Source {index}

    Title:
    {item['title']}

    Content:
    {item['content']}

    URL:
    {item['url']}
    """
        )

    return "\n".join(sources)