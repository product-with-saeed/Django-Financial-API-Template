"""
API views for the Financial API.
Defines the TransactionViewSet to handle CRUD operations for transactions.
"""

from typing import ClassVar

from django.db.models import QuerySet

from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from api.models import Transaction
from api.serializers import TransactionSerializer
from api.throttling import TransactionAnonThrottle, TransactionUserThrottle


class TransactionViewSet(viewsets.ModelViewSet[Transaction]):
    """
    API endpoints for managing financial transactions.

    Provides complete CRUD (Create, Read, Update, Delete) operations for transactions.
    All transactions are automatically scoped to the authenticated user,
    ensuring data isolation and security.

    **Authentication:** JWT Bearer token required for all endpoints.

    **Rate Limiting:**
    - Authenticated users: 500 requests/day
    - Anonymous users: 5 requests/minute

    **Endpoints:**
    - `GET /api/transactions/` - List all user's transactions
    - `POST /api/transactions/` - Create a new transaction
    - `GET /api/transactions/{id}/` - Retrieve a specific transaction
    - `PUT /api/transactions/{id}/` - Update a transaction (full)
    - `PATCH /api/transactions/{id}/` - Update a transaction (partial)
    - `DELETE /api/transactions/{id}/` - Delete a transaction

    **Example Transaction:**
    ```json
    {
        "id": 1,
        "amount": "100.50",
        "category": "income",
        "description": "Freelance payment",
        "date": "2025-10-25T12:00:00Z",
        "user": 1
    }
    ```
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [IsAuthenticated]
    throttle_classes: ClassVar[
        list[type[TransactionUserThrottle] | type[TransactionAnonThrottle]]
    ] = [TransactionUserThrottle, TransactionAnonThrottle]

    @swagger_auto_schema(
        operation_description="List all transactions for the authenticated user.",
        operation_summary="List user transactions",
        responses={
            200: openapi.Response(
                description="List of transactions",
                schema=TransactionSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "amount": "100.50",
                            "category": "income",
                            "description": "Freelance payment",
                            "date": "2025-10-25T12:00:00Z",
                            "user": 1,
                        },
                        {
                            "id": 2,
                            "amount": "50.00",
                            "category": "expense",
                            "description": "Groceries",
                            "date": "2025-10-24T10:30:00Z",
                            "user": 1,
                        },
                    ]
                },
            ),
            401: "Unauthorized - Authentication required",
        },
        tags=["transactions"],
    )
    def list(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """List all transactions for the authenticated user."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Create a new financial transaction. "
            "The user field is automatically set to the authenticated user."
        ),
        operation_summary="Create transaction",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["amount", "category"],
            properties={
                "amount": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Transaction amount (decimal, max 10 digits, 2 decimal places)",
                    example="100.50",
                ),
                "category": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Transaction category (income or expense)",
                    enum=["income", "expense"],
                    example="income",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Optional transaction description",
                    example="Freelance payment for web design project",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Transaction created successfully",
                schema=TransactionSerializer(),
                examples={
                    "application/json": {
                        "id": 3,
                        "amount": "100.50",
                        "category": "income",
                        "description": "Freelance payment for web design project",
                        "date": "2025-10-25T14:30:00Z",
                        "user": 1,
                    }
                },
            ),
            400: "Bad Request - Invalid data",
            401: "Unauthorized - Authentication required",
        },
        tags=["transactions"],
    )
    def create(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Create a new transaction."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Retrieve a specific transaction by ID. "
            "Users can only access their own transactions."
        ),
        operation_summary="Retrieve transaction",
        responses={
            200: TransactionSerializer(),
            401: "Unauthorized - Authentication required",
            404: (
                "Not Found - Transaction does not exist " "or belongs to another user"
            ),
        },
        tags=["transactions"],
    )
    def retrieve(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Retrieve a specific transaction."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Update all fields of a transaction. "
            "Users can only update their own transactions."
        ),
        operation_summary="Update transaction (full)",
        request_body=TransactionSerializer(),
        responses={
            200: TransactionSerializer(),
            400: "Bad Request - Invalid data",
            401: "Unauthorized - Authentication required",
            404: (
                "Not Found - Transaction does not exist " "or belongs to another user"
            ),
        },
        tags=["transactions"],
    )
    def update(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Update a transaction (full update)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Partially update specific fields of a transaction. "
            "Users can only update their own transactions."
        ),
        operation_summary="Update transaction (partial)",
        request_body=TransactionSerializer(partial=True),
        responses={
            200: TransactionSerializer(),
            400: "Bad Request - Invalid data",
            401: "Unauthorized - Authentication required",
            404: (
                "Not Found - Transaction does not exist " "or belongs to another user"
            ),
        },
        tags=["transactions"],
    )
    def partial_update(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Partially update a transaction."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            "Delete a transaction permanently. "
            "Users can only delete their own transactions."
        ),
        operation_summary="Delete transaction",
        responses={
            204: "No Content - Transaction deleted successfully",
            401: "Unauthorized - Authentication required",
            404: (
                "Not Found - Transaction does not exist " "or belongs to another user"
            ),
        },
        tags=["transactions"],
    )
    def destroy(self, request, *args, **kwargs):  # type: ignore[no-untyped-def]
        """Delete a transaction."""
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self) -> "QuerySet[Transaction, Transaction]":
        """
        Return transactions that belong to the authenticated user.

        This method ensures that users can only access their own transactions,
        providing data isolation and security.

        For schema generation (swagger_fake_view), returns all transactions
        to allow proper API documentation generation.

        Returns:
            QuerySet[Transaction]: Filtered transactions for the authenticated user.

        Examples:
            >>> viewset = TransactionViewSet()
            >>> viewset.request = request  # request.user is authenticated
            >>> queryset = viewset.get_queryset()
            >>> all(t.user == request.user for t in queryset)
            True
        """
        # Return base queryset for schema generation
        if getattr(self, "swagger_fake_view", False):
            return Transaction.objects.all()

        # Return user-filtered queryset for normal requests
        return Transaction.objects.filter(user=self.request.user)
