#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive HTTP transport tests for improved coverage.

This module adds tests for edge cases and missing coverage areas."""

from __future__ import annotations

import httpx
from provide.testkit.mocking import AsyncMock, patch
import pytest
from pytest_httpx import HTTPXMock

from provide.foundation.transport import (
    HTTPTransport,
    Request,
    TransportConnectionError,
    TransportTimeoutError,
)
from provide.foundation.transport.config import HTTPConfig
from provide.foundation.transport.types import TransportType


@pytest.fixture
def http_transport() -> HTTPTransport:
    """HTTP transport instance."""
    return HTTPTransport(config=HTTPConfig())


class TestClientNotConnected:
    """Tests for client not connected scenarios."""

    @pytest.mark.asyncio
    async def test_execute_without_client_raises_error(self) -> None:
        """Test execute when client is None after connect."""
        transport = HTTPTransport()

        # Manually set client to None after "connect" to trigger the check
        transport._client = None

        request = Request(uri="https://api.example.com/test", method="GET")

        # The execute method calls connect(), so we need to mock it
        with patch.object(transport, "connect", new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = None  # connect() sets _client but we'll override

            with pytest.raises(TransportConnectionError, match="HTTP client not connected"):
                await transport.execute(request)

    @pytest.mark.asyncio
    async def test_stream_without_client_raises_error(self) -> None:
        """Test stream when client is None after connect."""
        transport = HTTPTransport()
        transport._client = None

        request = Request(uri="https://api.example.com/stream", method="GET")

        with (
            patch.object(transport, "connect", new_callable=AsyncMock),
            pytest.raises(TransportConnectionError, match="HTTP client not connected"),
        ):
            async for _ in transport.stream(request):
                pass


class TestBodySerialization:
    """Tests for request body handling."""

    @pytest.mark.asyncio
    async def test_execute_with_string_body(
        self, http_transport: HTTPTransport, httpx_mock: HTTPXMock
    ) -> None:
        """Test execute with string body."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.example.com/text",
            status_code=200,
        )

        request = Request(
            uri="https://api.example.com/text",
            method="POST",
            body="plain text data",
        )

        async with http_transport:
            response = await http_transport.execute(request)

        assert response.status == 200

    @pytest.mark.asyncio
    async def test_execute_with_bytes_body(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test execute with bytes body."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.example.com/binary",
            status_code=200,
        )

        request = Request(
            uri="https://api.example.com/binary",
            method="POST",
            body=b"binary data",
        )

        async with http_transport:
            response = await http_transport.execute(request)

        assert response.status == 200

    @pytest.mark.asyncio
    async def test_execute_with_object_body(
        self, http_transport: HTTPTransport, httpx_mock: HTTPXMock
    ) -> None:
        """Test execute with object body (fallback to JSON)."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.example.com/obj",
            status_code=200,
        )

        # Use a list instead of dict to trigger the else branch
        request = Request(
            uri="https://api.example.com/obj",
            method="POST",
            body=["item1", "item2"],
        )

        async with http_transport:
            response = await http_transport.execute(request)

        assert response.status == 200


class TestExceptionHandling:
    """Tests for exception handling."""

    @pytest.mark.asyncio
    async def test_request_error_exception(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test httpx.RequestError handling."""
        httpx_mock.add_exception(httpx.RequestError("Generic request error"))

        request = Request(uri="https://api.example.com/test", method="GET")

        async with http_transport:
            with pytest.raises(TransportConnectionError, match="Request failed"):
                await http_transport.execute(request)

    @pytest.mark.asyncio
    async def test_unexpected_exception(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test handling of unexpected exceptions."""
        # Mock the client request to raise an unexpected exception
        request = Request(uri="https://api.example.com/test", method="GET")

        async with http_transport:
            with patch.object(http_transport._client, "request", side_effect=ValueError("Unexpected error")):
                with pytest.raises(TransportConnectionError, match="Unexpected error"):
                    await http_transport.execute(request)


class TestStreamExceptionHandling:
    """Tests for streaming exception handling."""

    @pytest.mark.asyncio
    async def test_stream_connection_error(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test stream ConnectError handling."""
        httpx_mock.add_exception(httpx.ConnectError("Stream connection failed"))

        request = Request(uri="https://api.example.com/stream", method="GET")

        async with http_transport:
            with pytest.raises(TransportConnectionError, match="Failed to connect"):
                async for _ in http_transport.stream(request):
                    pass

    @pytest.mark.asyncio
    async def test_stream_timeout_error(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test stream TimeoutException handling."""
        httpx_mock.add_exception(httpx.TimeoutException("Stream timed out"))

        request = Request(uri="https://api.example.com/stream", method="GET")

        async with http_transport:
            with pytest.raises(TransportTimeoutError, match="Stream timed out"):
                async for _ in http_transport.stream(request):
                    pass

    @pytest.mark.asyncio
    async def test_stream_request_error(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test stream RequestError handling."""
        httpx_mock.add_exception(httpx.RequestError("Stream request failed"))

        request = Request(uri="https://api.example.com/stream", method="GET")

        async with http_transport:
            with pytest.raises(TransportConnectionError, match="Stream failed"):
                async for _ in http_transport.stream(request):
                    pass

    @pytest.mark.asyncio
    async def test_stream_with_params(self, http_transport: HTTPTransport, httpx_mock: HTTPXMock) -> None:
        """Test streaming with query parameters."""
        content = b"streamed content"

        httpx_mock.add_response(
            method="GET",
            url="https://api.example.com/stream?limit=10&offset=0",
            status_code=200,
            stream=httpx.ByteStream(content),
        )

        request = Request(
            uri="https://api.example.com/stream",
            method="GET",
            params={"limit": 10, "offset": 0},
        )

        chunks = []
        async with http_transport:
            async for chunk in http_transport.stream(request):
                chunks.append(chunk)

        assert b"".join(chunks) == content


class TestStatusEmojis:
    """Tests for status code emoji selection."""

    def test_redirect_status_emoji(self) -> None:
        """Test redirect status codes (3xx) get correct emoji."""
        transport = HTTPTransport()

        # Test 301 Moved Permanently
        emoji = transport._get_status_emoji(301)
        assert emoji == "↩️"

        # Test 302 Found
        emoji = transport._get_status_emoji(302)
        assert emoji == "↩️"

        # Test 304 Not Modified
        emoji = transport._get_status_emoji(304)
        assert emoji == "↩️"

    def test_server_error_status_emoji(self) -> None:
        """Test server error status codes (5xx) get correct emoji."""
        transport = HTTPTransport()

        # Test 500 Internal Server Error
        emoji = transport._get_status_emoji(500)
        assert emoji == "❌"

        # Test 503 Service Unavailable
        emoji = transport._get_status_emoji(503)
        assert emoji == "❌"

    def test_unknown_status_emoji(self) -> None:
        """Test unknown status codes get question mark emoji."""
        transport = HTTPTransport()

        # Test status code outside standard ranges
        emoji = transport._get_status_emoji(600)
        assert emoji == "❓"

        emoji = transport._get_status_emoji(100)
        assert emoji == "❓"


class TestDisconnect:
    """Tests for disconnect logic."""

    @pytest.mark.asyncio
    async def test_disconnect_when_client_is_none(self) -> None:
        """Test disconnect when client is already None."""
        transport = HTTPTransport()
        assert transport._client is None

        # Should not raise
        await transport.disconnect()

        assert transport._client is None

    @pytest.mark.asyncio
    async def test_disconnect_closes_client(self) -> None:
        """Test disconnect properly closes client."""
        transport = HTTPTransport()

        # Connect
        await transport.connect()
        assert transport._client is not None

        # Disconnect
        await transport.disconnect()
        assert transport._client is None


class TestTransportRegistration:
    """Tests for HTTP transport registration."""

    def test_registration_guard_prevents_double_registration(self) -> None:
        """Test that registration guard prevents multiple registrations."""
        # Import the registration function
        from provide.foundation.transport.http import _register_http_transport

        # First registration should succeed (already done on module import)
        # Second call should be guarded
        _register_http_transport()  # Should return early due to guard

        # Verify transport is registered (get_transport returns instance, not class)
        from provide.foundation.transport.registry import get_transport

        transport = get_transport(TransportType.HTTP)
        assert isinstance(transport, HTTPTransport)

    def test_registration_flag_set_after_registration(self) -> None:
        """Test that registration flag is set after successful registration."""
        import provide.foundation.transport.http as http_module

        # The flag should be True after module import (registration happens on import)
        assert http_module._http_transport_registered


class TestRequestTimeout:
    """Tests for custom request timeout."""

    @pytest.mark.asyncio
    async def test_execute_with_custom_timeout(
        self, http_transport: HTTPTransport, httpx_mock: HTTPXMock
    ) -> None:
        """Test execute with custom timeout in request."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.example.com/slow",
            status_code=200,
        )

        request = Request(
            uri="https://api.example.com/slow",
            method="GET",
            timeout=60.0,  # Custom timeout
        )

        async with http_transport:
            response = await http_transport.execute(request)

        assert response.status == 200

    @pytest.mark.asyncio
    async def test_stream_with_custom_timeout(
        self, http_transport: HTTPTransport, httpx_mock: HTTPXMock
    ) -> None:
        """Test stream with custom timeout in request."""
        content = b"slow stream content"

        httpx_mock.add_response(
            method="GET",
            url="https://api.example.com/slow-stream",
            status_code=200,
            stream=httpx.ByteStream(content),
        )

        request = Request(
            uri="https://api.example.com/slow-stream",
            method="GET",
            timeout=120.0,  # Custom timeout
        )

        chunks = []
        async with http_transport:
            async for chunk in http_transport.stream(request):
                chunks.append(chunk)

        assert b"".join(chunks) == content


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
