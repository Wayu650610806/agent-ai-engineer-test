"""Agent 2: Web Search Agent.

Searches the web via the Google Custom Search JSON API and gathers
information from the top N sources, then hands the results off to the
Post-process Agent.
"""
import requests

GOOGLE_SEARCH_ENDPOINT = "https://www.googleapis.com/customsearch/v1"


class WebSearchAgent:
    """Agent 2 — retrieves search results for the Post-process Agent."""

    def __init__(self, api_key: str, cx: str, num_results: int = 5):
        self.api_key = api_key
        self.cx = cx
        self.num_results = num_results

    def search(self, query: str) -> list[dict]:
        """Return up to `num_results` sources: [{title, link, snippet}, ...]."""
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": self.num_results,
        }
        response = requests.get(GOOGLE_SEARCH_ENDPOINT, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])[: self.num_results]
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
            for item in items
        ]
