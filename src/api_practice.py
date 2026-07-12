import requests

url = "https://jsonplaceholder.typicode.com/posts/9"

response = requests.get(url)

print("Status Code:", response.status_code)
print(response.json())

title = response.json().get("title")

print("Title:", title)