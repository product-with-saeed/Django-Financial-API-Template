"""
Serializers for the Financial API.
Defines the TransactionSerializer for API data serialization.
"""

from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    Converts Transaction model instances into JSON format and vice versa.
    """

    class Meta:
        model = Transaction
        fields = "__all__"
