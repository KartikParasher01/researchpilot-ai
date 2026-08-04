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
        print("🔍 Searching...")
        progress(0.2, desc="🔍 Searching the web...")

    queries = planner.generate_queries(query)
    results = []

    for search_query in queries:
        print(f"Searching: {search_query}")

        search_results = search_client.search(search_query)

        results.extend(search_results)

    if queries is None:
        return {
            "success": False,
            "message": "Failed to generate search queries.",
            "data": None,
        }

    # Step 2: Scrape articles
    if progress:
        print("📄 Scraping articles...")
        progress(0.5, desc="📄 Scraping articles...")

    articles = []

    for result in results:
        url = result.get("url")
        if not url:
            continue

        if url.lower().endswith(".pdf"):
            print(f"Skipping PDF: {url}")
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
        return {
            "success": False,
            "message": "Couldn't retrieve enough articles.",
            "data": None,
        }

    # Step 3: Generate AI summary
    if progress:
        print("🧠 AI is analyzing...")
        progress(0.8, desc="🧠 AI is analyzing the articles...")

    print(f"\nTotal Articles: {len(articles)}")

    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   URL: {article['url']}")
        print(f"   Characters: {len(article['content'])}")
        print("-" * 80)
    
    print(len(articles))
    # messages = build_research_messages(query, articles)
    messages = build_research_messages(query, articles[:2])
    raw_result = llm.generate(messages)

    if raw_result is None:
        return {
            "success": False,
            "message": "Failed to generate research report.",
            "data": None,
        }

    try:
        print("=" * 100)
        print("RAW LLM RESPONSE")
        print("=" * 100)
        print(raw_result)
        print("=" * 100)
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
        print("✅ Done!")
        progress(1.0, desc="✅ Report generated!")

    return {
        "success": True,
        "message": "Success",
        "data": parsed_result,
    }