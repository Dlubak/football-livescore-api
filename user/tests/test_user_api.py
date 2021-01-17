from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user.serializers import UserSerializer


class PublicUserApiTests(TestCase):
    """
    Test the USERS API (public)
    """
    def setUp(self):
        self.client = APIClient()

    def test_expect_success_create_valid_user(self):
        """
        Test Create user with valid data is successful
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpassword123',
            'name': "Test User"
        }
        response = self.client.post(reverse('user:create'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_expect_fail_create_two_users_with_same_email(self):
        """
        Test creating user that already exists fail
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpass123',
            'name': 'Test'
        }
        get_user_model().objects.create_user(**payload)
        response = self.client.post(reverse('user:create'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expect_fail_password_to_short(self):
        """
        Test that password must be more than 4 characters
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'tp',
            'name': 'Test'
        }
        response = self.client.post(reverse('user:create'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that user was not created
        user = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user)

    def test_expect_success_retrieve_users_unathorized(self):
        """
        Test that unathorized user can retrieve all users
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpass123',
            'name': 'Test'
        }
        user = get_user_model().objects.create_user(**payload)
        serializer = UserSerializer(user)
        response = self.client.get(reverse('user:list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, response.data)

    def test_expect_success_token_is_created_for_user(self):
        """
        Test that token is created for the user
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpass123',
            'name': 'Test'
        }
        user = get_user_model().objects.create_user(**payload)
        response = self.client.post(reverse('user:token'), payload)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expect_fail_token_invalid_credentials(self):
        """
        Test that authentication token is not created if invalid credentials are given
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpass123',
            'name': 'Test'
        }
        user = get_user_model().objects.create_user(**payload)
        payload['password'] = 'fail'
        response = self.client.post(reverse('user:token'), payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_expect_fail_token_nonexistent_user(self):
        """
        Test that token is not created if user does not exist
        """
        payload = {
            'email': 'test_user@dev.com',
            'password': 'Testpass123',
            'name': 'Test'
        }
        response = self.client.post(reverse('user:token'), payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expect_fail_missing_field(self):
        """
        Test that email and password are required for token to be created
        """
        payload = {
            'email': 'test',
            'password': ''
        }
        response = self.client.post(reverse('user:token'), payload)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """
    Test API request that require authentication
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='testpassword123',
            name='test'
        )
        self.manage_url = reverse('user:manage', kwargs={'pk': self.user.id})
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_expect_success_retrieve_profile(self):
        """
        Test retrieving profile for logged in user
        """
        response = self.client.get(self.manage_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'email': self.user.email,
            'name': self.user.name
        })

    def test_expect_fail_retrieve_other_user_profile(self):
        """
        Test retrieving other user profile fails
        """
        second_user = get_user_model().objects.create_user(
            email='second_user@seconduser.com',
            password='seconduser123',
            name='seconduser'
        )
        response = self.client.get(
            reverse('user:manage', kwargs={'pk': second_user.id}))
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expected_fail_post_method(self):
        """
        Test that post method is not allowed on manage endpoint
        """
        response = self.client.post(self.manage_url, {})
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_expect_success_update_user(self):
        """
        Test that updating the user for authenticated user works
        """
        payload = {
            'name': 'Test Updated',
            'password': 'newpass123'
        }
        response = self.client.patch(self.manage_url, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
