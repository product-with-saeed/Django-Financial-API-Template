"""
Unit tests for Transaction serializer.

Tests serializer validation, field configuration, and data transformation.
"""

from decimal import Decimal
from typing import Any

from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

import pytest

from api.models import Transaction
from api.serializers import TransactionSerializer
from tests.factories import UserFactory


@pytest.mark.django_db
class TestTransactionSerializer:
    """Test suite for TransactionSerializer."""

    def test_serializer_contains_expected_fields(self) -> None:
        """Test serializer includes all expected fields."""
        serializer = TransactionSerializer()
        expected_fields = {"id", "amount", "category", "description", "date", "user"}

        assert set(serializer.fields.keys()) == expected_fields

    def test_serializer_read_only_fields(self) -> None:
        """Test id, date, and user fields are read-only."""
        serializer = TransactionSerializer()

        assert serializer.fields["id"].read_only is True
        assert serializer.fields["date"].read_only is True
        assert serializer.fields["user"].read_only is True

    def test_serialize_transaction(self, sample_transaction: Transaction) -> None:
        """Test serializing a transaction instance."""
        serializer = TransactionSerializer(sample_transaction)
        data = serializer.data

        assert data["id"] == sample_transaction.id
        assert Decimal(data["amount"]) == sample_transaction.amount
        assert data["category"] == sample_transaction.category
        assert data["description"] == sample_transaction.description
        assert data["user"] == sample_transaction.user.id

    def test_deserialize_valid_data(self, user: User) -> None:
        """Test deserializing valid transaction data."""
        data: dict[str, Any] = {
            "amount": "150.75",
            "category": "expense",
            "description": "Office supplies",
        }

        serializer = TransactionSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["amount"] == Decimal("150.75")
        assert serializer.validated_data["category"] == "expense"

    def test_deserialize_missing_amount(self) -> None:
        """Test validation fails when amount is missing."""
        data: dict[str, Any] = {
            "category": "income",
            "description": "Test",
        }

        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors

    def test_deserialize_missing_category(self) -> None:
        """Test validation fails when category is missing."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "description": "Test",
        }

        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()
        assert "category" in serializer.errors

    def test_deserialize_invalid_category(self) -> None:
        """Test validation fails with invalid category choice."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "category": "invalid_category",
            "description": "Test",
        }

        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()
        assert "category" in serializer.errors

    def test_deserialize_invalid_amount_format(self) -> None:
        """Test validation fails with invalid amount format."""
        data: dict[str, Any] = {
            "amount": "not_a_number",
            "category": "income",
        }

        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()
        assert "amount" in serializer.errors

    def test_deserialize_description_optional(self) -> None:
        """Test description field is optional."""
        data: dict[str, Any] = {
            "amount": "100.00",
            "category": "income",
        }

        serializer = TransactionSerializer(data=data)
        assert serializer.is_valid()
        # Description should default to empty or None
        assert (
            "description" not in serializer.validated_data
            or serializer.validated_data["description"] in [None, ""]
        )

    def test_create_assigns_user_from_request(self, user: User) -> None:
        """Test create() automatically assigns user from request context."""
        factory = APIRequestFactory()
        request = factory.post("/api/transactions/")
        request.user = user

        data: dict[str, Any] = {
            "amount": "200.00",
            "category": "income",
            "description": "Consulting fee",
        }

        serializer = TransactionSerializer(data=data, context={"request": request})
        assert serializer.is_valid()

        transaction = serializer.save()
        assert transaction.user == user
        assert transaction.amount == Decimal("200.00")

    def test_cannot_override_user_in_data(self, user: User) -> None:
        """Test user field in data is ignored (read-only)."""
        other_user = UserFactory()

        factory = APIRequestFactory()
        request = factory.post("/api/transactions/")
        request.user = user

        data: dict[str, Any] = {
            "user": other_user.id,  # Attempt to set different user
            "amount": "100.00",
            "category": "income",
        }

        serializer = TransactionSerializer(data=data, context={"request": request})
        assert serializer.is_valid()

        transaction = serializer.save()
        # User should be from request, not from data
        assert transaction.user == user
        assert transaction.user != other_user

    def test_update_transaction(self, sample_transaction: Transaction) -> None:
        """Test updating an existing transaction."""
        data: dict[str, Any] = {
            "amount": "250.00",
            "category": "expense",
            "description": "Updated description",
        }

        serializer = TransactionSerializer(sample_transaction, data=data, partial=True)
        assert serializer.is_valid()

        updated = serializer.save()
        assert updated.id == sample_transaction.id
        assert updated.amount == Decimal("250.00")
        assert updated.category == "expense"
