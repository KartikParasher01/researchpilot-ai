from dotenv import load_dotenv
import os


load_dotenv()

APP_NAME = os.getenv("APP_NAME")
DEBUG = os.getenv("DEBUG")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# gemini Api
LLM_PROVIDER = os.getenv("LLM_PROVIDER")
LLM_API_KEY= os.getenv("LLM_API_KEY")
LLM_MODEL= os.getenv("LLM_MODEL")
TEMPERATURE= float(os.getenv("OPENAI_TEMPERATURE", 0.3))
MAX_TOKENS= int(os.getenv("OPENAI_MAX_TOKENS", 1000))