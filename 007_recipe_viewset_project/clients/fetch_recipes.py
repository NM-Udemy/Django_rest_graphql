import requests

fetch_url = 'http://localhost:8000/recipe/recipe/'

response = requests.get(fetch_url,
                        params={
                            'ordering': '-id',
                            # 'title': 'カレーライス'
                        })
print(response.json())
