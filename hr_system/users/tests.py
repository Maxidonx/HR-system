from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User

class UserAuthTests(APITestCase):
    """
    Test suite for user registration and JWT authentication.
    """

    def test_user_registration(self):
        """
        Ensure a new user can be registered successfully.
        """
        url = reverse('user-register')
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword123",
            "password2": "testpassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')
        self.assertIn('message', response.data)

    def test_jwt_login(self):
        """
        Ensure a registered user can log in and receive access/refresh tokens.
        """
        # First, create a user to log in with
        User.objects.create_user(
            username='loginuser', 
            email='loginuser@example.com', 
            password='loginpassword123'
        )
        
        url = reverse('token_obtain_pair')
        data = {
            "email": "loginuser@example.com",
            "password": "loginpassword123"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)