from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="john",
            email="john@test.com"
        )

        self.user.set_password(
            "John12345"
        )

        self.user.save()

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

    def test_forgot_password_success(
            self
    ):
        response = self.client.post(

            "/users/forgot-password/",

            {
                "email":
                    self.user.email
            },
            format="json"
        )
        self.assertEqual(
            response.status_code,
            200
        )
        self.user.refresh_from_db()
        self.assertIsNotNone(
            self.user.reset_token
        )

    def test_forgot_password_invalid_user(
            self
    ):
        response = self.client.post(

            "/users/forgot-password/",

            {
                "email":
                    "fake@test.com"
            },

            format="json"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_reset_password_success(
            self
    ):
        self.user.reset_token = (
            "abc123"
        )

        self.user.save()

        response = self.client.post(

            "/users/reset-password/",

            {
                "token": "abc123",

                "newpassword":
                    "NewPassword123"
            },

            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.user.refresh_from_db()

        self.assertIsNone(
            self.user.reset_token
        )

    def test_reset_password_invalid_token(
            self
    ):
        response = self.client.post(

            "/users/reset-password/",

            {
                "token": "wrongtoken",

                "newpassword":
                    "Password123"
            },

            format="json"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_login_after_password_reset(
            self
    ):
        self.user.reset_token = (
            "abc123"
        )

        self.user.save()

        self.client.post(

            "/users/reset-password/",

            {
                "token": "abc123",

                "newpassword":
                    "NewPassword123"
            },

            format="json"
        )

        response = self.client.post(

            "/login/",

            {
                "username":
                    self.user.username,

                "password":
                    "NewPassword123"
            },

            format="json"
        )

        self.assertEqual(
            response.status_code,
            200
        )