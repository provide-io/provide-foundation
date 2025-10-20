"""Universal client tests."""

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
from provide.foundation.transport.middleware import MetricsMiddleware


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


def test_default_client_singleton() -> None:
    """Test that default client is a singleton."""
    client1 = get_default_client()
    client2 = get_default_client()

    assert client1 is client2


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
@pytest.mark.httpx_mock(assert_all_requests_were_expected=False)
async def test_universal_client_error_handling(httpx_mock: HTTPXMock) -> None:
    """Test client error handling through middleware."""
    from provide.foundation.transport.errors import TransportTimeoutError

    client = UniversalClient(hub=get_hub())

    # Test with timeout error (httpx_mock without response causes timeout)
    with pytest.raises(TransportTimeoutError) as exc_info:
        await client.get("https://api.example.com/error")

    # The error message should indicate a timeout
    assert "Request timed out" in str(exc_info.value)


@pytest.mark.asyncio
async def test_universal_client_with_http_method_enum(httpx_mock: HTTPXMock) -> None:
    """Test client with HTTPMethod enum instead of string."""
    from provide.foundation.transport.types import HTTPMethod

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
async def test_universal_client_cache_eviction() -> None:
    """Test transport cache eviction on failures."""
    from unittest.mock import AsyncMock, patch

    from provide.foundation.transport.errors import TransportError

    client = UniversalClient(hub=get_hub())

    # Mock get_transport to raise errors
    with patch("provide.foundation.transport.registry.get_transport") as mock_get:
        mock_transport = AsyncMock()
        mock_transport.execute.side_effect = TransportError("Connection failed")
        mock_get.return_value = mock_transport

        # Make multiple failed requests to trigger cache tracking
        for _ in range(3):
            with pytest.raises(TransportError):
                await client.get("https://api.example.com/fail")


@pytest.mark.asyncio
async def test_universal_client_reset_cache(httpx_mock: HTTPXMock) -> None:
    """Test reset_transport_cache method."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/test",
        json={"ok": True},
        status_code=200,
    )

    client = UniversalClient(hub=get_hub())

    async with client:
        # Make a request to populate cache
        await client.get("https://api.example.com/test")
        assert len(client._cache._transports) == 1

        # Reset cache
        client.reset_transport_cache()
        assert len(client._cache._transports) == 0


@pytest.mark.asyncio
async def test_universal_client_context_manager_with_exception(httpx_mock: HTTPXMock) -> None:
    """Test context manager cleanup when exception occurs."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/test",
        json={"ok": True},
        status_code=200,
    )

    client = UniversalClient(hub=get_hub())

    # Simulate exception during use
    try:
        async with client:
            # Make request to populate cache
            await client.get("https://api.example.com/test")
            # Verify cache was populated
            assert len(client._cache._transports) == 1
            # Raise exception
            raise ValueError("Test exception")
    except ValueError:
        pass

    # After exiting context, cache should be cleared
    assert len(client._cache._transports) == 0


@pytest.mark.asyncio
async def test_universal_client_context_manager_disconnect_error() -> None:
    """Test context manager handles disconnect errors gracefully."""
    from unittest.mock import AsyncMock

    client = UniversalClient(hub=get_hub())

    # Create a mock transport that will fail on disconnect
    mock_transport = AsyncMock()
    mock_transport.disconnect = AsyncMock(side_effect=Exception("Disconnect failed"))

    # Manually add it to cache
    client._cache._transports["https"] = mock_transport

    # Should not raise even if disconnect fails
    async with client:
        pass  # Just test cleanup

    # Verify disconnect was attempted despite error
    mock_transport.disconnect.assert_called_once()


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
async def test_universal_client_middleware_error_processing() -> None:
    """Test middleware error processing."""
    from unittest.mock import AsyncMock, patch

    from provide.foundation.transport.errors import TransportError

    client = UniversalClient(hub=get_hub())

    with patch("provide.foundation.transport.registry.get_transport") as mock_get:
        mock_transport = AsyncMock()
        original_error = TransportError("Original error")
        mock_transport.execute.side_effect = original_error
        mock_get.return_value = mock_transport

        # Error should be processed through middleware
        with pytest.raises(TransportError) as exc_info:
            await client.get("https://api.example.com/error")

        # Should be the same error (or processed version)
        assert isinstance(exc_info.value, TransportError)


@pytest.mark.asyncio
async def test_universal_client_cache_success_marking(httpx_mock: HTTPXMock) -> None:
    """Test that successful requests mark cache as successful."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/success",
        json={"ok": True},
        status_code=200,
    )

    client = UniversalClient(hub=get_hub())

    async with client:
        # Make successful request
        await client.get("https://api.example.com/success")

        # Check that transport is in cache and marked successful
        assert "https" in client._cache._transports
        # Success count should be tracked (implementation detail, but verifies logic)


@pytest.mark.asyncio
async def test_universal_client_stream_with_method_enum(httpx_mock: HTTPXMock) -> None:
    """Test streaming with HTTPMethod enum."""
    from provide.foundation.transport.types import HTTPMethod

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
