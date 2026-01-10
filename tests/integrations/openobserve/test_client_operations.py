#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve client operations with mocked transport.

This module tests search, list streams, and connection testing operations.
Run with: pytest tests/integrations/openobserve/test_client_operations.py -v"""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConnectionError,
    OpenObserveQueryError,
)
from provide.foundation.integrations.openobserve.models import SearchResponse, StreamInfo
from provide.foundation.transport.errors import (
    TransportConnectionError,
    TransportError,
    TransportTimeoutError,
)


class MockResponse:
    """Mock response object for testing."""

    def __init__(
        self,
        status: int = 200,
        body: bytes | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> None:
        self.status = status
        self.body = body or b"{}"
        self._json_data = json_data or {}

    def is_success(self) -> bool:
        """Check if response is successful."""
        return 200 <= self.status < 300

    def json(self) -> dict[str, Any]:
        """Return JSON data."""
        return self._json_data


class TestMakeRequest(FoundationTestCase):
    """Tests for _make_request method."""

    async def test_make_request_success(self) -> None:
        """Test successful request."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(
            status=200,
            body=b'{"result": "success"}',
            json_data={"result": "success"},
        )

        # Mock the _client object
        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client._make_request(
            method="GET",
            endpoint="streams",
        )

        assert result == {"result": "success"}
        mock_client.request.assert_called_once()

    async def test_make_request_empty_response(self) -> None:
        """Test handling empty response body."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(status=200, body=b"")

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client._make_request(
            method="GET",
            endpoint="streams",
        )

        assert result == {}

    async def test_make_request_connection_error(self) -> None:
        """Test handling TransportConnectionError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=TransportConnectionError("Connection refused"))
        client._client = mock_client

        with pytest.raises(OpenObserveConnectionError, match="Failed to connect"):
            await client._make_request(method="GET", endpoint="streams")

    async def test_make_request_timeout_error(self) -> None:
        """Test handling TransportTimeoutError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=TransportTimeoutError("Request timed out"))
        client._client = mock_client

        with pytest.raises(OpenObserveConnectionError, match="Request timed out"):
            await client._make_request(method="GET", endpoint="streams")

    async def test_make_request_transport_error(self) -> None:
        """Test handling generic TransportError."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=TransportError("Transport failed"))
        client._client = mock_client

        with pytest.raises(OpenObserveQueryError, match="Transport error"):
            await client._make_request(method="GET", endpoint="streams")

    async def test_make_request_unexpected_error(self) -> None:
        """Test handling unexpected errors."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=ValueError("Unexpected error"))
        client._client = mock_client

        with pytest.raises(OpenObserveQueryError, match="Unexpected error"):
            await client._make_request(method="GET", endpoint="streams")

    async def test_make_request_reraises_openobserve_errors(self) -> None:
        """Test that OpenObserve errors are re-raised."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(status=401)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        with pytest.raises(OpenObserveConnectionError, match="Authentication failed"):
            await client._make_request(method="GET", endpoint="streams")


class TestSearch(FoundationTestCase):
    """Tests for search method."""

    async def test_search_basic(self) -> None:
        """Test basic search query."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response_data = {
            "took": 10,
            "hits": [{"message": "log entry"}],
            "total": 1,
        }

        mock_response = MockResponse(status=200, json_data=mock_response_data)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client.search(sql="SELECT * FROM logs")

        assert isinstance(result, SearchResponse)
        assert result.took == 10
        assert len(result.hits) == 1

    async def test_search_error_in_response(self) -> None:
        """Test handling error in search response."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(
            status=200,
            json_data={"error": "Invalid SQL syntax"},
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        with pytest.raises(OpenObserveQueryError, match="Invalid SQL syntax"):
            await client.search(sql="SELECT * INVALID")

    async def test_search_with_function_errors(self) -> None:
        """Test search with function errors in response."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(
            status=200,
            json_data={
                "took": 10,
                "hits": [],
                "total": 0,
                "function_error": ["Function warning 1", "Function warning 2"],
            },
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client.search(sql="SELECT * FROM logs")

        # Should still return results but log warnings
        assert isinstance(result, SearchResponse)
        assert result.function_error == ["Function warning 1", "Function warning 2"]


class TestListStreams(FoundationTestCase):
    """Tests for list_streams method."""

    async def test_list_streams_success(self) -> None:
        """Test listing streams successfully."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(
            status=200,
            json_data={
                "logs": [
                    {"name": "stream1", "storage_type": "disk", "stream_type": "logs"},
                    {"name": "stream2", "storage_type": "disk", "stream_type": "logs"},
                ],
            },
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        streams = await client.list_streams()

        assert len(streams) == 2
        assert all(isinstance(s, StreamInfo) for s in streams)
        assert streams[0].name == "stream1"
        assert streams[1].name == "stream2"

    async def test_list_streams_empty(self) -> None:
        """Test listing streams when none exist."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(status=200, json_data={})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        streams = await client.list_streams()

        assert streams == []


class TestGetSearchHistory(FoundationTestCase):
    """Tests for get_search_history method."""

    async def test_get_search_history_basic(self) -> None:
        """Test getting search history."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(
            status=200,
            json_data={"took": 5, "hits": [], "total": 0},
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client.get_search_history()

        assert isinstance(result, SearchResponse)


class TestConnectionTest(FoundationTestCase):
    """Tests for test_connection method."""

    async def test_connection_success(self) -> None:
        """Test successful connection test."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(status=200, json_data={})

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        result = await client.test_connection()

        assert result is True

    async def test_connection_failure(self) -> None:
        """Test connection test failure with @resilient decorator."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(side_effect=TransportConnectionError("Connection refused"))
        client._client = mock_client

        # The @resilient decorator should catch the exception and return fallback value
        result = await client.test_connection()

        assert result is False

    async def test_connection_auth_failure(self) -> None:
        """Test connection test with auth failure."""
        client = OpenObserveClient(
            url="http://localhost:5080",
            username="test@example.com",
            password="password",
        )

        mock_response = MockResponse(status=401)

        mock_client = AsyncMock()
        mock_client.request = AsyncMock(return_value=mock_response)
        client._client = mock_client

        # The @resilient decorator should catch the exception and return fallback value
        result = await client.test_connection()

        assert result is False


__all__ = [
    "TestConnectionTest",
    "TestGetSearchHistory",
    "TestListStreams",
    "TestMakeRequest",
    "TestSearch",
]

# 🧱🏗️🔚
