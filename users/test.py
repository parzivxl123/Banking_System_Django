from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserTests(APITestCase):

    def test_create_user(self):

        data = {
            "username":"john",
            "email":"john@test.com",
            "password":"John12345",
            "balance":"5000"
        }

        response = self.client.post(
            "/users/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_login(self):

        User.objects.create_user(
            username="john",
            email="john@test.com",
            password="John12345"
        )

        response = self.client.post(
            "/login/",
            {
                "username":"john",
                "password":"John12345"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn(
            "access",
            response.data
        )

    def test_wrong_login(self):

        User.objects.create_user(
            username="john",
            password="John12345"
        )

        response = self.client.post(
            "/login/",
            {
                "username":"john",
                "password":"Wrong123"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )