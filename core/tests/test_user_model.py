from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    """
    Test Custom User Model
    """

    def test_create_user_succesful(self):
        """
        Test creating a new user with successs
        """
        email = "test_user@test.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_invalid_email(self):
        """
        Test creating user with invalid email
        """
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                'a@.com',
                'testpassword123'
            )

    def test_check_new_user_email_normalized(self):
        """
        Test that email for new user is normalized
        """
        email = "test@DEV.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_check_user_privileges(self):
        """
        Test that checks that normal user has no superuser privileges
        """
        email = "test_user@test.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_creating_superuser(self):
        """
        Test creating a new super user
        """
        email = "admin@superuser.com"
        password = "adminpassword123"
        superuser = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
