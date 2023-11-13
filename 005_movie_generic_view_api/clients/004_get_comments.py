import requests
import json

def get_comments(movie_id):
    url = f'http://localhost:8000/api/movies/{movie_id}/comments'
    response = requests.get(url)
    return json.loads(response.text)

print(get_comments(2))
