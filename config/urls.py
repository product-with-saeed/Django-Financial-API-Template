"""
Main URL configuration for the Financial API.
Includes API and authentication endpoints.
"""

from typing import Any

from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, re_path

from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Define API schema view for Swagger documentation
schema_view: Any = get_schema_view(
    openapi.Info(
        title="Django Financial API",
        default_version="v1.0.0",
        description="""
# Django Financial Transactions API

A **production-ready REST API** for managing financial transactions with
enterprise-grade security and features.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👤 **User Isolation** - Users can only access their own transactions
- 📊 **CRUD Operations** - Complete Create, Read, Update, Delete support
- ⚡ **Rate Limiting** - Protection against API abuse
- 📝 **Auto-generated Docs** - Interactive Swagger UI and ReDoc
- ✅ **99% Test Coverage** - Comprehensive test suite
- 🎯 **Type Hints** - Full Python type annotation coverage

## Authentication

All transaction endpoints require JWT authentication. Obtain a token by sending
a POST request to `/api/token/` with your credentials:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

Include the token in the Authorization header for all subsequent requests:
```
Authorization: Bearer <your_access_token>
```

## Categories

Transactions support two categories:
- **income** - Money received
- **expense** - Money spent

## Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Resource deleted successfully
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Authentication required or failed
- `404 Not Found` - Resource not found or access denied
- `429 Too Many Requests` - Rate limit exceeded

## Support

For questions or issues, please contact: product.with.saeed@gmail.com
        """,
        terms_of_service="https://github.com/product-with-saeed/Django-Financial-API-Template",
        contact=openapi.Contact(
            name="Saeed Mohammadpour",
            email="product.with.saeed@gmail.com",
            url="https://github.com/product-with-saeed",
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT",
        ),
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
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
