"""
Main URL configuration for the Financial API.
Includes API and authentication endpoints.
"""

from typing import Any

from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define API schema view for Swagger documentation
schema_view: Any = get_schema_view(
    openapi.Info(
        title="Django Financial API",
        default_version="v1",
        description="API documentation for the Django Financial Transactions System",
        terms_of_service="https://www.yourcompany.com/terms/",
        contact=openapi.Contact(email="support@yourcompany.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Define URL patterns
urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger & Redoc API documentation endpoints
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
