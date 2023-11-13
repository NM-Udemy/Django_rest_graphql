from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class UserViewSetTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
    
    def test_regist(self):
        url = '/api/user/regist/'
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_regist_failed(self):
        url = '/api/user/regist/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
    
    def test_login(self):
        url = '/api/user/login/'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_failed(self):
        url = '/api/user/login/'
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
