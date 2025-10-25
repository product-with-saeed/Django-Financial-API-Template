"""
Models for the Financial API.
Defines the Transaction model to store financial transactions.
"""

from decimal import Decimal
from typing import ClassVar

from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    """
    Represents a financial transaction for a user.

    Attributes:
        user (User): The user associated with the transaction.
        amount (Decimal): The amount of the transaction.
        category (str): The type of transaction (income or expense).
        description (str, optional): Additional details about the transaction.
        date (Date): The date when the transaction was recorded.

    Examples:
        >>> user = User.objects.get(username='john')
        >>> transaction = Transaction.objects.create(
        ...     user=user,
        ...     amount=Decimal('100.50'),
        ...     category='income',
        ...     description='Freelance payment'
        ... )
        >>> str(transaction)
        'john - income: $100.50'
    """

    CATEGORY_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user: models.ForeignKey[User, User] = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2)
    category: models.CharField = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES
    )
    description: models.TextField = models.TextField(blank=True, null=True)
    date: models.DateField = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Return a human-readable string representation of the transaction.

        Returns:
            str: Formatted string in format "username - category: $amount"

        Examples:
            >>> transaction = Transaction(
            ...     user=user,
            ...     category='income',
            ...     amount=Decimal('100.50')
            ... )
            >>> str(transaction)
            'john - income: $100.50'
        """
        return f"{self.user.username} - {self.category}: ${self.amount}"
