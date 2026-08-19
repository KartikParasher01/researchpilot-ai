import json
import logging

from pydantic import ValidationError

from src.query_planner import QueryPlanner
from src.search import SearchClient
from src.scraper import Scraper
from src.llm import LLMClient
from src.prompts import build_research_messages
from src.models import ResearchResponse


logger = logging.getLogger(__name__)

MAX_ARTICLES = 3


search_client = SearchClient()
scraper = Scraper()
llm = LLMClient()
planner = QueryPlanner(llm)


def research(query: str, progress=None):
    """
    Run the complete ResearchPilot pipeline:

    1. Generate search queries
    2. Search the web
    3. Deduplicate search results
    4. Scrape usable sources
    5. Generate a research report
    6. Validate the LLM response
    """

    # ---------------------------------------------------------
    # Step 1: Generate search queries
    # ---------------------------------------------------------

    if progress:
        progress(0.2, desc="🔍 Searching the web...")

    try:
        queries = planner.generate_queries(query)
    except Exception:
        logger.exception("Query planning failed")
        return {
            "success": False,
            "message": "Failed to generate search queries.",
            "data": None,
        }

    if not queries:
        return {
            "success": False,
            "message": "No search queries were generated.",
            "data": None,
        }

    # ---------------------------------------------------------
    # Step 2: Search the web
    # ---------------------------------------------------------

    results = []

    for search_query in queries:
        try:
            search_results = search_client.search(search_query)

            if search_results:
                results.extend(search_results)

        except Exception:
            logger.exception(
                "Search failed for query: %s",
                search_query,
            )

    if not results:
        return {
            "success": False,
            "message": "No search results were found.",
            "data": None,
        }

    # ---------------------------------------------------------
    # Step 3: Remove duplicate URLs
    # ---------------------------------------------------------

    seen_urls = set()
    unique_results = []

    for result in results:
        url = result.get("url")

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(result)

    logger.info(
        "Total search results: %d | Unique results: %d",
        len(results),
        len(unique_results),
    )

    # ---------------------------------------------------------
    # Step 4: Scrape articles
    # ---------------------------------------------------------

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

            articles.append(
                {
                    "title": result.get("title"),
                    "url": url,
                    "content": content,
                }
            )

        except Exception:
            logger.exception("Failed to scrape: %s", url)

    # Limit the amount of content sent to the LLM.
    articles = articles[:MAX_ARTICLES]

    logger.info(
        "Articles successfully scraped: %d",
        len(articles),
    )

    if not articles:
        return {
            "success": False,
            "message": "Couldn't retrieve any usable articles.",
            "data": None,
        }

    # ---------------------------------------------------------
    # Step 5: Generate research report
    # ---------------------------------------------------------

    if progress:
        progress(0.8,desc="🧠 AI is analyzing the articles...",)

    messages = build_research_messages(query,articles,)

    try:
        raw_result = llm.generate(messages)
    except Exception:
        logger.exception("LLM request failed")
        return {"success": False,"message": "Failed to generate research report.","data": None,}

    if not raw_result:
        return {"success": False,"message": "Failed to generate research report.","data": None,}

    # ---------------------------------------------------------
    # Step 6: Validate LLM response
    # ---------------------------------------------------------

    try:
        data = json.loads(raw_result)

        parsed_result = (ResearchResponse.model_validate(data).model_dump())

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

        return {"success": False,"message": "Invalid response schema.","data": None,}

    # ---------------------------------------------------------
    # Step 7: Finished
    # ---------------------------------------------------------

    if progress:
        progress(1.0,desc="✅ Report generated!",)

    return {
        "success": True,
        "message": "Success",
        "data": parsed_result,
    }