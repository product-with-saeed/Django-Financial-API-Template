"""
Unit tests for Transaction ViewSet.

Tests API endpoints, permissions, authentication, and user isolation.
"""

from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient

import pytest

from api.models import Transaction
from tests.factories import TransactionFactory, UserFactory


@pytest.mark.django_db
class TestTransactionViewSet:
    """Test suite for TransactionViewSet API endpoints."""

    def test_list_transactions_requires_authentication(
        self, api_client: APIClient
    ) -> None:
        """Test that listing transactions requires authentication."""
        response = api_client.get("/api/transactions/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_transactions_returns_only_user_transactions(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test that users can only see their own transactions."""
        # Create transactions for authenticated user
        user_transaction1 = TransactionFactory(user=user, amount=Decimal("100.00"))
        user_transaction2 = TransactionFactory(user=user, amount=Decimal("200.00"))

        # Create transactions for another user
        other_user = UserFactory()
        TransactionFactory(user=other_user, amount=Decimal("300.00"))
        TransactionFactory(user=other_user, amount=Decimal("400.00"))

        response = authenticated_client.get("/api/transactions/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # type: ignore[arg-type]
        transaction_ids = [t["id"] for t in response.data]  # type: ignore[union-attr]
        assert user_transaction1.id in transaction_ids
        assert user_transaction2.id in transaction_ids

    def test_list_transactions_empty_for_new_user(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that new users see empty transaction list."""
        # Create transactions for other users
        other_user = UserFactory()
        TransactionFactory(user=other_user)

        response = authenticated_client.get("/api/transactions/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0  # type: ignore[arg-type]

    def test_retrieve_transaction_requires_authentication(
        self, api_client: APIClient, user: User
    ) -> None:
        """Test that retrieving a transaction requires authentication."""
        transaction = TransactionFactory(user=user)

        response = api_client.get(f"/api/transactions/{transaction.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_own_transaction_success(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test that users can retrieve their own transactions."""
        transaction = TransactionFactory(
            user=user, amount=Decimal("150.75"), category="income", description="Salary"
        )

        response = authenticated_client.get(f"/api/transactions/{transaction.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == transaction.id  # type: ignore[index]
        assert Decimal(response.data["amount"]) == Decimal("150.75")  # type: ignore[index]
        assert response.data["category"] == "income"  # type: ignore[index]
        assert response.data["description"] == "Salary"  # type: ignore[index]

    def test_retrieve_other_user_transaction_forbidden(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that users cannot retrieve other users' transactions."""
        other_user = UserFactory()
        other_transaction = TransactionFactory(user=other_user)

        response = authenticated_client.get(
            f"/api/transactions/{other_transaction.id}/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_transaction_requires_authentication(
        self, api_client: APIClient
    ) -> None:
        """Test that creating a transaction requires authentication."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "category": "income",
            "description": "Test",
        }

        response = api_client.post("/api/transactions/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_transaction_success(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test successful transaction creation."""
        data: dict[str, Any] = {
            "amount": "250.50",
            "category": "expense",
            "description": "Office supplies",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Decimal(response.data["amount"]) == Decimal("250.50")  # type: ignore[index]
        assert response.data["category"] == "expense"  # type: ignore[index]
        assert response.data["description"] == "Office supplies"  # type: ignore[index]
        assert response.data["user"] == user.id  # type: ignore[index]

        # Verify transaction was created in database
        assert Transaction.objects.filter(user=user, amount=Decimal("250.50")).exists()

    def test_create_transaction_auto_assigns_user(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test that created transaction is automatically assigned to authenticated user."""
        other_user = UserFactory()

        data: dict[str, Any] = {
            "user": other_user.id,  # Attempt to set different user
            "amount": "100.00",
            "category": "income",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_201_CREATED
        # User should be the authenticated user, not other_user
        assert response.data["user"] == user.id  # type: ignore[index]
        assert response.data["user"] != other_user.id  # type: ignore[index]

    def test_create_transaction_missing_amount(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that creating transaction without amount fails."""
        data: dict[str, Any] = {
            "category": "income",
            "description": "Test",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount" in response.data  # type: ignore[operator]

    def test_create_transaction_missing_category(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that creating transaction without category fails."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "description": "Test",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category" in response.data  # type: ignore[operator]

    def test_create_transaction_invalid_category(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that creating transaction with invalid category fails."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "category": "invalid_category",
            "description": "Test",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category" in response.data  # type: ignore[operator]

    def test_update_transaction_requires_authentication(
        self, api_client: APIClient, user: User
    ) -> None:
        """Test that updating a transaction requires authentication."""
        transaction = TransactionFactory(user=user)
        data: dict[str, Any] = {"amount": "200.00"}

        response = api_client.put(f"/api/transactions/{transaction.id}/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_own_transaction_success(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test successful update of own transaction."""
        transaction = TransactionFactory(
            user=user, amount=Decimal("100.00"), category="income"
        )

        data: dict[str, Any] = {
            "amount": "150.00",
            "category": "expense",
            "description": "Updated description",
        }

        response = authenticated_client.put(
            f"/api/transactions/{transaction.id}/", data
        )

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["amount"]) == Decimal("150.00")  # type: ignore[index]
        assert response.data["category"] == "expense"  # type: ignore[index]
        assert response.data["description"] == "Updated description"  # type: ignore[index]

        # Verify in database
        transaction.refresh_from_db()
        assert transaction.amount == Decimal("150.00")
        assert transaction.category == "expense"

    def test_update_other_user_transaction_forbidden(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that users cannot update other users' transactions."""
        other_user = UserFactory()
        other_transaction = TransactionFactory(user=other_user)

        data: dict[str, Any] = {
            "amount": "200.00",
            "category": "income",
        }

        response = authenticated_client.put(
            f"/api/transactions/{other_transaction.id}/", data
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_transaction_success(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test partial update (PATCH) of own transaction."""
        transaction = TransactionFactory(
            user=user,
            amount=Decimal("100.00"),
            category="income",
            description="Original",
        )

        # Only update amount
        data: dict[str, Any] = {"amount": "200.00"}

        response = authenticated_client.patch(
            f"/api/transactions/{transaction.id}/", data
        )

        assert response.status_code == status.HTTP_200_OK
        assert Decimal(response.data["amount"]) == Decimal("200.00")  # type: ignore[index]
        # Other fields should remain unchanged
        assert response.data["category"] == "income"  # type: ignore[index]
        assert response.data["description"] == "Original"  # type: ignore[index]

    def test_delete_transaction_requires_authentication(
        self, api_client: APIClient, user: User
    ) -> None:
        """Test that deleting a transaction requires authentication."""
        transaction = TransactionFactory(user=user)

        response = api_client.delete(f"/api/transactions/{transaction.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_own_transaction_success(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test successful deletion of own transaction."""
        transaction = TransactionFactory(user=user)
        transaction_id = transaction.id

        response = authenticated_client.delete(f"/api/transactions/{transaction_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        # Verify transaction is deleted from database
        assert not Transaction.objects.filter(id=transaction_id).exists()

    def test_delete_other_user_transaction_forbidden(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that users cannot delete other users' transactions."""
        other_user = UserFactory()
        other_transaction = TransactionFactory(user=other_user)
        transaction_id = other_transaction.id

        response = authenticated_client.delete(f"/api/transactions/{transaction_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Verify transaction still exists
        assert Transaction.objects.filter(id=transaction_id).exists()

    def test_list_transactions_with_multiple_users(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test that user isolation works correctly with multiple users."""
        # Create 3 transactions for authenticated user
        TransactionFactory.create_batch(3, user=user)

        # Create 5 transactions for other users
        user2 = UserFactory()
        user3 = UserFactory()
        TransactionFactory.create_batch(2, user=user2)
        TransactionFactory.create_batch(3, user=user3)

        response = authenticated_client.get("/api/transactions/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3  # type: ignore[arg-type]
        # Verify all returned transactions belong to authenticated user
        for transaction_data in response.data:  # type: ignore[union-attr]
            assert transaction_data["user"] == user.id

    def test_transaction_date_is_auto_set(
        self, authenticated_client: APIClient
    ) -> None:
        """Test that transaction date is automatically set on creation."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "category": "income",
        }

        response = authenticated_client.post("/api/transactions/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "date" in response.data  # type: ignore[operator]
        assert response.data["date"] is not None  # type: ignore[index]

    def test_transaction_id_is_read_only(
        self, authenticated_client: APIClient, user: User
    ) -> None:
        """Test that transaction ID cannot be modified on update."""
        transaction = TransactionFactory(user=user)
        original_id = transaction.id

        data: dict[str, Any] = {
            "id": 99999,  # Attempt to change ID
            "amount": "100.00",
            "category": "income",
        }

        response = authenticated_client.put(
            f"/api/transactions/{transaction.id}/", data
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == original_id  # type: ignore[index]
        assert response.data["id"] != 99999  # type: ignore[index]
