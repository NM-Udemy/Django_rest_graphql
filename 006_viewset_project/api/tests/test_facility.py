from rest_framework.test import APITestCase
from rest_framework import status

from ..models import Facility
from ..serializers import FacilitySerializer
from django.contrib.auth.models import User
from parameterized import parameterized


class FacilityViewSetTestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.facility1 = Facility.objects.create(
            name='Facility1',
            detail='Detail1'
        )
        cls.facility2 = Facility.objects.create(
            name='Facility2',
            detail='Detail2'
        )
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
    def login(self):
        self.client.login(username='testuser', password='testpassword')
    
    def test_list(self):
        url = '/api/facility/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, FacilitySerializer([self.facility1, self.facility2], many=True).data)
        
    def test_retrieve(self):
        url = f'/api/facility/{self.facility1.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, FacilitySerializer(self.facility1).data)
        
    def test_retrieve_non_existent_facility(self):
        non_existent_facility_pk = 999
        url = f'/api/facility/{non_existent_facility_pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_filter_list(self):
        url = '/api/facility/filter_list/'
        response = self.client.get(url, {'name': 'Facility1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 
                         FacilitySerializer([self.facility1,], many=True).data
                        )
    
    def test_create_without_login(self):
        url = '/api/facility/'
        data = {'name': 'new facility1', 'detail': 'new detail1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Facility.objects.count(), 2)
    
    @parameterized.expand([
        ('new facility1', 'new detail1'),
        ('1' * 100, 'new detail2'),
    ])
    def test_create(self, name, detail):
        url = '/api/facility/'
        data = {'name': name, 'detail': detail}
        self.login()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Facility.objects.count(), 3)
        inserted_facility = Facility.objects.get(pk=response.data['id'])
        self.assertEqual(inserted_facility.name, data['name'])
        self.assertEqual(inserted_facility.detail, data['detail'])
        
    @parameterized.expand([
        ('1' * 101, 'new detail'),
        ('', 'new detail'),
        ('Facility', ''),
    ])
    def test_create_invalid_data(self, name, detail):
        url = '/api/facility/'
        data = {'name': name, 'detail': detail}
        self.login()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Facility.objects.count(), 2)
