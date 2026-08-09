from pyexpat.errors import messages

from src.query_planner import QueryPlanner
from src.search import SearchClient
from src.scraper import Scraper
from src.llm import LLMClient
from src.prompts import build_research_messages
from src.models import ResearchResponse
from pydantic import ValidationError
import logging
import json

search_client = SearchClient()
scraper = Scraper()
llm = LLMClient()
planner = QueryPlanner(llm)

logger = logging.getLogger(__name__)


def research(query: str, progress=None):
    # Step 1: Search the web
    if progress:
        progress(0.2, desc="🔍 Searching the web...")

    queries = planner.generate_queries(query)
    if queries is None:
        return {
            "success": False,
            "message": "Failed to generate search queries.",
            "data": None,
        }
    results = []

    for search_query in queries:

        search_results = search_client.search(search_query)

        results.extend(search_results)

    seen_urls = set()
    unique_results = []

    for result in results:
        url = result.get("url")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(result)

    print(f"Total search results: {len(results)}")
    print(f"Unique search results: {len(unique_results)}")

    print(f"Results selected for scraping: {len(unique_results)}")

    # Step 2: Scrape articles
    if progress:
        progress(0.5, desc="📄 Scraping articles...")

    articles = []

    for result in unique_results:
        url = result.get("url")
        if not url:
            continue

        try:
            content = scraper.scrape(url)

            if not content:
                continue

            article = {
                "title": result.get("title"),
                "url": url,
                "content": content,
            }

            articles.append(article)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    articles = articles[:5]
    print(f"Articles successfully scraped: {len(articles)}")

    if not articles:
        return {
            "success": False,
            "message": "Couldn't retrieve enough articles.",
            "data": None,
        }

    # Step 3: Generate AI summary
    if progress:
        progress(0.8, desc="🧠 AI is analyzing the articles...")

    for i, article in enumerate(articles, 1):
        print(f"Article {i}: {article['title']}")
        print(f"Characters: {len(article['content'])}")
        print(f"First 100 chars: {repr(article['content'][:100])}")
        print("-" * 80)


    messages = build_research_messages(query, articles[:2])
    raw_result = llm.generate(messages)

    if raw_result is None:
        return {
            "success": False,
            "message": "Failed to generate research report.",
            "data": None,
        }

    try:

        data = json.loads(raw_result)
        parsed_result = ResearchResponse.model_validate(data).model_dump()
        parsed_result["sources"] = articles

    except json.JSONDecodeError:
        logger.exception("LLM returned invalid JSON")
        return {
            "success": False,
            "message": "LLM returned invalid JSON.",
            "data": None,
        }

    except ValidationError:
        logger.exception("LLM response failed validation")
        return {
            "success": False,
            "message": "Invalid response schema.",
            "data": None,
        }

    # Step 4: Finished
    if progress:
        progress(1.0, desc="✅ Report generated!")

    return {
        "success": True,
        "message": "Success",
        "data": parsed_result,
    }
