from login_user import login_user
import requests
token = login_user('test_user@mail.com', '12345678')

post_url = 'http://localhost:8000/recipe/ingredient/'

response = requests.post(post_url, data={
    'name': 'クリーム',
    'quantity': '100g',
    'recipe': 6
},
              headers={
                  'Authorization': f'Token {token}'
              })

print(response.status_code)
print(response.json())