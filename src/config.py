import os

from dotenv import load_dotenv


load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")

TEMPERATURE = float(
    os.getenv("LLM_TEMPERATURE", "0.3")
)

MAX_TOKENS = int(
    os.getenv("LLM_MAX_TOKENS", "1000")
)