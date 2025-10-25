"""
Integration tests for full transaction lifecycle.

Tests complete workflows from creation to deletion, JWT authentication flow,
and multi-user scenarios.
"""

from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Transaction
from tests.factories import TransactionFactory, UserFactory


@pytest.mark.django_db
class TestTransactionLifecycle:
    """Test suite for complete transaction lifecycle scenarios."""

    def test_full_transaction_crud_lifecycle(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test complete CRUD lifecycle: create, read, update, delete."""
        # 1. Create transaction
        create_data: dict[str, Any] = {
            "amount": "100.00",
            "category": "income",
            "description": "Initial transaction",
        }
        create_response = authenticated_client.post("/api/transactions/", create_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        transaction_id = create_response.data["id"]  # type: ignore[index]

        # 2. Retrieve transaction
        retrieve_response = authenticated_client.get(
            f"/api/transactions/{transaction_id}/"
        )
        assert retrieve_response.status_code == status.HTTP_200_OK
        assert Decimal(retrieve_response.data["amount"]) == Decimal("100.00")  # type: ignore[index]
        assert retrieve_response.data["description"] == "Initial transaction"  # type: ignore[index]

        # 3. Update transaction
        update_data: dict[str, Any] = {
            "amount": "150.00",
            "category": "expense",
            "description": "Updated transaction",
        }
        update_response = authenticated_client.put(
            f"/api/transactions/{transaction_id}/", update_data
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert Decimal(update_response.data["amount"]) == Decimal("150.00")  # type: ignore[index]
        assert update_response.data["category"] == "expense"  # type: ignore[index]

        # 4. Verify update in list
        list_response = authenticated_client.get("/api/transactions/")
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) == 1  # type: ignore[arg-type]
        assert Decimal(list_response.data[0]["amount"]) == Decimal("150.00")  # type: ignore[index]

        # 5. Delete transaction
        delete_response = authenticated_client.delete(
            f"/api/transactions/{transaction_id}/"
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # 6. Verify deletion
        list_after_delete = authenticated_client.get("/api/transactions/")
        assert len(list_after_delete.data) == 0  # type: ignore[arg-type]

    def test_jwt_authentication_flow(self, api_client: APIClient) -> None:
        """Test complete JWT authentication and token usage flow."""
        # 1. Create user
        user = User.objects.create_user(
            username="authtest", password="testpass123"  # nosec B106
        )

        # 2. Obtain JWT tokens
        token_data: dict[str, str] = {
            "username": "authtest",
            "password": "testpass123",  # nosec B106
        }
        token_response = api_client.post("/api/token/", token_data)
        assert token_response.status_code == status.HTTP_200_OK
        assert "access" in token_response.data  # type: ignore[operator]
        assert "refresh" in token_response.data  # type: ignore[operator]

        access_token = token_response.data["access"]  # type: ignore[index]

        # 3. Use access token to create transaction
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        create_data: dict[str, Any] = {
            "amount": "200.00",
            "category": "income",
        }
        create_response = api_client.post("/api/transactions/", create_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        assert create_response.data["user"] == user.id  # type: ignore[index]

        # 4. Use token to list transactions
        list_response = api_client.get("/api/transactions/")
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) == 1  # type: ignore[arg-type]

    def test_multi_user_isolation_scenario(self, api_client: APIClient) -> None:
        """Test that multiple users can only access their own transactions."""
        # Create two users
        user1 = UserFactory(username="user1")
        user2 = UserFactory(username="user2")

        # Create transactions for both users
        user1_transaction1 = TransactionFactory(
            user=user1, amount=Decimal("100.00"), description="User1 Transaction1"
        )
        user1_transaction2 = TransactionFactory(
            user=user1, amount=Decimal("200.00"), description="User1 Transaction2"
        )
        user2_transaction1 = TransactionFactory(
            user=user2, amount=Decimal("300.00"), description="User2 Transaction1"
        )
        user2_transaction2 = TransactionFactory(
            user=user2, amount=Decimal("400.00"), description="User2 Transaction2"
        )

        # User1 authenticates and lists transactions
        user1_token = str(RefreshToken.for_user(user1).access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_token}")
        user1_response = api_client.get("/api/transactions/")

        assert user1_response.status_code == status.HTTP_200_OK
        assert len(user1_response.data) == 2  # type: ignore[arg-type]
        user1_ids = [t["id"] for t in user1_response.data]  # type: ignore[union-attr]
        assert user1_transaction1.id in user1_ids
        assert user1_transaction2.id in user1_ids
        assert user2_transaction1.id not in user1_ids
        assert user2_transaction2.id not in user1_ids

        # User2 authenticates and lists transactions
        user2_token = str(RefreshToken.for_user(user2).access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_token}")
        user2_response = api_client.get("/api/transactions/")

        assert user2_response.status_code == status.HTTP_200_OK
        assert len(user2_response.data) == 2  # type: ignore[arg-type]
        user2_ids = [t["id"] for t in user2_response.data]  # type: ignore[union-attr]
        assert user2_transaction1.id in user2_ids
        assert user2_transaction2.id in user2_ids
        assert user1_transaction1.id not in user2_ids
        assert user1_transaction2.id not in user2_ids

        # User1 cannot access User2's transaction
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user1_token}")
        forbidden_response = api_client.get(
            f"/api/transactions/{user2_transaction1.id}/"
        )
        assert forbidden_response.status_code == status.HTTP_404_NOT_FOUND

    def test_transaction_updates_maintain_user_ownership(
        self, api_client: APIClient
    ) -> None:
        """Test that updating transaction does not change ownership."""
        user1 = UserFactory(username="owner")
        user2 = UserFactory(username="attacker")

        # User1 creates transaction
        transaction = TransactionFactory(user=user1, amount=Decimal("100.00"))

        # User2 authenticates and attempts to update User1's transaction
        user2_token = str(RefreshToken.for_user(user2).access_token)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user2_token}")

        update_data: dict[str, Any] = {
            "amount": "999.00",
            "category": "expense",
        }
        update_response = api_client.put(
            f"/api/transactions/{transaction.id}/", update_data
        )

        # Should fail with 404 (transaction not in user2's queryset)
        assert update_response.status_code == status.HTTP_404_NOT_FOUND

        # Verify transaction is unchanged
        transaction.refresh_from_db()
        assert transaction.amount == Decimal("100.00")
        assert transaction.user == user1

    def test_cascade_delete_user_deletes_transactions(self) -> None:
        """Test that deleting a user cascades to delete their transactions."""
        user = UserFactory()
        transaction1 = TransactionFactory(user=user)
        transaction2 = TransactionFactory(user=user)
        transaction3 = TransactionFactory(user=user)

        transaction_ids = [transaction1.id, transaction2.id, transaction3.id]

        # Verify transactions exist
        assert Transaction.objects.filter(user=user).count() == 3

        # Delete user
        user.delete()

        # Verify all user's transactions are deleted
        assert Transaction.objects.filter(id__in=transaction_ids).count() == 0

    def test_bulk_transaction_creation_for_user(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test creating multiple transactions for a user in sequence."""
        transactions_data = [
            {"amount": "100.00", "category": "income", "description": "Salary"},
            {"amount": "50.00", "category": "expense", "description": "Groceries"},
            {"amount": "200.00", "category": "income", "description": "Freelance"},
            {"amount": "30.00", "category": "expense", "description": "Transport"},
            {"amount": "150.00", "category": "income", "description": "Bonus"},
        ]

        created_ids = []
        for data in transactions_data:
            response = authenticated_client.post("/api/transactions/", data)
            assert response.status_code == status.HTTP_201_CREATED
            created_ids.append(response.data["id"])  # type: ignore[index]

        # Verify all transactions are in the list
        list_response = authenticated_client.get("/api/transactions/")
        assert list_response.status_code == status.HTTP_200_OK
        assert len(list_response.data) == 5  # type: ignore[arg-type]

        # Verify all created IDs are present
        returned_ids = [t["id"] for t in list_response.data]  # type: ignore[union-attr]
        for created_id in created_ids:
            assert created_id in returned_ids

    def test_unauthenticated_access_rejected_for_all_endpoints(
        self, api_client: APIClient, user: User
    ) -> None:
        """Test that all transaction endpoints require authentication."""
        transaction = TransactionFactory(user=user)

        # Test LIST
        list_response = api_client.get("/api/transactions/")
        assert list_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test RETRIEVE
        retrieve_response = api_client.get(f"/api/transactions/{transaction.id}/")
        assert retrieve_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test CREATE
        create_data: dict[str, Any] = {"amount": "100.00", "category": "income"}
        create_response = api_client.post("/api/transactions/", create_data)
        assert create_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test UPDATE
        update_data: dict[str, Any] = {"amount": "200.00", "category": "expense"}
        update_response = api_client.put(
            f"/api/transactions/{transaction.id}/", update_data
        )
        assert update_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test PARTIAL UPDATE
        patch_data: dict[str, Any] = {"amount": "300.00"}
        patch_response = api_client.patch(
            f"/api/transactions/{transaction.id}/", patch_data
        )
        assert patch_response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test DELETE
        delete_response = api_client.delete(f"/api/transactions/{transaction.id}/")
        assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED
