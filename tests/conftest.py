"""
Pytest configuration and fixtures for Django Financial API tests.

This module provides reusable test fixtures for database setup,
user authentication, and API client configuration.
"""

from typing import Any

from django.contrib.auth.models import User

from rest_framework.test import APIClient

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Transaction


@pytest.fixture
def api_client() -> APIClient:
    """
    Provide a DRF API test client.

    Returns:
        APIClient: An unauthenticated API client instance.

    Examples:
        >>> def test_endpoint(api_client):
        ...     response = api_client.get('/api/transactions/')
        ...     assert response.status_code == 401
    """
    return APIClient()


@pytest.fixture
def user(db: Any) -> User:
    """
    Create a test user.

    Args:
        db: Pytest-django database fixture.

    Returns:
        User: A created user instance with username 'testuser'.

    Examples:
        >>> def test_with_user(user):
        ...     assert user.username == 'testuser'
        ...     assert user.is_active is True
    """
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",  # nosec B106
    )


@pytest.fixture
def admin_user(db: Any) -> User:
    """
    Create an admin test user.

    Args:
        db: Pytest-django database fixture.

    Returns:
        User: A created superuser instance.

    Examples:
        >>> def test_with_admin(admin_user):
        ...     assert admin_user.is_superuser is True
        ...     assert admin_user.is_staff is True
    """
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",  # nosec B106
    )


@pytest.fixture
def authenticated_client(api_client: APIClient, user: User) -> APIClient:
    """
    Provide an authenticated API client with JWT token.

    Args:
        api_client: API client fixture.
        user: User fixture.

    Returns:
        APIClient: An API client authenticated with JWT token.

    Examples:
        >>> def test_authenticated(authenticated_client):
        ...     response = authenticated_client.get('/api/transactions/')
        ...     assert response.status_code == 200
    """
    refresh: RefreshToken = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def admin_client(api_client: APIClient, admin_user: User) -> APIClient:
    """
    Provide an authenticated admin API client with JWT token.

    Args:
        api_client: API client fixture.
        admin_user: Admin user fixture.

    Returns:
        APIClient: An API client authenticated as admin.

    Examples:
        >>> def test_admin_access(admin_client):
        ...     response = admin_client.get('/admin/')
        ...     assert response.status_code == 200
    """
    refresh: RefreshToken = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def sample_transaction(user: User) -> Transaction:
    """
    Create a sample transaction for testing.

    Args:
        user: User fixture.

    Returns:
        Transaction: A created transaction instance.

    Examples:
        >>> def test_transaction(sample_transaction):
        ...     assert sample_transaction.amount == 100.50
        ...     assert sample_transaction.category == 'income'
    """
    return Transaction.objects.create(
        user=user,
        amount=100.50,
        category="income",
        description="Test transaction",
    )


@pytest.fixture
def multiple_transactions(user: User) -> list[Transaction]:
    """
    Create multiple transactions for testing list operations.

    Args:
        user: User fixture.

    Returns:
        list[Transaction]: A list of 5 created transaction instances.

    Examples:
        >>> def test_list(multiple_transactions):
        ...     assert len(multiple_transactions) == 5
    """
    transactions = [
        Transaction.objects.create(
            user=user,
            amount=100.00 + i * 10,
            category="income" if i % 2 == 0 else "expense",
            description=f"Transaction {i}",
        )
        for i in range(5)
    ]
    return transactions
