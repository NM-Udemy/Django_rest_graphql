import requests


url = "http://localhost:8000/api_token_auth/"

response = requests.post(url, data= {
    "username": 'test3', "password": "12345678"
})
print(response.text)
# {"token":"b0958c6ceb94319213e165e536b50dee910a0279"}

url = "http://localhost:8000/api/v2/product/"

token = response.json().get("token")
print(token)
response = requests.post(url, data= {
    "name": "Product 1", "price": "10000", "user": 3
}, headers={"Authorization": f"Token {token}"})
print(response.text)