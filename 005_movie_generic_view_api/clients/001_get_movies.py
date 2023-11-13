import requests
import json

url = 'http://localhost:8000/api/movies'

def fetch_movies(fetch_url):
    response = requests.get(fetch_url)
    return json.loads(response.text)

next_url = url
while True:
    response = fetch_movies(next_url)
    print([movie.get('name') for movie in response.get('results')])
    next_url = response['next']
    if next_url is None:
        break
    
