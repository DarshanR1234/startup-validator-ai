from tavily import TavilyClient

from app.config.settings import settings


tavily_client = TavilyClient(
    api_key=settings.tavily_api_key
)


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web and return relevant results.
    """

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )

    return response.get("results", [])