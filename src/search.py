import logging

import requests

from src.config import TAVILY_API_KEY


logger = logging.getLogger(__name__)

SEARCH_URL = "https://api.tavily.com/search"
REQUEST_TIMEOUT = 10


class SearchClient:

    def __init__(self):
        self.api_key = TAVILY_API_KEY
        self.base_url = SEARCH_URL
        self.timeout = REQUEST_TIMEOUT

    def search(self, query: str) -> list[dict]:
        """Search Tavily and return normalized search results."""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "query": query,
        }

        logger.info("Searching Tavily for: %s", query)

        response = requests.post(
            url=self.base_url,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return self.extract_results(data)

    def extract_results(self, response: dict) -> list[dict]:
        """Extract the fields ResearchPilot needs from search results."""

        extracted_data = []

        for result in response.get("results", []):
            article = {
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "content": result.get("content", ""),
            }

            extracted_data.append(article)

        return extracted_data