import requests

url = 'http://localhost:8000/api/country_datetime/'

# response = requests.get(url, params={"timezone": "US/Eastern"})

response = requests.post(url, data={"timezone": "US/Easter"})

print(response.status_code)
print(response.text)
print(response.headers)
if response.status_code == 400:
    print('実行失敗')