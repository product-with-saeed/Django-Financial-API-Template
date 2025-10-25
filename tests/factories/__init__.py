"""
Factory classes for generating test data.

This package contains factory_boy factories for creating
test instances of models with realistic fake data.
"""

from tests.factories.transaction_factory import TransactionFactory
from tests.factories.user_factory import UserFactory

__all__ = ["UserFactory", "TransactionFactory"]
