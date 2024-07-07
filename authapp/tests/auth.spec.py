from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from authapp.models import User, Organisation

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123"
        }
        self.login_data = {
            "email": "john.doe@example.com",
            "password": "password123"
        }

    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])
        
        user = User.objects.get(email=self.user_data['email'])
        self.assertIsNotNone(user)
        self.assertTrue(Organisation.objects.filter(users=user).exists())
        organisation = Organisation.objects.get(users=user)
        expected_org_name = f"{self.user_data['firstName']}'s Organisation"
        self.assertEqual(organisation.name, expected_org_name)

    def test_login_success(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('user', response.data['data'])

    def test_login_failure_invalid_credentials(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.login_url, {
            "email": self.user_data['email'],
            "password": "wrongpassword"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['statusCode'], 401)
        self.assertEqual(response.data['message'], "Authentication failed")

    def test_register_missing_required_fields(self):
        required_fields = ['firstName', 'lastName', 'email', 'password']
        for field in required_fields:
            invalid_data = self.user_data.copy()
            invalid_data.pop(field)
            response = self.client.post(self.register_url, invalid_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertIn(field, response.data['errors'])

    def test_register_duplicate_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('email', response.data['errors'])
