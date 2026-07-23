from src.search import SearchClient
from src.scraper import Scraper
from src.llm import LLMClient

search_client = SearchClient()
scraper = Scraper()
llm = LLMClient()


def research(query: str):
    results = search_client.search(query)
    articles = []

    for result in results:
        url = result.get("url")

        if not url:
            continue

        try:
            article = {
                "title": result.get("title"),
                "url": url,
                "content": scraper.scrape(url),
            }

            articles.append(article)

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    if not articles:
        return None

    return llm.summarize(query, articles)