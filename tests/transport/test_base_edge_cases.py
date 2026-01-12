#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Edge case tests for transport base classes and types."""

from __future__ import annotations

import json
from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock
import pytest

from provide.foundation.transport.base import Request, Response, TransportBase
from provide.foundation.transport.errors import HTTPResponseError
from provide.foundation.transport.types import TransportType


class TestRequestEdgeCases(FoundationTestCase):
    """Test edge cases for Request class."""

    def test_transport_type_unknown_scheme(self) -> None:
        """Test unknown scheme defaults to HTTP."""
        request = Request(uri="ftp://example.com/file")
        assert request.transport_type == TransportType.HTTP

    def test_transport_type_no_scheme(self) -> None:
        """Test malformed URI without scheme."""
        request = Request(uri="example.com/path")
        # Should handle gracefully and default to HTTP
        assert request.transport_type == TransportType.HTTP

    def test_base_url_malformed_uri(self) -> None:
        """Test base_url extraction with malformed URI."""
        # URI with fewer than 3 parts
        request = Request(uri="http://")
        assert request.base_url == "http://"

    def test_base_url_simple_uri(self) -> None:
        """Test base_url extraction with simple URI."""
        request = Request(uri="example.com")
        assert request.base_url == "example.com"

    def test_base_url_complex_path(self) -> None:
        """Test base_url extraction ignores path components."""
        request = Request(uri="https://api.example.com/v1/users/123?active=true")
        assert request.base_url == "https://api.example.com"


class TestResponseEdgeCases(FoundationTestCase):
    """Test edge cases for Response class."""

    def test_json_with_bytes_body(self) -> None:
        """Test JSON parsing from bytes body."""
        data = {"key": "value", "number": 42}
        json_bytes = json.dumps(data).encode("utf-8")
        response = Response(status=200, body=json_bytes)

        result = response.json()
        assert result == data

    def test_json_with_string_body(self) -> None:
        """Test JSON parsing from string body."""
        data = {"key": "value", "number": 42}
        json_str = json.dumps(data)
        response = Response(status=200, body=json_str)

        result = response.json()
        assert result == data

    def test_json_with_invalid_body_type(self) -> None:
        """Test JSON parsing with non-string/bytes body."""
        response = Response(status=200, body=123)  # Invalid type

        with pytest.raises(ValueError, match="Response body is not JSON-parseable"):
            response.json()

    def test_json_with_none_body(self) -> None:
        """Test JSON parsing with None body."""
        response = Response(status=200, body=None)

        with pytest.raises(ValueError, match="Response body is not JSON-parseable"):
            response.json()

    def test_text_with_bytes_body(self) -> None:
        """Test text extraction from bytes body."""
        text_bytes = "Hello, 世界".encode()
        response = Response(status=200, body=text_bytes)

        assert response.text == "Hello, 世界"

    def test_text_with_string_body(self) -> None:
        """Test text extraction from string body."""
        response = Response(status=200, body="Hello, World!")
        assert response.text == "Hello, World!"

    def test_text_with_none_body(self) -> None:
        """Test text extraction with None body."""
        response = Response(status=200, body=None)
        assert response.text == ""

    def test_text_with_numeric_body(self) -> None:
        """Test text extraction with numeric body."""
        response = Response(status=200, body=42)
        assert response.text == "42"

    def test_raise_for_status_success(self) -> None:
        """Test raise_for_status with successful status codes."""
        for status in [200, 201, 204, 299]:
            response = Response(status=status)
            # Should not raise
            response.raise_for_status()

    def test_raise_for_status_client_error(self) -> None:
        """Test raise_for_status with client error status."""
        response = Response(status=404, body="Not Found")

        with pytest.raises(HTTPResponseError) as exc_info:
            response.raise_for_status()

        error = exc_info.value
        assert error.status_code == 404
        assert error.response is response
        assert "Request failed with status 404" in str(error)

    def test_raise_for_status_server_error(self) -> None:
        """Test raise_for_status with server error status."""
        response = Response(status=500, body="Internal Server Error")

        with pytest.raises(HTTPResponseError) as exc_info:
            response.raise_for_status()

        error = exc_info.value
        assert error.status_code == 500
        assert error.response is response

    def test_is_success_boundary_cases(self) -> None:
        """Test is_success with boundary status codes."""
        # Edge cases around success range
        assert not Response(status=199).is_success()  # Just below success
        assert Response(status=200).is_success()  # Start of success
        assert Response(status=299).is_success()  # End of success
        assert not Response(status=300).is_success()  # Just above success


class TestTransportBaseEdgeCases(FoundationTestCase):
    """Test edge cases for TransportBase abstract class."""

    class MockTransport(TransportBase):
        """Mock transport implementation for testing."""

        async def execute(self, request: Request) -> Response:
            return Response(status=200, body="OK")

        def supports(self, transport_type: TransportType) -> bool:
            return transport_type == TransportType.HTTP

    def test_transport_base_initialization(self) -> None:
        """Test TransportBase creates logger correctly."""
        transport = self.MockTransport()
        assert transport._logger is not None
        # Logger name should contain the class name somehow
        assert hasattr(transport._logger, "name")

    async def test_transport_base_connect_default(self) -> None:
        """Test default connect implementation."""
        transport = self.MockTransport()
        # Should complete without error
        await transport.connect()

    async def test_transport_base_disconnect_default(self) -> None:
        """Test default disconnect implementation."""
        transport = self.MockTransport()
        # Should complete without error
        await transport.disconnect()

    async def test_transport_base_context_manager(self) -> None:
        """Test TransportBase context manager functionality."""
        transport = self.MockTransport()

        # Mock the connect/disconnect methods to verify they're called
        transport.connect = AsyncMock()
        transport.disconnect = AsyncMock()

        async with transport as ctx_transport:
            assert ctx_transport is transport
            transport.connect.assert_called_once()

        transport.disconnect.assert_called_once()

    async def test_transport_base_context_manager_with_exception(self) -> Never:
        """Test TransportBase context manager handles exceptions."""
        transport = self.MockTransport()

        transport.connect = AsyncMock()
        transport.disconnect = AsyncMock()

        with pytest.raises(ValueError):
            async with transport:
                raise ValueError("Test exception")

        # Disconnect should still be called even with exception
        transport.connect.assert_called_once()
        transport.disconnect.assert_called_once()


# 🧱🏗️🔚
