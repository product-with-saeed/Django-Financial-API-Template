"""
Unit tests for Swagger/OpenAPI documentation.

Tests schema generation, endpoint documentation, and API metadata.
"""

from typing import Any

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

import pytest


@pytest.mark.django_db
class TestSwaggerDocumentation:
    """Test suite for Swagger/OpenAPI documentation endpoints."""

    def test_swagger_ui_accessible(self, api_client: APIClient) -> None:
        """Test that Swagger UI endpoint is accessible."""
        url = reverse("schema-swagger-ui")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "swagger" in response.content.decode().lower()

    def test_redoc_ui_accessible(self, api_client: APIClient) -> None:
        """Test that ReDoc UI endpoint is accessible."""
        url = reverse("schema-redoc")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "redoc" in response.content.decode().lower()

    def test_swagger_json_schema_generation(self, api_client: APIClient) -> None:
        """Test that OpenAPI JSON schema is generated correctly."""
        url = "/swagger.json"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "application/json" in response["Content-Type"]

        schema: dict[str, Any] = response.json()
        assert "swagger" in schema or "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_schema_contains_api_info(self, api_client: APIClient) -> None:
        """Test that schema contains proper API information."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        assert "info" in schema
        info = schema["info"]
        assert "title" in info
        assert "Django Financial API" in info["title"]
        assert "version" in info
        assert "description" in info

    def test_schema_contains_transaction_endpoints(self, api_client: APIClient) -> None:
        """Test that schema includes all transaction endpoints."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        assert "paths" in schema
        paths = schema["paths"]

        # Check that transaction endpoints exist
        assert "/transactions/" in paths
        assert "/transactions/{id}/" in paths

    def test_schema_documents_http_methods(self, api_client: APIClient) -> None:
        """Test that schema documents all HTTP methods for transactions."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        transactions_list = schema["paths"]["/transactions/"]
        transactions_detail = schema["paths"]["/transactions/{id}/"]

        # List endpoint should have GET and POST
        assert "get" in transactions_list
        assert "post" in transactions_list

        # Detail endpoint should have GET, PUT, PATCH, DELETE
        assert "get" in transactions_detail
        assert "put" in transactions_detail
        assert "patch" in transactions_detail
        assert "delete" in transactions_detail

    def test_schema_includes_authentication(self, api_client: APIClient) -> None:
        """Test that schema documents authentication requirements."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        # Check for security definitions
        assert (
            "securityDefinitions" in schema or "components" in schema
        ), "Schema should include security definitions"

    def test_schema_includes_request_body_examples(self, api_client: APIClient) -> None:
        """Test that POST/PUT endpoints include request body schemas."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        # Check POST endpoint has request body definition
        post_endpoint = schema["paths"]["/transactions/"]["post"]
        assert (
            "parameters" in post_endpoint or "requestBody" in post_endpoint
        ), "POST endpoint should define request body"

    def test_schema_includes_response_schemas(self, api_client: APIClient) -> None:
        """Test that endpoints include response schema definitions."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        get_endpoint = schema["paths"]["/transactions/"]["get"]
        assert "responses" in get_endpoint
        assert "200" in get_endpoint["responses"]

    def test_schema_includes_authentication_endpoints(
        self, api_client: APIClient
    ) -> None:
        """Test that JWT authentication endpoints are documented."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        paths = schema["paths"]
        assert "/token/" in paths
        assert "/token/refresh/" in paths

    def test_swagger_ui_contains_api_title(self, api_client: APIClient) -> None:
        """Test that Swagger UI displays the API title."""
        url = reverse("schema-swagger-ui")
        response = api_client.get(url)
        content = response.content.decode()

        assert "Django Financial API" in content

    def test_schema_parameter_descriptions(self, api_client: APIClient) -> None:
        """Test that schema includes parameter descriptions."""
        url = "/swagger.json"
        response = api_client.get(url)
        schema: dict[str, Any] = response.json()

        # Check detail endpoint has id parameter documented
        detail_path = schema["paths"]["/transactions/{id}/"]
        if "parameters" in detail_path:
            params = detail_path["parameters"]
            id_param = next((p for p in params if p.get("name") == "id"), None)
            assert id_param is not None, "ID parameter should be documented"
