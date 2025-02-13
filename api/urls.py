"""
URL routing for the Financial API.
Defines API endpoints for managing transactions.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

# Create a router and register the TransactionViewSet
router = DefaultRouter()
router.register(r"transactions", TransactionViewSet)

# Define the URL patterns for the API
urlpatterns = [
    path("", include(router.urls)),
]
