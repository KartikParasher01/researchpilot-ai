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



class QueryPlanner:
    def __init__(self, llm):
        self.llm = llm

    def classify_query(self, query: str) -> QueryType:

        query = query.lower()

        if any(word in query for word in COMPARISON_KEYWORDS):
            return QueryType.COMPARISON

        if any(word in query for word in RESEARCH_KEYWORDS):
            return QueryType.RESEARCH

        return QueryType.SIMPLE


    def get_max_queries(self, query_type: QueryType) -> int:

        mapping = {
            QueryType.SIMPLE: 2,
            QueryType.COMPARISON: 3,
            QueryType.RESEARCH: 5,
        }

        return mapping[query_type]



    def generate_queries(self, user_query: str):
        query_type = self.classify_query(user_query)
        max_queries = self.get_max_queries(query_type)
        messages = build_query_planner_messages(user_query,max_queries,)

        response = self.llm.generate(messages)

        if response is None:
            return None
        
        try:
            data = json.loads(response)

            result = QueryPlannerResponse.model_validate(data)

            return result.queries

        except json.JSONDecodeError:
            logger.exception("LLM returned invalid JSON")
            return None

        except ValidationError:
            logger.exception("Invalid query planner response")
            return None