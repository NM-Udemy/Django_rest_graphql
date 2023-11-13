import requests
import json

url = 'http://localhost:8000/api/movies'

def fetch_movies(fetch_url, staff_name):
    response = requests.get(fetch_url,
                            params={'roles__staffs__name': staff_name,})
    return json.loads(response.text)

next_url = url
staff_name = input("スタッフの名前を入力してください")
while True:
    response = fetch_movies(next_url, staff_name)
    print([(movie.get('name'), movie.get('average_star')) for movie in response.get('results')])
    
    next_url = response['next']
    if next_url is None:
        break
    
