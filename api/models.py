"""
Models for the Financial API.
Defines the Transaction model to store financial transactions.
"""

from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    """
    Represents a financial transaction for a user.

    Attributes:
        user (User): The user associated with the transaction.
        amount (Decimal): The amount of the transaction.
        category (str): The type of transaction (income or expense).
        description (str, optional): Additional details about the transaction.
        date (Date): The date when the transaction was recorded.
    """

    CATEGORY_CHOICES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the transaction."""
        return f"{self.user.username} - {self.category}: ${self.amount}"
