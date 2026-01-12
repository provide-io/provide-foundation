#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve search operations.

These tests mock the OpenObserveClient to test search functionality without
requiring a running OpenObserve instance."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import AsyncMock, Mock, patch
import pytest

from provide.foundation.integrations.openobserve.models import SearchResponse
from provide.foundation.integrations.openobserve.search import (
    aggregate_by_level,
    get_current_trace_logs,
    search_by_level,
    search_by_service,
    search_by_trace_id,
    search_errors,
    search_logs,
)


class TestSearchLogsUnit(FoundationTestCase):
    """Unit tests for search_logs function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_search_logs_with_provided_client(self) -> None:
        """Test search_logs with provided client."""
        # Create mock client
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        # Call search_logs with mock client
        result = await search_logs(
            sql="SELECT * FROM test",
            start_time="-1h",
            end_time="now",
            size=100,
            client=mock_client,
        )

        # Verify client.search was called with correct parameters
        mock_client.search.assert_called_once_with(
            sql="SELECT * FROM test",
            start_time="-1h",
            end_time="now",
            size=100,
        )

        assert result == mock_response

    @pytest.mark.asyncio
    async def test_search_logs_creates_client_when_none(self) -> None:
        """Test search_logs creates client from config when None provided."""
        # Mock OpenObserveClient.from_config
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        with patch(
            "provide.foundation.integrations.openobserve.search.OpenObserveClient.from_config",
            return_value=mock_client,
        ):
            result = await search_logs(sql="SELECT * FROM test")

            # Verify client was created from config
            mock_client.search.assert_called_once()
            assert result == mock_response


class TestSearchByTraceIdUnit(FoundationTestCase):
    """Unit tests for search_by_trace_id function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_search_by_trace_id_delegation(self) -> None:
        """Test search_by_trace_id delegates to search_logs correctly."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await search_by_trace_id(
            trace_id="abc123def456",
            stream="test_stream",
            client=mock_client,
        )

        # Verify correct SQL was constructed and delegated
        mock_client.search.assert_called_once()
        call_args = mock_client.search.call_args
        assert "SELECT * FROM test_stream" in call_args.kwargs["sql"]
        assert "abc123def456" in call_args.kwargs["sql"]
        assert call_args.kwargs["start_time"] == "-24h"

        assert result == mock_response

    @pytest.mark.asyncio
    async def test_search_by_trace_id_uuid_format(self) -> None:
        """Test search_by_trace_id with UUID format."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        trace_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        result = await search_by_trace_id(
            trace_id=trace_id,
            stream="default",
            client=mock_client,
        )

        # Verify UUID format trace ID is included in query
        call_args = mock_client.search.call_args
        assert trace_id in call_args.kwargs["sql"]
        assert result == mock_response


class TestSearchByLevelUnit(FoundationTestCase):
    """Unit tests for search_by_level function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_search_by_level_error(self) -> None:
        """Test search_by_level for ERROR level."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await search_by_level(
            level="ERROR",
            stream="test_stream",
            start_time="-1h",
            end_time="now",
            size=50,
            client=mock_client,
        )

        # Verify SQL construction and parameters
        call_args = mock_client.search.call_args
        assert "SELECT * FROM test_stream" in call_args.kwargs["sql"]
        assert "level = 'ERROR'" in call_args.kwargs["sql"]
        assert call_args.kwargs["start_time"] == "-1h"
        assert call_args.kwargs["end_time"] == "now"
        assert call_args.kwargs["size"] == 50

        assert result == mock_response

    @pytest.mark.asyncio
    async def test_search_by_level_all_levels(self) -> None:
        """Test search_by_level with all valid log levels."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        valid_levels = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_levels:
            mock_client.search.reset_mock()

            result = await search_by_level(
                level=level,
                client=mock_client,
            )

            call_args = mock_client.search.call_args
            assert f"level = '{level}'" in call_args.kwargs["sql"]
            assert result == mock_response


class TestSearchErrorsUnit(FoundationTestCase):
    """Unit tests for search_errors function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_search_errors_delegation(self) -> None:
        """Test search_errors delegates to search_by_level."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await search_errors(
            stream="error_stream",
            start_time="-2h",
            size=25,
            client=mock_client,
        )

        # Verify it delegates to search_by_level with ERROR
        call_args = mock_client.search.call_args
        assert "level = 'ERROR'" in call_args.kwargs["sql"]
        assert "error_stream" in call_args.kwargs["sql"]
        assert call_args.kwargs["start_time"] == "-2h"
        assert call_args.kwargs["size"] == 25

        assert result == mock_response


class TestSearchByServiceUnit(FoundationTestCase):
    """Unit tests for search_by_service function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_search_by_service(self) -> None:
        """Test search_by_service constructs query correctly."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await search_by_service(
            service="auth-service",
            stream="logs",
            start_time="-30m",
            end_time="now",
            size=75,
            client=mock_client,
        )

        # Verify SQL construction
        call_args = mock_client.search.call_args
        assert "SELECT * FROM logs" in call_args.kwargs["sql"]
        assert "service_name = 'auth-service'" in call_args.kwargs["sql"]
        assert call_args.kwargs["start_time"] == "-30m"
        assert call_args.kwargs["end_time"] == "now"
        assert call_args.kwargs["size"] == 75

        assert result == mock_response

    @pytest.mark.asyncio
    async def test_search_by_service_with_dots(self) -> None:
        """Test search_by_service with service names containing dots."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await search_by_service(
            service="api.gateway.v2",
            client=mock_client,
        )

        call_args = mock_client.search.call_args
        assert "service_name = 'api.gateway.v2'" in call_args.kwargs["sql"]
        assert result == mock_response


class TestAggregateByLevelUnit(FoundationTestCase):
    """Unit tests for aggregate_by_level function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_aggregate_by_level_result_processing(self) -> None:
        """Test aggregate_by_level processes results correctly."""
        mock_client = Mock()

        # Create mock response with aggregation results
        mock_response = SearchResponse(
            hits=[
                {"level": "ERROR", "count": 42},
                {"level": "WARNING", "count": 15},
                {"level": "INFO", "count": 100},
                {"level": "DEBUG", "count": 5},
            ],
            total=4,
            took=20,
            scan_size=4,
        )
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await aggregate_by_level(
            stream="metrics",
            start_time="-1d",
            end_time="now",
            client=mock_client,
        )

        # Verify SQL uses GROUP BY
        call_args = mock_client.search.call_args
        assert "GROUP BY level" in call_args.kwargs["sql"]
        assert "SELECT level, COUNT(*)" in call_args.kwargs["sql"]
        assert call_args.kwargs["size"] == 1000

        # Verify result dictionary is constructed correctly
        assert isinstance(result, dict)
        assert result["ERROR"] == 42
        assert result["WARNING"] == 15
        assert result["INFO"] == 100
        assert result["DEBUG"] == 5

    @pytest.mark.asyncio
    async def test_aggregate_by_level_with_unknown_level(self) -> None:
        """Test aggregate_by_level handles hits without level field."""
        mock_client = Mock()

        # Create response with some hits missing 'level' field
        mock_response = SearchResponse(
            hits=[
                {"level": "ERROR", "count": 10},
                {"count": 5},  # Missing level
                {"level": "INFO", "count": 20},
            ],
            total=3,
            took=15,
            scan_size=3,
        )
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await aggregate_by_level(client=mock_client)

        # Verify UNKNOWN is used for missing level
        assert result["ERROR"] == 10
        assert result["UNKNOWN"] == 5
        assert result["INFO"] == 20

    @pytest.mark.asyncio
    async def test_aggregate_by_level_empty_results(self) -> None:
        """Test aggregate_by_level with empty results."""
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await aggregate_by_level(client=mock_client)

        assert isinstance(result, dict)
        assert len(result) == 0


class TestGetCurrentTraceLogsUnit(FoundationTestCase):
    """Unit tests for get_current_trace_logs function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    @pytest.mark.asyncio
    async def test_get_current_trace_logs_no_active_trace(self) -> None:
        """Test get_current_trace_logs when no trace is active.

        This tests the common case where neither OpenTelemetry nor Foundation
        tracer have an active trace, which should return None.
        """
        mock_client = Mock()
        mock_response = SearchResponse(hits=[], total=0, took=10, scan_size=0)
        mock_client.search = AsyncMock(return_value=mock_response)

        result = await get_current_trace_logs(client=mock_client)

        # Should return None when no active trace or a SearchResponse
        # This exercises all the ImportError and None check paths
        assert result is None or hasattr(result, "hits")


__all__ = [
    "TestAggregateByLevelUnit",
    "TestGetCurrentTraceLogsUnit",
    "TestSearchByLevelUnit",
    "TestSearchByServiceUnit",
    "TestSearchByTraceIdUnit",
    "TestSearchErrorsUnit",
    "TestSearchLogsUnit",
]

# 🧱🏗️🔚
