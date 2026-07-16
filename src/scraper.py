import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        pass

    def fetch_html(self, url):
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    
    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def extract_article_text(self, soup):
        text = soup.get_text()
        all_text = ' '.join(text.split())
        return all_text
    
    def scrape(self, url):
        html = self.fetch_html(url)
        soup = self.parse_html(html)
        text = self.extract_article_text(soup)
        return text