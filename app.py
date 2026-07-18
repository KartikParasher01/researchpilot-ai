from src.search import SearchClient
from src.scraper import Scraper

search_client = SearchClient()
scraper = Scraper()

results = search_client.search("Should I learn Spark or Airflow in 2026?")
articles = []

for result in results["results"]:
    url = result.get("url")

    if url:
        try:
            article = {
                "title": result.get("title"),
                "url": url,
                "text": scraper.scrape(url)}

            articles.append(article)

        except Exception as e:
            print(f"❌ Failed to scrape: {result.get('title')}")
            print(f"URL: {url}")
            print(f"Error: {e}\n")

for article in articles:
    print("=" * 80)
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print()
    print(article["text"][:500])
    print("\n")


