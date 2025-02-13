"""
Test cases for Transactions API.
"""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Transaction


class TransactionAPITest(APITestCase):
    """
    Test suite for the Transaction API.
    """

    def setUp(self):
        """
        Set up test user and authenticate with JWT.
        """
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Set the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_transaction(self):
        """
        Ensure a user can create a financial transaction.
        """
        data = {
            "user": self.user.id,
            "amount": 100.50,
            "category": "income",
            "description": "Freelance payment",
        }
        response = self.client.post("/api/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_transactions(self):
        """
        Ensure a user can retrieve their transactions.
        """
        response = self.client.get("/api/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self):
        """
        Ensure unauthorized users cannot access the API.
        """
        self.client.credentials()  # Remove authentication
        response = self.client.get("/api/transactions/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
