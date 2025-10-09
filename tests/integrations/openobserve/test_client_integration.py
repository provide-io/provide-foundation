"""Integration tests for OpenObserve client.

This module contains integration tests that require a running OpenObserve instance.
Run with: pytest tests/integrations/openobserve/ --integration -v

Environment variables required (loaded via Foundation config):
    OPENOBSERVE_URL: OpenObserve instance URL
    OPENOBSERVE_USER: Username for authentication
    OPENOBSERVE_PASSWORD: Password for authentication
    OPENOBSERVE_ORG: Organization name (default: "default")
"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveConfigError,
    OpenObserveQueryError,
)
from provide.foundation.integrations.openobserve.models import StreamInfo


@pytest.mark.integration
class TestClientInitialization(FoundationTestCase):
    """Tests for OpenObserve client initialization."""

    def test_client_from_config(
        self,
        openobserve_config: OpenObserveConfig,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test creating client from Foundation config."""
        client = OpenObserveClient.from_config()

        assert client.url == openobserve_config.url
        assert client.username == openobserve_config.user
        assert client.organization == (openobserve_config.org or "default")
        assert client.timeout == 30  # default
        assert client.session is not None

    def test_client_direct_initialization(
        self,
        openobserve_config: OpenObserveConfig,
    ) -> None:
        """Test direct client initialization."""
        client = OpenObserveClient(
            url=openobserve_config.url or "http://localhost:5080/api/default",
            username=openobserve_config.user or "test@example.com",
            password=openobserve_config.password or "password",
            organization=openobserve_config.org or "default",
            timeout=60,
            max_retries=5,
        )

        assert client.url.endswith("/api/default") or "/api/" in client.url
        assert client.timeout == 60
        assert client.session is not None

    def test_client_url_normalization(self) -> None:
        """Test that client normalizes URLs correctly."""
        client = OpenObserveClient(
            url="http://localhost:5080/api/default/",  # Trailing slash
            username="user@example.com",
            password="password",
        )

        # Should strip trailing slash
        assert not client.url.endswith("/")


@pytest.mark.integration
class TestClientConnection(FoundationTestCase):
    """Tests for OpenObserve client connection."""

    def test_connection_test(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test connection testing method."""
        assert openobserve_client is not None

        result = openobserve_client.test_connection()

        assert result is True

    def test_connection_with_invalid_credentials(
        self,
        openobserve_config: OpenObserveConfig,
    ) -> None:
        """Test connection with invalid credentials."""
        if not openobserve_config.url:
            pytest.skip("OpenObserve URL not configured")

        client = OpenObserveClient(
            url=openobserve_config.url,
            username="invalid@example.com",
            password="wrongpassword",
            organization=openobserve_config.org or "default",
        )

        result = client.test_connection()

        # Should fail with invalid credentials
        assert result is False


@pytest.mark.integration
class TestListStreams(FoundationTestCase):
    """Tests for listing streams."""

    def test_list_streams(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test listing available streams."""
        assert openobserve_client is not None

        streams = openobserve_client.list_streams()

        # Should return a list (may be empty for new instance)
        assert isinstance(streams, list)
        # All items should be StreamInfo objects
        for stream in streams:
            assert isinstance(stream, StreamInfo)
            assert stream.name  # Should have a name

    def test_list_streams_returns_stream_info(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that list_streams returns properly formed StreamInfo objects."""
        assert openobserve_client is not None

        streams = openobserve_client.list_streams()

        if streams:  # If there are any streams
            stream = streams[0]
            # Check required fields
            assert hasattr(stream, "name")
            assert hasattr(stream, "storage_type")
            assert hasattr(stream, "stream_type")
            # Check stats fields exist (may be 0)
            assert hasattr(stream, "doc_count")
            assert hasattr(stream, "compressed_size")
            assert hasattr(stream, "original_size")


@pytest.mark.integration
class TestSearchHistory(FoundationTestCase):
    """Tests for search history functionality."""

    def test_get_search_history(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test getting search history."""
        assert openobserve_client is not None

        response = openobserve_client.get_search_history(size=10)

        # Should return SearchResponse
        assert hasattr(response, "hits")
        assert hasattr(response, "total")
        assert hasattr(response, "took")
        assert isinstance(response.hits, list)

    def test_get_search_history_with_stream_filter(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test getting search history filtered by stream."""
        assert openobserve_client is not None

        response = openobserve_client.get_search_history(
            stream_name=test_stream_name,
            size=5,
        )

        # Should return SearchResponse
        assert isinstance(response.hits, list)
        # Size parameter should be respected
        assert len(response.hits) <= 5

    def test_get_search_history_different_sizes(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test getting search history with different size parameters."""
        assert openobserve_client is not None

        # Test with different sizes
        for size in [1, 5, 50]:
            response = openobserve_client.get_search_history(size=size)
            # Returned hits should not exceed requested size
            assert len(response.hits) <= size


@pytest.mark.integration
class TestClientErrorHandling(FoundationTestCase):
    """Tests for client error handling."""

    def test_invalid_endpoint_raises_error(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that invalid endpoints raise appropriate errors."""
        assert openobserve_client is not None

        with pytest.raises(OpenObserveQueryError):
            # Try to make request to non-existent endpoint
            openobserve_client._make_request(
                method="GET",
                endpoint="nonexistent_endpoint_xyz",
            )

    def test_timeout_configuration(
        self,
        openobserve_config: OpenObserveConfig,
    ) -> None:
        """Test that timeout is properly configured."""
        if not openobserve_config.url:
            pytest.skip("OpenObserve URL not configured")

        client = OpenObserveClient(
            url=openobserve_config.url,
            username=openobserve_config.user or "user@example.com",
            password=openobserve_config.password or "password",
            timeout=5,  # Short timeout
        )

        assert client.timeout == 5

    def test_retry_configuration(
        self,
        openobserve_config: OpenObserveConfig,
    ) -> None:
        """Test that retry logic is properly configured."""
        if not openobserve_config.url:
            pytest.skip("OpenObserve URL not configured")

        client = OpenObserveClient(
            url=openobserve_config.url,
            username=openobserve_config.user or "user@example.com",
            password=openobserve_config.password or "password",
            max_retries=10,
        )

        # Verify session has retry adapter
        assert client.session is not None
        # Check that adapters are mounted
        assert "http://" in client.session.adapters
        assert "https://" in client.session.adapters


__all__ = [
    "TestClientConnection",
    "TestClientErrorHandling",
    "TestClientInitialization",
    "TestListStreams",
    "TestSearchHistory",
]
