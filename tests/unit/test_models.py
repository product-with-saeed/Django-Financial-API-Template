"""
Unit tests for Transaction model.

Tests model validation, fields, methods, and relationships.
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError

import pytest

from api.models import Transaction
from tests.factories import TransactionFactory, UserFactory


@pytest.mark.django_db
class TestTransactionModel:
    """Test suite for Transaction model."""

    def test_create_transaction_with_valid_data(self, user: User) -> None:
        """Test creating a transaction with valid data."""
        transaction = Transaction.objects.create(
            user=user,
            amount=Decimal("100.50"),
            category="income",
            description="Test transaction",
        )

        assert transaction.id is not None
        assert transaction.user == user
        assert transaction.amount == Decimal("100.50")
        assert transaction.category == "income"
        assert transaction.description == "Test transaction"
        assert transaction.date is not None

    def test_transaction_str_representation(self, user: User) -> None:
        """Test __str__ method returns formatted string."""
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("100.50"), category="income"
        )

        expected = f"{user.username} - income: $100.50"
        assert str(transaction) == expected

    def test_transaction_amount_decimal_precision(self, user: User) -> None:
        """Test amount field accepts correct decimal precision."""
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("99.99"), category="expense"
        )

        assert transaction.amount == Decimal("99.99")
        assert isinstance(transaction.amount, Decimal)

    def test_transaction_category_choices(self, user: User) -> None:
        """Test category field accepts valid choices."""
        # Test income
        income = Transaction.objects.create(
            user=user, amount=Decimal("100"), category="income"
        )
        assert income.category == "income"

        # Test expense
        expense = Transaction.objects.create(
            user=user, amount=Decimal("50"), category="expense"
        )
        assert expense.category == "expense"

    def test_transaction_description_can_be_blank(self, user: User) -> None:
        """Test description field is optional."""
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("100"), category="income", description=""
        )

        assert transaction.description == ""
        assert transaction.id is not None

    def test_transaction_description_can_be_null(self, user: User) -> None:
        """Test description field can be None."""
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("100"), category="income", description=None
        )

        assert transaction.description is None
        assert transaction.id is not None

    def test_transaction_date_auto_set(self, user: User) -> None:
        """Test date field is automatically set on creation."""
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("100"), category="income"
        )

        assert transaction.date is not None
        # Date should be set to today
        from datetime import date

        assert transaction.date == date.today()

    def test_transaction_user_relationship(self) -> None:
        """Test transaction is linked to user correctly."""
        user = UserFactory()
        transaction = TransactionFactory(user=user)

        assert transaction.user == user
        assert transaction in user.transaction_set.all()

    def test_transaction_cascade_delete_with_user(self) -> None:
        """Test transactions are deleted when user is deleted."""
        user = UserFactory()
        transaction1 = TransactionFactory(user=user)
        transaction2 = TransactionFactory(user=user)

        transaction_ids = [transaction1.id, transaction2.id]

        # Delete user
        user.delete()

        # Transactions should be deleted
        assert not Transaction.objects.filter(id__in=transaction_ids).exists()

    def test_transaction_queryset_filter_by_user(self) -> None:
        """Test filtering transactions by user."""
        user1 = UserFactory()
        user2 = UserFactory()

        TransactionFactory.create_batch(3, user=user1)
        TransactionFactory.create_batch(2, user=user2)

        user1_transactions = Transaction.objects.filter(user=user1)
        user2_transactions = Transaction.objects.filter(user=user2)

        assert user1_transactions.count() == 3
        assert user2_transactions.count() == 2

    def test_transaction_queryset_filter_by_category(self, user: User) -> None:
        """Test filtering transactions by category."""
        TransactionFactory.create_batch(3, user=user, category="income")
        TransactionFactory.create_batch(2, user=user, category="expense")

        income_transactions = Transaction.objects.filter(category="income")
        expense_transactions = Transaction.objects.filter(category="expense")

        assert income_transactions.count() >= 3
        assert expense_transactions.count() >= 2

    def test_transaction_amount_max_digits(self, user: User) -> None:
        """Test amount field max_digits constraint."""
        # Should accept up to 10 digits total, 2 decimal places
        transaction = Transaction.objects.create(
            user=user, amount=Decimal("99999999.99"), category="income"
        )

        assert transaction.amount == Decimal("99999999.99")

    def test_transaction_user_required(self) -> None:
        """Test that user field is required."""
        with pytest.raises(IntegrityError):
            Transaction.objects.create(
                user=None, amount=Decimal("100"), category="income"  # type: ignore[arg-type]
            )

    def test_transaction_amount_required(self, user: User) -> None:
        """Test that amount field is required."""
        with pytest.raises(IntegrityError):
            Transaction.objects.create(user=user, amount=None, category="income")  # type: ignore[arg-type]

    def test_transaction_category_required(self, user: User) -> None:
        """Test that category field is required."""
        with pytest.raises(IntegrityError):
            Transaction.objects.create(user=user, amount=Decimal("100"), category=None)  # type: ignore[arg-type]
