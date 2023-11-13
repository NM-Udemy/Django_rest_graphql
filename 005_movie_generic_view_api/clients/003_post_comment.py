import requests
import json

login_url = 'http://localhost:8000/api_token_auth'

response = requests.post(login_url,
                         data={
                             'username': 'test',
                             'password': '12345678'
                         })
token = response.json().get('token')
url = 'http://localhost:8000/api/movies/2/comments'
response = requests.post(url, data={
    'comment': 'よかったです。clientから',
    'star': 4,
},headers = {"Authorization": f"Token {token}"})
print(response.text)
