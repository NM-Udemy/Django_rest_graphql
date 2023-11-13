from login_user import login_user
import requests
token = login_user('test_user@mail.com', '12345678')

put_url = 'http://localhost:8000/recipe/recipe/5/'

response = requests.put(put_url, data={
    'title': 'ビーフシチュー',
    'instruction': '作り方の説明',
},
              headers={
                  'Authorization': f'Token {token}'
              })


print(response.status_code)
print(response.json())