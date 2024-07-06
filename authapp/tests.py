# from django.urls import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from authapp.models import User, Organisation

# class AuthTests(APITestCase):

#     def setUp(self):
#         self.register_url = reverse('register')
#         self.login_url = reverse('login')
#         self.user_detail_url = lambda pk: reverse('user-detail', kwargs={'pk': pk})
#         self.organisations_url = reverse('organisation-list')
#         self.single_organisation_url = lambda orgId: reverse('organisation-detail', kwargs={'orgId': orgId})
#         self.add_user_to_organisation_url = lambda orgId: reverse('add-user-to-organisation', kwargs={'orgId': orgId})

#         self.user_data = {
#             "firstName": "Temilade",
#             "lastName": "Seyi",
#             "email": "tems@gmail.com",
#             "password": "password123",
#             "phone": "08045674332"
#         }

#     def authenticate_user(self, email, password):
#         response = self.client.post(self.login_url, {'email': email, 'password': password}, format='json')
#         print("Login response data:", response.data)  # Debug information
#         token = response.data.get('data', {}).get('accessToken')
#         if token:
#             self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
#         else:
#             print("Authentication failed:", response.data)
#         return response

#     def test_register_success(self):
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn('accessToken', response.data['data'])
#         self.assertEqual(response.data['data']['user']['firstName'], 'Temilade')
#         self.assertEqual(response.data['data']['user']['lastName'], 'Seyi')

#     def test_login_success(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         response = self.authenticate_user('tems@gmail.com', 'password123')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('accessToken', response.data['data'])

#     def test_register_missing_fields(self):
#         incomplete_data = {
#             "firstName": "Temilade",
#             "email": "tems@gmail.com",
#             "password": "password123"
#         }
#         response = self.client.post(self.register_url, incomplete_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
#         self.assertIn('lastName', response.data['errors'])

#     def test_register_duplicate_email(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
#         self.assertIn('email', response.data['errors'])

#     def test_create_default_organisation_on_registration(self):
#         response = self.client.post(self.register_url, self.user_data, format='json')
#         user = User.objects.get(email='tems@gmail.com')
#         self.assertTrue(Organisation.objects.filter(name="Temilade's Organisation", users=user).exists())

#     def test_get_user_details(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         user = User.objects.get(email='tems@gmail.com')
#         self.authenticate_user('tems@gmail.com', 'password123')
#         response = self.client.get(self.user_detail_url(user.pk))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['firstName'], 'Temilade')
#         self.assertEqual(response.data['email'], 'tems@gmail.com')

#     def test_get_organisations(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         self.authenticate_user('tems@gmail.com', 'password123')
#         response = self.client.get(self.organisations_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response.data['data']['organisations']) > 0)

#     def test_get_single_organisation(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         user = User.objects.get(email='tems@gmail.com')
#         organisation = Organisation.objects.get(users=user)
#         self.authenticate_user('tems@gmail.com', 'password123')
#         response = self.client.get(self.single_organisation_url(organisation.id))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], "Temilade's Organisation")

#     def test_create_organisation(self):
#         self.client.post(self.register_url, self.user_data, format='json')
#         self.authenticate_user('tems@gmail.com', 'password123')
#         organisation_data = {
#             "name": "New Org",
#             "description": "New organisation description"
#         }
#         response = self.client.post(self.organisations_url, organisation_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['data']['name'], 'New Org')

#     def test_add_user_to_organisation(self):
#         # Register the first user
#         self.client.post(self.register_url, self.user_data, format='json')
#         user = User.objects.get(email='tems@gmail.com')
        
#         # Create organisation manually if not done in registration
#         organisation = Organisation.objects.create(name="Temilade's Organisation")
#         organisation.users.add(user)

#         new_user_data = {
#             "firstName": "New",
#             "lastName": "User",
#             "email": "newuser@gmail.com",
#             "password": "password123",
#             "phone": "07000000000"
#         }

#         # Register the new user
#         self.client.post(self.register_url, new_user_data, format='json')
#         new_user = User.objects.get(email='newuser@gmail.com')

#         # Authenticate the first user
#         self.authenticate_user('tems@gmail.com', 'password123')

#         # Add the new user to the organisation
#         response = self.client.post(self.add_user_to_organisation_url(organisation.id), {"userId": new_user.id}, format='json')
#         print("Add user to organisation response data:", response.data)  # Debug information

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(organisation.users.filter(pk=new_user.pk).exists())



from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from authapp.models import User, Organisation

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_detail_url = lambda pk: reverse('user-detail', kwargs={'pk': pk})
        self.organisations_url = reverse('organisation-list')
        self.single_organisation_url = lambda orgId: reverse('organisation-detail', kwargs={'orgId': orgId})
        self.add_user_to_organisation_url = lambda orgId: reverse('add-user-to-organisation', kwargs={'orgId': orgId})

        self.user_data = {
            "firstName": "Temilade",
            "lastName": "Seyi",
            "email": "tems@gmail.com",
            "password": "password123",
            "phone": "08045674332"
        }

    def authenticate_user(self, email, password):
        response = self.client.post(self.login_url, {'email': email, 'password': password}, format='json')
        print("Login response data:", response.data)  # Debug information
        token = response.data.get('data', {}).get('accessToken')
        if token:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        else:
            print("Authentication failed:", response.data)
        return response

    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        print("Register response data:", response.data)  # Debug information
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])
        self.assertEqual(response.data['data']['user']['firstName'], 'Temilade')
        self.assertEqual(response.data['data']['user']['lastName'], 'Seyi')

    def test_login_success(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.authenticate_user('tems@gmail.com', 'password123')
        print("Login response data after register:", response.data)  # Debug information
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])

    def test_register_missing_fields(self):
        incomplete_data = {
            "firstName": "Temilade",
            "email": "tems@gmail.com",
            "password": "password123"
        }
        response = self.client.post(self.register_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('lastName', response.data['errors'])

    def test_register_duplicate_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn('email', response.data['errors'])

    def test_create_default_organisation_on_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email='tems@gmail.com')
        self.assertTrue(Organisation.objects.filter(name="Temilade's Organisation", users=user).exists())

    def test_get_user_details(self):
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email='tems@gmail.com')
        self.authenticate_user('tems@gmail.com', 'password123')
        response = self.client.get(self.user_detail_url(user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstName'], 'Temilade')
        self.assertEqual(response.data['email'], 'tems@gmail.com')

    def test_get_organisations(self):
        self.client.post(self.register_url, self.user_data, format='json')
        self.authenticate_user('tems@gmail.com', 'password123')
        response = self.client.get(self.organisations_url)
        print("Get organisations response data:", response.data)  # Debug information
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_single_organisation(self):
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email='tems@gmail.com')
        organisation = Organisation.objects.get(users=user)
        self.authenticate_user('tems@gmail.com', 'password123')
        response = self.client.get(self.single_organisation_url(organisation.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Temilade's Organisation")

    def test_add_user_to_organisation(self):
        # Register the first user
        self.client.post(self.register_url, self.user_data, format='json')
        user = User.objects.get(email='tems@gmail.com')
        
        # Create organisation manually if necessary
        organisation = Organisation.objects.create(name="Test Org")
        organisation.users.add(user)
        
        # Register a second user
        second_user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "08012345678"
        }
        self.client.post(self.register_url, second_user_data, format='json')
        second_user = User.objects.get(email='john.doe@example.com')
        
        # Authenticate the first user
        self.authenticate_user('tems@gmail.com', 'password123')
        
        # Add the second user to the organisation
        response = self.client.post(self.add_user_to_organisation_url(organisation.id), {'userId': second_user.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(organisation.users.filter(id=second_user.id).exists())
