import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        })
        


    def fetch_html(self, url):
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text

        except HTTPError as e:
            if response.status_code == 429:
                print(f"⚠️ Rate limited: {url}")
            raise
    
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def extract_article_text(self, soup):
        article = soup.find("article")

        if article:
            text = article.get_text(separator=" ", strip=True)
        else:
            text = soup.get_text(separator=" ", strip=True)

        MAX_CHARS = 10000

        return text[:MAX_CHARS]

    
    def scrape(self, url):
        html = self.fetch_html(url)
        soup = self.parse_html(html)
        text = self.extract_article_text(soup)
        return text



        