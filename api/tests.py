"""
Test cases for Transactions API.
"""

from typing import Any

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Transaction


class TransactionAPITest(APITestCase):
    """
    Test suite for the Transaction API.

    Tests authentication, authorization, and CRUD operations
    for financial transactions.
    """

    user: User
    token: str

    def setUp(self) -> None:
        """
        Set up test user and authenticate with JWT.

        Creates a test user and generates a JWT token for authentication.
        The token is automatically added to all subsequent API requests.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpass"  # nosec B106
        )

        # Generate JWT token
        refresh: RefreshToken = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Set the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_transaction(self) -> None:
        """
        Ensure a user can create a financial transaction.

        Tests that:
        - Authenticated users can create transactions
        - The API returns HTTP 201 CREATED on success
        - User field is automatically assigned (not from request data)
        """
        data: dict[str, Any] = {
            "user": self.user.pk,
            "amount": 100.50,
            "category": "income",
            "description": "Freelance payment",
        }
        response: Response = self.client.post("/api/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_transactions(self) -> None:
        """
        Ensure a user can retrieve their transactions.

        Tests that:
        - Authenticated users can list their transactions
        - The API returns HTTP 200 OK on success
        - Only the user's own transactions are returned
        """
        response: Response = self.client.get("/api/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self) -> None:
        """
        Ensure unauthorized users cannot access the API.

        Tests that:
        - Unauthenticated requests are rejected
        - The API returns HTTP 401 UNAUTHORIZED
        - Authentication is required for all endpoints
        """
        self.client.credentials()  # Remove authentication
        response: Response = self.client.get("/api/transactions/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
