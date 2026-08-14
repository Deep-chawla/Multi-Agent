import wikipediaapi
from langchain_core.tools import tool

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="MultiAgentResearchBot/1.0"
)


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for factual information.

    Use this tool when the user asks about:
    - People
    - Places
    - Historical events
    - Scientific concepts
    - Programming languages
    - Technologies
    - General knowledge

    Prefer this over web search when current information is NOT required.
    """

    page = wiki.page(query)

    if not page.exists():
        return "No Wikipedia article found."

    return (
        f"Title: {page.title}\n\n"
        f"Summary:\n{page.summary[:2000]}\n\n"
        f"URL: {page.fullurl}"
    )