"""
API views for the Financial API.
Defines the TransactionViewSet to handle CRUD operations for transactions.
"""

from typing import ClassVar

from django.db.models import QuerySet

from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from api.models import Transaction
from api.serializers import TransactionSerializer
from api.throttling import TransactionAnonThrottle, TransactionUserThrottle


class TransactionViewSet(viewsets.ModelViewSet[Transaction]):
    """
    ViewSet for managing financial transactions.

    Provides CRUD operations (Create, Read, Update, Delete) for transactions.
    All transactions are scoped to the authenticated user.

    Attributes:
        queryset: Base queryset for all transactions (filtered in get_queryset).
        serializer_class: Serializer class for transaction data.
        permission_classes: List of permission classes (requires authentication).
        throttle_classes: List of throttle classes for rate limiting.

    Examples:
        GET /api/transactions/ - List all user's transactions
        POST /api/transactions/ - Create a new transaction
        GET /api/transactions/{id}/ - Retrieve a specific transaction
        PUT /api/transactions/{id}/ - Update a transaction
        DELETE /api/transactions/{id}/ - Delete a transaction
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [IsAuthenticated]
    throttle_classes: ClassVar[
        list[type[TransactionUserThrottle] | type[TransactionAnonThrottle]]
    ] = [TransactionUserThrottle, TransactionAnonThrottle]

    def get_queryset(self) -> "QuerySet[Transaction, Transaction]":
        """
        Return transactions that belong to the authenticated user.

        This method ensures that users can only access their own transactions,
        providing data isolation and security.

        Returns:
            QuerySet[Transaction]: Filtered transactions for the authenticated user.

        Examples:
            >>> viewset = TransactionViewSet()
            >>> viewset.request = request  # request.user is authenticated
            >>> queryset = viewset.get_queryset()
            >>> all(t.user == request.user for t in queryset)
            True
        """
        return Transaction.objects.filter(user=self.request.user)
