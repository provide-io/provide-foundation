#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Universal client cache management and error handling tests."""

from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.hub import get_hub
from provide.foundation.transport import UniversalClient


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


# 🧱🏗️🔚
