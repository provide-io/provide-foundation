#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Basic transport system tests."""

from __future__ import annotations

import pytest

from provide.foundation.transport import (
    HTTPMethod,
    Request,
    Response,
    TransportType,
    get_transport,
)
from provide.foundation.transport.base import TransportBase
from provide.foundation.transport.errors import TransportNotFoundError


class MockTransport(TransportBase):
    """Mock transport for testing."""

    def supports(self, transport_type: TransportType) -> bool:
        return transport_type.value == "mock"

    async def execute(self, request: Request) -> Response:
        return Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=b'{"success": true}',
            elapsed_ms=100.0,
            request=request,
        )


def test_request_creation() -> None:
    """Test Request object creation and properties."""
    request = Request(
        uri="https://api.example.com/users",
        method="GET",
        headers={"Authorization": "Bearer token"},
        params={"limit": 10},
        body={"data": "test"},
    )

    assert request.uri == "https://api.example.com/users"
    assert request.method == "GET"
    assert request.headers["Authorization"] == "Bearer token"
    assert request.params["limit"] == 10
    assert request.body["data"] == "test"
    assert request.transport_type == TransportType.HTTPS
    assert request.base_url == "https://api.example.com"


def test_response_creation() -> None:
    """Test Response object creation and methods."""
    request = Request(uri="https://api.example.com/test")

    response = Response(
        status=200,
        headers={"Content-Type": "application/json"},
        body=b'{"message": "success"}',
        elapsed_ms=150.0,
        request=request,
    )

    assert response.status == 200
    assert response.is_success() is True
    assert response.text == '{"message": "success"}'
    assert response.json()["message"] == "success"
    assert response.elapsed_ms == 150.0


def test_response_error_status() -> None:
    """Test Response error checking."""
    response_404 = Response(status=404)
    response_500 = Response(status=500)
    response_200 = Response(status=200)

    assert response_404.is_success() is False
    assert response_500.is_success() is False
    assert response_200.is_success() is True

    from provide.foundation.transport.errors import HTTPResponseError

    with pytest.raises(HTTPResponseError):
        response_404.raise_for_status()

    with pytest.raises(HTTPResponseError):
        response_500.raise_for_status()

    # Should not raise
    response_200.raise_for_status()


def test_transport_registration() -> None:
    """Test transport registration and discovery."""
    # For testing, we'll use HTTP transport that's already registered
    from provide.foundation.transport.http import HTTPTransport

    # Test retrieval of existing transport
    transport = get_transport("https://example.com/test")
    assert isinstance(transport, HTTPTransport)

    # Test error for unknown scheme
    with pytest.raises(TransportNotFoundError):
        get_transport("unknown://example.com")


@pytest.mark.asyncio
async def test_mock_transport() -> None:
    """Test mock transport execution."""
    transport = MockTransport()

    request = Request(
        uri="mock://example.com/test",
        method="GET",
    )

    async with transport:
        response = await transport.execute(request)

    assert response.status == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json()["success"] is True
    assert response.elapsed_ms == 100.0


def test_http_method_enum() -> None:
    """Test HTTPMethod enum values."""
    assert HTTPMethod.GET == "GET"
    assert HTTPMethod.POST == "POST"
    assert HTTPMethod.PUT == "PUT"
    assert HTTPMethod.PATCH == "PATCH"
    assert HTTPMethod.DELETE == "DELETE"
    assert HTTPMethod.HEAD == "HEAD"
    assert HTTPMethod.OPTIONS == "OPTIONS"


def test_transport_type_enum() -> None:
    """Test TransportType enum values."""
    assert TransportType.HTTP == "http"
    assert TransportType.HTTPS == "https"
    assert TransportType.WS == "ws"
    assert TransportType.WSS == "wss"
    assert TransportType.GRPC == "grpc"


# 🧱🏗️🔚
