#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""HTTP transport tests with httpx."""

from __future__ import annotations

from collections.abc import Generator

import httpx
import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.transport import (
    HTTPTransport,
    Request,
    TransportConnectionError,
    TransportTimeoutError,
)
from provide.foundation.transport.config import HTTPConfig


@pytest.fixture
def http_config() -> HTTPConfig:
    """HTTP configuration for testing."""
    return HTTPConfig(
        timeout=30.0,
        max_retries=3,
        retry_backoff_factor=0.5,
        verify_ssl=True,
        pool_connections=10,
        pool_maxsize=100,
        follow_redirects=True,
        http2=True,
        max_redirects=5,
    )


@pytest.fixture
def http_transport(http_config: HTTPConfig) -> HTTPTransport:
    """HTTP transport instance."""
    return HTTPTransport(config=http_config)


@pytest.mark.asyncio
async def test_http_transport_get(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test HTTP GET request."""
    # Mock response
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users",
        json={"users": [{"id": 1, "name": "John"}]},
        status_code=200,
        headers={"Content-Type": "application/json"},
    )

    request = Request(
        uri="https://api.example.com/users",
        method="GET",
        headers={"Authorization": "Bearer token"},
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200
    assert response.is_success()
    assert response.headers["content-type"] == "application/json"

    data = response.json()
    assert data["users"][0]["name"] == "John"
    assert response.elapsed_ms > 0


@pytest.mark.asyncio
async def test_http_transport_post_json(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test HTTP POST with JSON body."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/users",
        json={"id": 123, "name": "Jane", "email": "jane@example.com"},
        status_code=201,
    )

    request = Request(
        uri="https://api.example.com/users",
        method="POST",
        body={"name": "Jane", "email": "jane@example.com"},
        headers={"Content-Type": "application/json"},
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 201
    assert response.is_success()

    data = response.json()
    assert data["name"] == "Jane"
    assert data["email"] == "jane@example.com"


@pytest.mark.asyncio
async def test_http_transport_error_status(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test HTTP error status handling."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/not-found",
        status_code=404,
        text="Not Found",
    )

    request = Request(
        uri="https://api.example.com/not-found",
        method="GET",
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 404
    assert not response.is_success()
    assert response.text == "Not Found"


@pytest.mark.asyncio
async def test_http_transport_connection_error(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test connection error handling."""
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    request = Request(
        uri="https://unreachable.example.com",
        method="GET",
    )

    async with http_transport:
        with pytest.raises(TransportConnectionError) as exc_info:
            await http_transport.execute(request)

        assert "Connection failed" in str(exc_info.value)
        assert exc_info.value.request == request


@pytest.mark.asyncio
async def test_http_transport_timeout(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test timeout error handling."""
    httpx_mock.add_exception(httpx.TimeoutException("Request timed out"))

    request = Request(
        uri="https://slow.example.com",
        method="GET",
    )

    async with http_transport:
        with pytest.raises(TransportTimeoutError) as exc_info:
            await http_transport.execute(request)

        assert "Request timed out" in str(exc_info.value)
        assert exc_info.value.request == request


@pytest.mark.asyncio
async def test_http_transport_streaming(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test HTTP streaming response."""
    content = b"chunk1\nchunk2\nchunk3\n"

    def stream_content() -> Generator[bytes, None, None]:
        for line in content.split(b"\n"):
            if line:
                yield line + b"\n"

    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/stream",
        status_code=200,
        stream=httpx.ByteStream(content),
    )

    request = Request(
        uri="https://api.example.com/stream",
        method="GET",
    )

    chunks = []
    async with http_transport:
        async for chunk in http_transport.stream(request):
            chunks.append(chunk)

    # Verify we got streaming chunks
    assert len(chunks) > 0
    assert b"".join(chunks) == content


@pytest.mark.asyncio
async def test_http_transport_context_manager(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test transport context manager behavior."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/test",
        json={"ok": True},
        status_code=200,
    )

    # Test that transport connects and disconnects properly
    assert http_transport._client is None

    async with http_transport as transport:
        assert transport._client is not None

        request = Request(uri="https://api.example.com/test", method="GET")
        response = await transport.execute(request)
        assert response.status == 200

    # Client should be closed after context exit
    assert http_transport._client is None


def test_http_transport_supports() -> None:
    """Test transport scheme support."""
    transport = HTTPTransport()

    from provide.foundation.transport.types import TransportType

    assert transport.supports(TransportType.HTTP)
    assert transport.supports(TransportType.HTTPS)
    assert not transport.supports(TransportType.WS)
    assert not transport.supports(TransportType.GRPC)


@pytest.mark.asyncio
async def test_http_transport_parameters(http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
    """Test HTTP request with parameters."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/search?q=python&limit=10",
        json={"results": ["item1", "item2"]},
        status_code=200,
    )

    request = Request(
        uri="https://api.example.com/search",
        method="GET",
        params={"q": "python", "limit": 10},
    )

    async with http_transport:
        response = await http_transport.execute(request)

    assert response.status == 200
    data = response.json()
    assert len(data["results"]) == 2


# 🧱🏗️🔚
