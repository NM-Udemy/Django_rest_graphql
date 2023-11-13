import requests
import json

def login_user(email, password) -> str:   
    regist_url = 'http://localhost:8000/user/login/'
    response = requests.post(regist_url, data={
        'email': email,
        'password': password,
    })

    return response.json().get('token')
