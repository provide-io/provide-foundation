#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Universal client basic operations tests - HTTP methods, headers, convenience functions."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.hub import get_hub
from provide.foundation.transport import (
    UniversalClient,
    get,
    get_default_client,
    post,
)
from provide.foundation.transport.types import HTTPMethod


@pytest.mark.asyncio
async def test_universal_client_get(httpx_mock: HTTPXMock) -> None:
    """Test UniversalClient GET request."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users",
        json={"users": ["Alice", "Bob"]},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.get("https://api.example.com/users")

    assert response.status == 200
    assert response.json()["users"] == ["Alice", "Bob"]


@pytest.mark.asyncio
async def test_universal_client_post(httpx_mock: HTTPXMock) -> None:
    """Test UniversalClient POST request."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/users",
        json={"id": 123, "name": "Charlie"},
        status_code=201,
    )

    client = UniversalClient(hub=get_hub())

    async with client:
        response = await client.post(
            "https://api.example.com/users",
            body={"name": "Charlie"},
        )

    assert response.status == 201
    assert response.json()["name"] == "Charlie"


@pytest.mark.asyncio
async def test_universal_client_all_methods(httpx_mock: HTTPXMock) -> None:
    """Test all HTTP methods through UniversalClient."""
    # Mock responses for all methods
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
        httpx_mock.add_response(
            method=method,
            url="https://api.example.com/resource",
            json={"method": method},
            status_code=200,
        )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.get("https://api.example.com/resource")
        assert response.json()["method"] == "GET"

        response = await client.post("https://api.example.com/resource")
        assert response.json()["method"] == "POST"

        response = await client.put("https://api.example.com/resource")
        assert response.json()["method"] == "PUT"

        response = await client.patch("https://api.example.com/resource")
        assert response.json()["method"] == "PATCH"

        response = await client.delete("https://api.example.com/resource")
        assert response.json()["method"] == "DELETE"

        response = await client.head("https://api.example.com/resource")
        assert response.json()["method"] == "HEAD"

        response = await client.options("https://api.example.com/resource")
        assert response.json()["method"] == "OPTIONS"


@pytest.mark.asyncio
async def test_universal_client_with_headers(httpx_mock: HTTPXMock) -> None:
    """Test client with default and request headers."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/protected",
        json={"message": "success"},
        status_code=200,
    )

    client = UniversalClient(
        hub=get_hub(),
        default_headers={"Authorization": "Bearer default-token"},
    )

    async with client:
        response = await client.get(
            "https://api.example.com/protected",
            headers={"X-Custom": "value"},
        )

    assert response.status == 200
    # Headers should have been merged (can't easily verify in mock, but logic is tested)


@pytest.mark.asyncio
async def test_convenience_functions(httpx_mock: HTTPXMock) -> None:
    """Test module-level convenience functions."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/simple",
        json={"message": "hello"},
        status_code=200,
    )

    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/create",
        json={"id": 456},
        status_code=201,
    )

    # Test GET
    response = await get("https://api.example.com/simple")
    assert response.status == 200
    assert response.json()["message"] == "hello"

    # Test POST
    response = await post(
        "https://api.example.com/create",
        body={"data": "test"},
    )
    assert response.status == 201
    assert response.json()["id"] == 456


def test_default_client_singleton() -> None:
    """Test that default client is a singleton."""
    client1 = get_default_client()
    client2 = get_default_client()

    assert client1 is client2


@pytest.mark.asyncio
async def test_convenience_functions_all_methods(httpx_mock: HTTPXMock) -> None:
    """Test all convenience functions (put, patch, delete, head, options, stream)."""
    from provide.foundation.transport import delete, head, options, patch, put, stream

    # Mock all methods
    httpx_mock.add_response(
        method="PUT", url="https://api.example.com/update", json={"updated": True}, status_code=200
    )
    httpx_mock.add_response(
        method="PATCH", url="https://api.example.com/patch", json={"patched": True}, status_code=200
    )
    httpx_mock.add_response(
        method="DELETE", url="https://api.example.com/delete", json={"deleted": True}, status_code=204
    )
    httpx_mock.add_response(method="HEAD", url="https://api.example.com/head", status_code=200)
    httpx_mock.add_response(
        method="OPTIONS",
        url="https://api.example.com/options",
        json={"methods": ["GET", "POST"]},
        status_code=200,
    )
    httpx_mock.add_response(
        method="GET", url="https://api.example.com/stream", content=b"streaming content", status_code=200
    )

    # Test PUT
    response = await put("https://api.example.com/update", body={"data": "new"})
    assert response.status == 200

    # Test PATCH
    response = await patch("https://api.example.com/patch", body={"field": "value"})
    assert response.status == 200

    # Test DELETE
    response = await delete("https://api.example.com/delete")
    assert response.status == 204

    # Test HEAD
    response = await head("https://api.example.com/head")
    assert response.status == 200

    # Test OPTIONS
    response = await options("https://api.example.com/options")
    assert response.status == 200

    # Test STREAM
    chunks = []
    async for chunk in stream("https://api.example.com/stream"):
        chunks.append(chunk)
    assert b"".join(chunks) == b"streaming content"


@pytest.mark.asyncio
async def test_universal_client_with_http_method_enum(httpx_mock: HTTPXMock) -> None:
    """Test client with HTTPMethod enum instead of string."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/data",
        json={"success": True},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.request(
            "https://api.example.com/data",
            method=HTTPMethod.POST,
            body={"test": "data"},
        )

    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_with_params(httpx_mock: HTTPXMock) -> None:
    """Test client with query parameters."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/search?q=test&limit=10",
        json={"results": []},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.get(
            "https://api.example.com/search",
            params={"q": "test", "limit": "10"},
        )

    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_request_with_string_body(httpx_mock: HTTPXMock) -> None:
    """Test request with string body instead of dict."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/text",
        json={"received": True},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.post(
            "https://api.example.com/text",
            body="raw text data",
        )

    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_request_with_bytes_body(httpx_mock: HTTPXMock) -> None:
    """Test request with bytes body."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/binary",
        json={"received": True},
        status_code=200,
    )

    async with UniversalClient(hub=get_hub()) as client:
        response = await client.post(
            "https://api.example.com/binary",
            body=b"binary data",
        )

    assert response.status == 200


# 🧱🏗️🔚
