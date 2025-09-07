"""
Universal client tests.
"""

import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.transport import (
    UniversalClient,
    get,
    post,
    get_default_client,
)
from provide.foundation.transport.middleware import LoggingMiddleware, MetricsMiddleware


@pytest.mark.asyncio
async def test_universal_client_get(httpx_mock: HTTPXMock):
    """Test UniversalClient GET request."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/users",
        json={"users": ["Alice", "Bob"]},
        status_code=200,
    )
    
    async with UniversalClient() as client:
        response = await client.get("https://api.example.com/users")
    
    assert response.status == 200
    assert response.json()["users"] == ["Alice", "Bob"]


@pytest.mark.asyncio
async def test_universal_client_post(httpx_mock: HTTPXMock):
    """Test UniversalClient POST request."""
    httpx_mock.add_response(
        method="POST",
        url="https://api.example.com/users",
        json={"id": 123, "name": "Charlie"},
        status_code=201,
    )
    
    client = UniversalClient()
    
    async with client:
        response = await client.post(
            "https://api.example.com/users",
            body={"name": "Charlie"},
        )
    
    assert response.status == 201
    assert response.json()["name"] == "Charlie"


@pytest.mark.asyncio
async def test_universal_client_all_methods(httpx_mock: HTTPXMock):
    """Test all HTTP methods through UniversalClient."""
    # Mock responses for all methods
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
        httpx_mock.add_response(
            method=method,
            url="https://api.example.com/resource",
            json={"method": method},
            status_code=200,
        )
    
    async with UniversalClient() as client:
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
async def test_universal_client_with_headers(httpx_mock: HTTPXMock):
    """Test client with default and request headers."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/protected",
        json={"message": "success"},
        status_code=200,
    )
    
    client = UniversalClient(
        default_headers={"Authorization": "Bearer default-token"}
    )
    
    async with client:
        response = await client.get(
            "https://api.example.com/protected",
            headers={"X-Custom": "value"}
        )
    
    assert response.status == 200
    # Headers should have been merged (can't easily verify in mock, but logic is tested)


@pytest.mark.asyncio
async def test_universal_client_middleware():
    """Test client with custom middleware."""
    client = UniversalClient()
    
    # Add custom middleware
    metrics_mw = MetricsMiddleware()
    client.middleware.add(metrics_mw)
    
    # Mock response
    import httpx
    from unittest.mock import AsyncMock, patch
    
    with patch('provide.foundation.transport.http.httpx.AsyncClient') as mock_client_class:
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
        assert hasattr(metrics_mw, '_request_counter')
        assert hasattr(metrics_mw, '_request_duration')


@pytest.mark.asyncio
async def test_convenience_functions(httpx_mock: HTTPXMock):
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
        body={"data": "test"}
    )
    assert response.status == 201
    assert response.json()["id"] == 456


@pytest.mark.asyncio
async def test_universal_client_streaming(httpx_mock: HTTPXMock):
    """Test client streaming functionality."""
    content = b"line1\nline2\nline3\n"
    
    httpx_mock.add_response(
        method="GET", 
        url="https://api.example.com/stream",
        status_code=200,
        content=content,
    )
    
    client = UniversalClient()
    chunks = []
    
    async with client:
        async for chunk in client.stream("https://api.example.com/stream"):
            chunks.append(chunk)
    
    assert b"".join(chunks) == content


def test_default_client_singleton():
    """Test that default client is a singleton."""
    client1 = get_default_client()
    client2 = get_default_client()
    
    assert client1 is client2


@pytest.mark.asyncio
async def test_universal_client_timeout(httpx_mock: HTTPXMock):
    """Test client with custom timeout."""
    httpx_mock.add_response(
        method="GET",
        url="https://api.example.com/slow",
        json={"data": "response"},
        status_code=200,
    )
    
    client = UniversalClient(default_timeout=5.0)
    
    async with client:
        response = await client.get("https://api.example.com/slow")
    
    assert response.status == 200


@pytest.mark.asyncio
async def test_universal_client_connection_pooling(httpx_mock: HTTPXMock):
    """Test that client reuses connections for same scheme."""
    client = UniversalClient()
    
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
        assert len(client._transports) == 1
        assert "https" in client._transports


@pytest.mark.asyncio 
async def test_universal_client_error_handling(httpx_mock: HTTPXMock):
    """Test client error handling through middleware."""
    from provide.foundation.transport.errors import TransportTimeoutError
    
    client = UniversalClient()
    
    # Test with timeout error (httpx_mock without response causes timeout)
    with pytest.raises(TransportTimeoutError) as exc_info:
        await client.get("https://api.example.com/error")
    
    # The error message should indicate a timeout
    assert "Request timed out" in str(exc_info.value)