"""
URL routing for the Financial API.
Defines API endpoints for managing transactions.
"""

from django.urls import URLPattern, URLResolver, include, path

from rest_framework.routers import DefaultRouter

from api.views import TransactionViewSet

# Create a router and register the TransactionViewSet
router: DefaultRouter = DefaultRouter()
router.register(r"transactions", TransactionViewSet)

# Define the URL patterns for the API
urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),
]
