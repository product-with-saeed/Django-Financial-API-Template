"""
Serializers for the Financial API.
Defines the TransactionSerializer for API data serialization.
"""

from typing import Any, Optional

from rest_framework import serializers

from api.models import Transaction
from core.types import APIRequest, SerializerData


class TransactionSerializer(serializers.ModelSerializer[Transaction]):
    """
    Serializer for the Transaction model.

    Converts Transaction model instances into JSON format and vice versa.
    The user field is read-only and automatically set to the authenticated user.

    Attributes:
        Meta: Serializer configuration including model, fields, and read-only fields.

    Examples:
        >>> serializer = TransactionSerializer(data={
        ...     'amount': '100.50',
        ...     'category': 'income',
        ...     'description': 'Freelance payment'
        ... })
        >>> serializer.is_valid()
        True
        >>> transaction = serializer.save()
    """

    class Meta:
        """Serializer configuration."""

        model = Transaction
        fields = ["id", "amount", "category", "description", "date", "user"]
        read_only_fields = ["id", "date", "user"]

    def create(self, validated_data: SerializerData) -> Transaction:
        """
        Create a new transaction with the authenticated user.

        The user is automatically assigned from the request context,
        preventing users from creating transactions for other users.

        Args:
            validated_data: Validated transaction data from the request.
                Must contain 'amount', 'category', and optionally 'description'.

        Returns:
            Transaction: The newly created transaction instance with the
                authenticated user assigned.

        Raises:
            ValueError: If request context or authenticated user is not available.

        Examples:
            >>> serializer = TransactionSerializer(
            ...     data={'amount': '100.50', 'category': 'income'},
            ...     context={'request': request}
            ... )
            >>> transaction = serializer.save()
            >>> transaction.user == request.user
            True
        """
        # Automatically assign the authenticated user from the request context
        request: APIRequest | None = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)
