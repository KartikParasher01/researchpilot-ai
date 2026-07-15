# from src.config import TAVILY_API_KEY

# print(TAVILY_API_KEY)

# def main():
#     print("Welcome to ResearchPilot AI")


# if __name__ == "__main__":
#     main()

from src.search import SearchClient

client = SearchClient()

results = client.search("Should I learn Spark or Airflow in 2026?")

print(results)