from src.llm import LLMClient
from src.query_planner import QueryPlanner

llm = LLMClient()
planner = QueryPlanner(llm)

queries = planner.generate_queries(
    "Explain the MSME cluster difference between Gujarat and Maharashtra from all perspectives"
)

print("\nGenerated Queries:\n")

if queries:
    for i, query in enumerate(queries, start=1):
        print(f"{i}. {query}")
else:
    print("No queries generated.")