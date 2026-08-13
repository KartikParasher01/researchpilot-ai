import json
import logging
from enum import Enum

from pydantic import ValidationError

from src.models import QueryPlannerResponse
from src.prompts import build_query_planner_messages


logger = logging.getLogger(__name__)


COMPARISON_KEYWORDS = [
    "vs",
    "versus",
    "compare",
    "difference",
    "better",
]

RESEARCH_KEYWORDS = [
    "research",
    "detailed",
    "complete",
    "analysis",
    "all perspective",
    "everything",
]


class QueryType(str, Enum):
    SIMPLE = "simple"
    COMPARISON = "comparison"
    RESEARCH = "research"


MAX_QUERIES = {
    QueryType.SIMPLE: 2,
    QueryType.COMPARISON: 3,
    QueryType.RESEARCH: 5,
}


class QueryPlanner:

    def __init__(self, llm):
        self.llm = llm

    def classify_query(self, query: str) -> QueryType:
        """Classify the user's query based on its intent."""

        query = query.lower().strip()

        if any(keyword in query for keyword in COMPARISON_KEYWORDS):
            return QueryType.COMPARISON

        if any(keyword in query for keyword in RESEARCH_KEYWORDS):
            return QueryType.RESEARCH

        return QueryType.SIMPLE

    def get_max_queries(self, query_type: QueryType) -> int:
        """Return the maximum number of search queries for a query type."""

        return MAX_QUERIES[query_type]

    def generate_queries(self, user_query: str) -> list[str] | None:
        """Generate search queries using the LLM."""

        if not user_query or not user_query.strip():
            logger.warning("Empty user query received")
            return None

        query_type = self.classify_query(user_query)
        max_queries = self.get_max_queries(query_type)

        messages = build_query_planner_messages(
            user_query,
            max_queries,
        )

        response = self.llm.generate(messages)

        if not response:
            logger.error("Query planner LLM returned no response")
            return None

        try:
            data = json.loads(response)

            result = QueryPlannerResponse.model_validate(data)

            return result.queries

        except json.JSONDecodeError:
            logger.exception(
                "Query planner LLM returned invalid JSON"
            )
            return None

        except ValidationError:
            logger.exception(
                "Query planner response failed validation"
            )
            return None