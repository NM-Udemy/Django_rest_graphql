import requests


url = "http://localhost:8000/api/item/"

response = requests.get(url)
print(response.text)
print(type(response.text))
data = response.json()
print(data)
for d in data:
    print(d.get('name'))