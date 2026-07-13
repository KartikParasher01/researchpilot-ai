import requests
from http_client import get_json

url = "https://jsonplaceholder.typicode.com/posts/9"

response = requests.get(url)

print("Status Code:", response.status_code)
print(response.json())

title = get_json(url)

print("Title:", title)