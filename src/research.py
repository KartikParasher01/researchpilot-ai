from src.search import SearchClient
from src.scraper import Scraper
from src.llm import LLMClient

search_client = SearchClient()
scraper = Scraper()
llm = LLMClient()


def research(query: str, progress=None):

    # Step 1: Search the web
    if progress:
        print("🔍 Searching...")
        progress(0.2, desc="🔍 Searching the web...")

    results = search_client.search(query)

    # Step 2: Scrape articles
    if progress:
        print("📄 Scraping articles...")
        progress(0.5, desc="📄 Scraping articles...")

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

    # No articles found
    if not articles:
        return {
            "success": False,
            "message": "Couldn't retrieve enough articles.",
            "data": None,
        }

    # Step 3: Generate AI summary
    if progress:
        print("🧠 AI is analyzing...")
        progress(0.8, desc="🧠 AI is analyzing the articles...")

    result = llm.summarize(query, articles)

    if result is None:
        return {
            "success": False,
            "message": "Failed to generate research report.",
            "data": None,
        }

    # Step 4: Finished
    if progress:
        print("✅ Done!")
        progress(1.0, desc="✅ Report generated!")

    return {
        "success": True,
        "message": "Success",
        "data": result,
    }