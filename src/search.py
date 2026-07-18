from src.config import TAVILY_API_KEY
import requests


class SearchClient:

    def __init__(self):
        self.api_key = TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
        self.timeout = 10

    def search(self, query):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"}
        payload = {"query": query}

        response = requests.post(url=self.base_url,headers=headers,json=payload,timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return self.extract_results(data)
            

    def extract_results(self, response):
            extracted_data = []
            for result in response.get("results", []):
                article = {"url": result.get("url", ""), "title": result.get("title", ""), "content": result.get("content", "")}
                extracted_data.append(article)
            
            return extracted_data


def extract_result(self,response):
     a = []
     for i in response.get('title'):
          article = {"url": i.get("url", ""), "title": i.get("title", ""), "content": i.get("content", "")}
          a.append(article)
     return a
           