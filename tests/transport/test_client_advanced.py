#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Universal client advanced features tests - streaming, middleware, connection pooling, timeouts."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.hub import get_hub
from provide.foundation.transport import UniversalClient
from provide.foundation.transport.middleware import MetricsMiddleware
from provide.foundation.transport.types import HTTPMethod


@pytest.mark.asyncio
async def test_universal_client_middleware() -> None:
    """Test client with custom middleware."""
    client = UniversalClient(hub=get_hub())

    # Add custom middleware
    metrics_mw = MetricsMiddleware()
    client.middleware.add(metrics_mw)

    # Mock response
    from provide.testkit.mocking import AsyncMock, patch

    with patch("provide.foundation.transport.http.httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value = mock_client

        # Mock response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.content = b'{"test": true}'
        mock_response.reason_phrase = "OK"
        mock_response.http_version = "1.1"
        mock_response.encoding = "utf-8"
        mock_response.is_redirect = False
        mock_response.url = "https://api.example.com/test"

        mock_client.request.return_value = mock_response

        async with client:
            response = await client.get("https://api.example.com/test")

        assert response.status == 200

        # Check metrics middleware was used
        assert hasattr(metrics_mw, "_request_counter")
        assert hasattr(metrics_mw, "_request_duration")


@pytest.mark.asyncio
async def test_universal_client_streaming(httpx_mock: HTTPXMock) -> None:
    """Test client streaming functionality."""
    content = b"line1\nline2\nline3\n"

    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/stream",
        status_code=200,
        content=content,
    )

    client = UniversalClient(hub=get_hub())
    chunks = []

    async with client:
        async for chunk in client.stream("https://api.example.com/stream"):
            chunks.append(chunk)

    assert b"".join(chunks) == content


@pytest.mark.asyncio
async def test_universal_client_timeout(httpx_mock: HTTPXMock) -> None:
    """Test client with custom timeout."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/slow",
        json={"data": "response"},
        status_code=200,
    )

    client = UniversalClient(hub=get_hub(), default_timeout=5.0)

    async with client:
        response = await client.get("https://api.example.com/slow")

    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_connection_pooling(httpx_mock: HTTPXMock) -> None:
    """Test that client reuses connections for same scheme."""
    client = UniversalClient(hub=get_hub())

    # This tests the internal transport caching mechanism
    # Multiple requests to same scheme should reuse transport

    # Mock responses for both requests
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/test1",
        json={"ok": True},
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/test2",
        json={"ok": True},
        status_code=200,
    )

    async with client:
        # Make multiple requests
        await client.get("https://api.example.com/test1")
        await client.get("https://api.example.com/test2")

        # Should have created only one transport instance (check inside context)
        assert len(client._cache._transports) == 1
        assert "https" in client._cache._transports


@pytest.mark.asyncio
async def test_universal_client_request_metadata(httpx_mock: HTTPXMock) -> None:
    """Test client with additional request metadata."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/meta",
        json={"ok": True},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.request(
            "https://api.example.com/meta",
            method="GET",
            custom_key="custom_value",  # Extra kwargs become metadata
        )

    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_stream_with_method_enum(httpx_mock: HTTPXMock) -> None:
    """Test streaming with HTTPMethod enum."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/stream",
        content=b"streamed data",
        status_code=200,
    )

    client = UniversalClient(hub=get_hub())

    chunks = []
    async with client:
        async for chunk in client.stream("https://api.example.com/stream", method=HTTPMethod.POST):
            chunks.append(chunk)

    assert b"".join(chunks) == b"streamed data"


@pytest.mark.asyncio
async def test_universal_client_default_timeout_override(httpx_mock: HTTPXMock) -> None:
    """Test overriding default timeout on per-request basis."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/timeout",
        json={"ok": True},
        status_code=200,
    )

    client = UniversalClient(hub=get_hub(), default_timeout=10.0)

    async with client:
        # Override default timeout for this request
        response = await client.get("https://api.example.com/timeout", timeout=5.0)

    assert response.status == 200


# 🧱🏗️🔚
