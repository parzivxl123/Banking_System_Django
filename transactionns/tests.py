from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from transactionns.models import Transaction
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.


class TransactionTests(APITestCase):

    def setUp(self):

        self.sender = User.objects.create_user(
            username="john",
            email="john@test.com",
            password="John12345",
            balance=5000
        )

        self.receiver = User.objects.create_user(
            username="emma",
            email="emma@test.com",
            password="Emma12345",
            balance=3000
        )

        refresh = RefreshToken.for_user(
            self.sender
        )

        self.token = str(
            refresh.access_token
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Bearer {self.token}"
        )



    def test_transaction_success(self):

        response = self.client.post(
            "/transactions/",
            {
                "receiver":self.receiver.id,
                "amount":"1000"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.sender.refresh_from_db()
        self.receiver.refresh_from_db()

        self.assertEqual(
            self.sender.balance,
            4000
        )

        self.assertEqual(
            self.receiver.balance,
            4000
        )



    def test_insufficient_balance(self):

        response = self.client.post(
            "/transactions/",
            {
                "receiver":self.receiver.id,
                "amount":"10000"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )



    def test_same_sender_receiver(self):

        response = self.client.post(
            "/transactions/",
            {
                "receiver":self.sender.id,
                "amount":"500"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_unauthorized_user(self):
        self.client.credentials()
        response = self.client.post(
            "/transactions/",
            {
                "receiver":self.receiver.id,
                "amount":"100"
            },
            format="json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )



