import logging

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


logger = logging.getLogger(__name__)

MAX_CHARS = 10_000
REQUEST_TIMEOUT = 10


class Scraper:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0 Safari/537.36"
                )
            }
        )

    def fetch_html(self, url: str) -> str | None:
        """Fetch an HTML page from a URL."""

        try:
            response = self.session.get(
                url,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            if "text/html" not in content_type:
                logger.info(
                    "Skipping non-HTML content: %s [%s]",
                    url,
                    content_type,
                )
                return None

            return response.text

        except requests.HTTPError as exc:

            if response.status_code == 429:
                logger.warning(
                    "Rate limited while scraping: %s",
                    url,
                )

            raise exc

        except RequestException:
            logger.exception(
                "Request failed while scraping: %s",
                url,
            )
            raise

    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content."""

        return BeautifulSoup(
            html,
            "html.parser",
        )

    def extract_article_text(
        self,
        soup: BeautifulSoup,
    ) -> str:
        """Extract readable text from a webpage."""

        article = soup.find("article")

        if article:
            text = article.get_text(
                separator=" ",
                strip=True,
            )
        else:
            text = soup.get_text(
                separator=" ",
                strip=True,
            )

        return text[:MAX_CHARS]

    def scrape(self, url: str) -> str | None:
        """Fetch, parse, and extract text from a webpage."""

        html = self.fetch_html(url)

        if not html:
            return None

        soup = self.parse_html(html)

        return self.extract_article_text(soup)