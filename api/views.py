"""
API views for the Financial API.
Defines the TransactionViewSet to handle CRUD operations for transactions.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from .models import Transaction
from .serializers import TransactionSerializer
from .throttling import TransactionAnonThrottle, TransactionUserThrottle


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing financial transactions.

    Provides CRUD operations (Create, Read, Update, Delete) for transactions.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TransactionUserThrottle, TransactionAnonThrottle]

    def get_queryset(self):
        """
        Return transactions that belong to the authenticated user.

        Returns:
            QuerySet: Filtered transactions for the logged-in user.
        """
        return Transaction.objects.filter(user=self.request.user)
