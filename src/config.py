from dotenv import load_dotenv
import os


load_dotenv()

APP_NAME = os.getenv("APP_NAME")
DEBUG = os.getenv("DEBUG")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")