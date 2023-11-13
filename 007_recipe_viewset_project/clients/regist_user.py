import requests
import json

regist_url = 'http://localhost:8000/user/regist/'

response = requests.post(regist_url, data={
    'username': 'test_user',
    'email': 'test_user@mail.com',
    'age': 30,
    'password': '12345678',
    'confirm_password': '12345678',
})

print(response.status_code)
print(response)
