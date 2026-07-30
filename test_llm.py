# from src.llm import LLMClient

# llm = LLMClient()

# query = "Should I learn Spark or Airflow in 2026?"

# articles = [
#     {
#         "title": "Spark vs Airflow",
#         "url": "https://example.com/spark-vs-airflow",
#         "content": """
# Apache Spark is a distributed computing framework used for
# large-scale data processing.

# Apache Airflow is a workflow orchestration tool used to
# schedule and monitor data pipelines.
#         """
#     }
# ]

# data = llm.summarize(query, articles)

# if data is not None:
#     print(data["summary"])


import time
import gradio as gr


def test(progress=gr.Progress()):
    progress(0.2, desc="Searching...")
    time.sleep(2)

    progress(0.5, desc="Scraping...")
    time.sleep(2)

    progress(0.8, desc="Thinking...")
    time.sleep(2)

    progress(1.0, desc="Done!")
    return "Finished"


demo = gr.Interface(
    fn=test,
    inputs=[],
    outputs="text",
)

demo.launch()