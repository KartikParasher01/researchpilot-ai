from src.llm import LLMClient

llm = LLMClient()

query = "Should I learn Spark or Airflow in 2026?"

articles = [
    {
        "title": "Spark vs Airflow",
        "content": """
Apache Spark is a distributed computing framework used for
large-scale data processing.

Apache Airflow is a workflow orchestration tool used to
schedule and monitor data pipelines.
        """
    }
]

summary = llm.summarize(query, articles)

print(summary)