import requests

from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def url_reader(url: str) -> str:
    """
    Read the content of a webpage.

    Use this tool whenever the user:
    - Provides a URL
    - Wants to summarize a webpage
    - Wants to read an article
    - Wants to understand documentation
    - Wants information from a webpage

    Input should be a valid URL.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "No Title"
        text = soup.get_text(separator="\n", strip=True)

        # Prevent sending huge pages to the LLM
        text = text[:8000]
        return f"""
Title:
{title}

Content:
{text}

Source:
{url}
"""

    except Exception as e:
        return f"Error reading webpage: {e}"