import requests
from scraper import Scraper

scraper = Scraper()

a = scraper.fetch_html("https://www.example.com")
print(a[:500])