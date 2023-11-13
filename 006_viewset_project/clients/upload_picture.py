import requests
import json

login_url = 'http://localhost:8000/api/user/login/'

response = requests.post(login_url,
                         data={
                             'username': 'test',
                             'password': '12345678'
                         })

post_url = 'http://localhost:8000/api/user/upload_picture/'
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from os.path import join

file =open(join(BASE_DIR, 'cat.jpg'), 'rb')

requests.post(post_url,
              files={
                  'file': file
              })

# requests.put(post_url + '1/',
#               data={
#                   'title': 'test1',
#                   'instruction': 'test',
#               },
#               headers={
#                 "Authorization": "Token " + token
#             }
#         )


# requests.delete(post_url + '1/',
              
#               headers={
#                 "Authorization": "Token " + token
#             }
#         )
