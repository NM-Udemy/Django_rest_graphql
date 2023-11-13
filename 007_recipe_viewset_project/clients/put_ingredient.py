from login_user import login_user
import requests
token = login_user('test_user@mail.com', '12345678')

put_url = 'http://localhost:8000/recipe/ingredient/6/'

response = requests.put(put_url, data={
    'name': 'クリーム',
    'quantity': '200g',
    'recipe': 6
},
              headers={
                  'Authorization': f'Token {token}'
              })

print(response.status_code)
print(response.json())