from enum import Enum


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

    def classify_query(self, query: str) -> QueryType:

        query = query.lower()

        if any(word in query for word in COMPARISON_KEYWORDS):
            return QueryType.COMPARISON

        if any(word in query for word in RESEARCH_KEYWORDS):
            return QueryType.RESEARCH

        return QueryType.SIMPLE


    def get_max_queries(self, query_type: QueryType):

        mapping = {
            QueryType.SIMPLE: 2,
            QueryType.COMPARISON: 3,
            QueryType.RESEARCH: 5,
        }

        return mapping[query_type]