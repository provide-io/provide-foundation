#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for OpenObserve search operations.

This module contains integration tests that require a running OpenObserve instance.
Run with: pytest tests/integrations/openobserve/ -m integration -v

Environment variables required (loaded via Foundation config):
    OPENOBSERVE_URL: OpenObserve instance URL
    OPENOBSERVE_USER: Username for authentication
    OPENOBSERVE_PASSWORD: Password for authentication
    OPENOBSERVE_STREAM: Stream name (default: "default")"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.search import (
    _sanitize_log_level,
    _sanitize_service_name,
    _sanitize_stream_name,
    _sanitize_trace_id,
    aggregate_by_level,
    get_current_trace_logs,
    search_by_level,
    search_by_service,
    search_by_trace_id,
    search_errors,
    search_logs,
)


class TestSanitizationFunctions(FoundationTestCase):
    """Unit tests for input sanitization functions."""

    def test_sanitize_stream_name_valid(self) -> None:
        """Test stream name sanitization with valid inputs."""
        assert _sanitize_stream_name("valid_stream123") == "valid_stream123"
        assert _sanitize_stream_name("test") == "test"
        assert _sanitize_stream_name("default") == "default"

    def test_sanitize_stream_name_invalid(self) -> None:
        """Test stream name sanitization rejects invalid inputs."""
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("invalid-stream")  # Hyphens not allowed
        with pytest.raises(ValueError, match="Invalid stream name"):
            _sanitize_stream_name("stream; DROP TABLE")  # SQL injection attempt

    def test_sanitize_trace_id_valid(self) -> None:
        """Test trace ID sanitization with valid inputs."""
        assert _sanitize_trace_id("abc123def456") == "abc123def456"
        assert _sanitize_trace_id("ABC123DEF456") == "ABC123DEF456"
        assert _sanitize_trace_id("a1b2-c3d4-e5f6") == "a1b2-c3d4-e5f6"  # UUID format

    def test_sanitize_trace_id_invalid(self) -> None:
        """Test trace ID sanitization rejects invalid inputs."""
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("invalid trace")  # Spaces not allowed
        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _sanitize_trace_id("trace'; DROP")  # SQL injection attempt

    def test_sanitize_log_level_valid(self) -> None:
        """Test log level sanitization with valid inputs."""
        assert _sanitize_log_level("ERROR") == "ERROR"
        assert _sanitize_log_level("WARNING") == "WARNING"
        assert _sanitize_log_level("INFO") == "INFO"
        assert _sanitize_log_level("DEBUG") == "DEBUG"
        assert _sanitize_log_level("TRACE") == "TRACE"
        assert _sanitize_log_level("CRITICAL") == "CRITICAL"

    def test_sanitize_log_level_invalid(self) -> None:
        """Test log level sanitization rejects invalid inputs."""
        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("INVALID")
        with pytest.raises(ValueError, match="Invalid log level"):
            _sanitize_log_level("ERROR'; DROP")  # SQL injection attempt

    def test_sanitize_service_name_valid(self) -> None:
        """Test service name sanitization with valid inputs."""
        assert _sanitize_service_name("my-service") == "my-service"
        assert _sanitize_service_name("service_123") == "service_123"
        assert _sanitize_service_name("api.gateway") == "api.gateway"

    def test_sanitize_service_name_invalid(self) -> None:
        """Test service name sanitization rejects invalid inputs."""
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("service;DROP")  # SQL injection attempt
        with pytest.raises(ValueError, match="Invalid service name"):
            _sanitize_service_name("service with spaces")  # Spaces not allowed


@pytest.mark.integration
class TestSearchLogs(FoundationTestCase):
    """Integration tests for basic search functionality."""

    async def test_search_logs_basic(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test basic log search with SQL query."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name} LIMIT 10"
        response = await search_logs(sql=sql, client=openobserve_client)

        assert hasattr(response, "hits")
        assert hasattr(response, "total")
        assert isinstance(response.hits, list)

    async def test_search_logs_with_time_range(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test search with time range parameters."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name}"
        response = await search_logs(
            sql=sql,
            start_time="-1h",
            end_time="now",
            size=5,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        assert len(response.hits) <= 5  # Respects size parameter

    async def test_search_logs_creates_client_if_none(
        self,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that search_logs creates client if not provided."""
        sql = "SELECT * FROM default LIMIT 1"

        # Should create client from config
        response = await search_logs(sql=sql)

        assert isinstance(response.hits, list)


@pytest.mark.integration
class TestSearchByTraceId(FoundationTestCase):
    """Integration tests for trace ID search."""

    async def test_search_by_trace_id(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching by trace ID."""
        assert openobserve_client is not None

        # Use a sample trace ID (may not exist in empty instance)
        trace_id = "abc123def456789"

        response = await search_by_trace_id(
            trace_id=trace_id,
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        # Results may be empty if trace_id doesn't exist

    async def test_search_by_trace_id_with_uuid(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching by UUID-format trace ID."""
        assert openobserve_client is not None

        # UUID format trace ID
        trace_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

        response = await search_by_trace_id(
            trace_id=trace_id,
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)


@pytest.mark.integration
class TestSearchByLevel(FoundationTestCase):
    """Integration tests for log level search."""

    async def test_search_by_level_error(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching by ERROR level."""
        assert openobserve_client is not None

        response = await search_by_level(
            level="ERROR",
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        # All results should have ERROR level (if any results exist)
        for hit in response.hits:
            if "level" in hit:
                assert hit["level"] == "ERROR"

    async def test_search_by_level_with_time_range(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching by level with time range."""
        assert openobserve_client is not None

        response = await search_by_level(
            level="INFO",
            stream=test_stream_name,
            start_time="-30m",
            end_time="now",
            size=10,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        assert len(response.hits) <= 10


@pytest.mark.integration
class TestSearchErrors(FoundationTestCase):
    """Integration tests for error search."""

    async def test_search_errors(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching for error logs."""
        assert openobserve_client is not None

        response = await search_errors(
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        # All results should be ERROR level
        for hit in response.hits:
            if "level" in hit:
                assert hit["level"] == "ERROR"

    async def test_search_errors_with_params(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching for errors with additional parameters."""
        assert openobserve_client is not None

        response = await search_errors(
            stream=test_stream_name,
            start_time="-1h",
            size=5,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        assert len(response.hits) <= 5


@pytest.mark.integration
class TestSearchByService(FoundationTestCase):
    """Integration tests for service name search."""

    async def test_search_by_service(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test searching by service name."""
        assert openobserve_client is not None

        service_name = "test-service"

        response = await search_by_service(
            service=service_name,
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(response.hits, list)
        # All results should have matching service_name (if any results exist)
        for hit in response.hits:
            if "service_name" in hit:
                assert hit["service_name"] == service_name


@pytest.mark.integration
class TestAggregatByLevel(FoundationTestCase):
    """Integration tests for level aggregation."""

    async def test_aggregate_by_level(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test aggregating log counts by level."""
        assert openobserve_client is not None

        result = await aggregate_by_level(
            stream=test_stream_name,
            client=openobserve_client,
        )

        assert isinstance(result, dict)
        # All values should be integers
        for level, count in result.items():
            assert isinstance(level, str)
            assert isinstance(count, int)
            assert count >= 0

    async def test_aggregate_by_level_with_time_range(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test aggregating by level with time range."""
        assert openobserve_client is not None

        result = await aggregate_by_level(
            stream=test_stream_name,
            start_time="-1h",
            end_time="now",
            client=openobserve_client,
        )

        assert isinstance(result, dict)


@pytest.mark.integration
class TestGetCurrentTraceLogs(FoundationTestCase):
    """Integration tests for current trace log retrieval."""

    async def test_get_current_trace_logs_no_active_trace(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test getting current trace logs when no trace is active."""
        assert openobserve_client is not None

        result = await get_current_trace_logs(
            stream=test_stream_name,
            client=openobserve_client,
        )

        # Should return None when no active trace
        assert result is None or hasattr(result, "hits")


__all__ = [
    "TestAggregatByLevel",
    "TestGetCurrentTraceLogs",
    "TestSanitizationFunctions",
    "TestSearchByLevel",
    "TestSearchByService",
    "TestSearchByTraceId",
    "TestSearchErrors",
    "TestSearchLogs",
]

# 🧱🏗️🔚
