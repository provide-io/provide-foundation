#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Integration tests for OpenObserve streaming operations.

This module contains tests for streaming functionality including polling,
HTTP/2 streaming, and tail operations.

Run with: pytest tests/integrations/openobserve/ -m integration -v"""

from __future__ import annotations

from itertools import islice

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors.config import ValidationError
from provide.foundation.integrations.openobserve.client import OpenObserveClient
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.streaming import (
    _build_where_clause_from_filters,
    stream_logs,
    stream_search_http2,
    tail_logs,
)


class TestBuildWhereClause(FoundationTestCase):
    """Unit tests for WHERE clause building."""

    def test_build_where_clause_empty(self) -> None:
        """Test building WHERE clause with no filters."""
        result = _build_where_clause_from_filters({})

        assert result == ""

    def test_build_where_clause_single_filter(self) -> None:
        """Test building WHERE clause with single filter."""
        result = _build_where_clause_from_filters({"level": "ERROR"})

        assert result == "WHERE level = 'ERROR'"

    def test_build_where_clause_multiple_filters(self) -> None:
        """Test building WHERE clause with multiple filters."""
        result = _build_where_clause_from_filters(
            {"level": "ERROR", "service": "api"},
        )

        # Should combine with AND
        assert "WHERE " in result
        assert "level = 'ERROR'" in result
        assert "service = 'api'" in result
        assert " AND " in result

    def test_build_where_clause_escapes_quotes(self) -> None:
        """Test that single quotes are escaped in filter values."""
        result = _build_where_clause_from_filters(
            {"message": "O'Brien's error"},
        )

        # Single quotes should be doubled for SQL escaping
        assert "O''Brien''s error" in result

    def test_build_where_clause_invalid_key(self) -> None:
        """Test that invalid filter keys are rejected."""
        with pytest.raises(ValidationError, match="Invalid filter key"):
            _build_where_clause_from_filters({"invalid-key": "value"})

        with pytest.raises(ValidationError, match="Invalid filter key"):
            _build_where_clause_from_filters({"key; DROP TABLE": "value"})

    def test_build_where_clause_valid_keys(self) -> None:
        """Test that various valid key formats are accepted."""
        # Alphanumeric and underscores are valid
        result = _build_where_clause_from_filters(
            {"valid_key_123": "value"},
        )
        assert "valid_key_123 = 'value'" in result


@pytest.mark.integration
class TestStreamLogs(FoundationTestCase):
    """Integration tests for polling-based log streaming."""

    def test_stream_logs_basic(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test basic log streaming (fetching first few items)."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name}"

        # Stream logs but only take first 3 items (to avoid infinite loop)
        stream = stream_logs(
            sql=sql,
            start_time="-1h",
            poll_interval=1,
            client=openobserve_client,
        )

        # Get first 3 items (or fewer if stream has less)
        items = list(islice(stream, 3))

        # Should get list of dicts
        assert isinstance(items, list)
        # All items should be dicts
        for item in items:
            assert isinstance(item, dict)

    def test_stream_logs_with_custom_start_time(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test streaming with custom start time."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name}"

        # Stream from 30 minutes ago
        stream = stream_logs(
            sql=sql,
            start_time="-30m",
            poll_interval=1,
            client=openobserve_client,
        )

        # Get first item
        items = list(islice(stream, 1))

        assert isinstance(items, list)

    @pytest.mark.skip(reason="Streaming generator cannot be called from async context - needs refactoring")
    def test_stream_logs_creates_client_if_none(
        self,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that stream_logs creates client if not provided.

        Note: This test is skipped because stream_logs() uses run_async() internally,
        which cannot be called from within an already-running event loop. The fixture
        setup creates an async context, causing this conflict. The function works fine
        when called from sync code (which is its intended use case).
        """
        sql = f"SELECT * FROM {test_stream_name} LIMIT 1"

        stream = stream_logs(sql=sql, poll_interval=1)

        # Should work without explicit client
        items = list(islice(stream, 1))
        assert isinstance(items, list)


@pytest.mark.integration
class TestStreamSearchHttp2(FoundationTestCase):
    """Integration tests for HTTP/2 streaming."""

    def test_stream_search_http2_basic(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test basic HTTP/2 streaming (may not be supported by all instances)."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name}"

        try:
            # Try HTTP/2 streaming
            stream = stream_search_http2(
                sql=sql,
                start_time="-1h",
                end_time="now",
                client=openobserve_client,
            )

            # Get first few items
            items = list(islice(stream, 3))

            assert isinstance(items, list)
            for item in items:
                assert isinstance(item, dict)

        except OpenObserveStreamingError:
            # HTTP/2 streaming might not be supported
            pytest.skip("HTTP/2 streaming not supported by this instance")

    def test_stream_search_http2_with_time_range(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test HTTP/2 streaming with time range."""
        assert openobserve_client is not None

        sql = f"SELECT * FROM {test_stream_name}"

        try:
            stream = stream_search_http2(
                sql=sql,
                start_time="-30m",
                end_time="-15m",  # Historical range
                client=openobserve_client,
            )

            # Get available items (may be empty for historical range)
            items = list(islice(stream, 5))

            assert isinstance(items, list)

        except OpenObserveStreamingError:
            pytest.skip("HTTP/2 streaming not supported")

    def test_stream_search_http2_creates_client_if_none(
        self,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that HTTP/2 streaming creates client if not provided."""
        sql = f"SELECT * FROM {test_stream_name}"

        try:
            stream = stream_search_http2(sql=sql)

            # Should work without explicit client
            items = list(islice(stream, 1))
            assert isinstance(items, list)

        except OpenObserveStreamingError:
            pytest.skip("HTTP/2 streaming not supported")


@pytest.mark.integration
class TestTailLogs(FoundationTestCase):
    """Integration tests for tail functionality."""

    def test_tail_logs_basic(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test basic log tailing without follow mode."""
        assert openobserve_client is not None

        # Tail without follow (just initial logs)
        stream = tail_logs(
            stream=test_stream_name,
            follow=False,
            lines=5,
            client=openobserve_client,
        )

        items = list(stream)

        # Should get at most 5 items
        assert len(items) <= 5
        assert isinstance(items, list)

    def test_tail_logs_with_filters(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test tailing with filters."""
        assert openobserve_client is not None

        # Tail with filter
        stream = tail_logs(
            stream=test_stream_name,
            filters={"level": "ERROR"},
            follow=False,
            lines=10,
            client=openobserve_client,
        )

        items = list(stream)

        assert isinstance(items, list)
        # All results should match filter (if any results exist)
        for item in items:
            if "level" in item:
                assert item["level"] == "ERROR"

    def test_tail_logs_different_line_counts(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test tailing with different line counts."""
        assert openobserve_client is not None

        for line_count in [1, 5, 50]:
            stream = tail_logs(
                stream=test_stream_name,
                follow=False,
                lines=line_count,
                client=openobserve_client,
            )

            items = list(stream)
            assert len(items) <= line_count

    def test_tail_logs_invalid_stream_name(
        self,
        openobserve_client: OpenObserveClient | None,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that invalid stream names are rejected."""
        assert openobserve_client is not None

        with pytest.raises(ValidationError, match="Invalid stream name"):
            stream = tail_logs(
                stream="invalid-stream",  # Hyphens not allowed
                follow=False,
                client=openobserve_client,
            )
            list(stream)  # Consume the generator

    def test_tail_logs_invalid_lines_parameter(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that invalid lines parameter is rejected."""
        assert openobserve_client is not None

        # Negative lines
        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            stream = tail_logs(
                stream=test_stream_name,
                lines=-1,
                follow=False,
                client=openobserve_client,
            )
            list(stream)

        # Zero lines
        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            stream = tail_logs(
                stream=test_stream_name,
                lines=0,
                follow=False,
                client=openobserve_client,
            )
            list(stream)

        # Too many lines
        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            stream = tail_logs(
                stream=test_stream_name,
                lines=20000,  # Exceeds max of 10000
                follow=False,
                client=openobserve_client,
            )
            list(stream)

    def test_tail_logs_with_follow_mode(
        self,
        openobserve_client: OpenObserveClient | None,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test tailing in follow mode (get first few items only)."""
        assert openobserve_client is not None

        # Tail in follow mode
        stream = tail_logs(
            stream=test_stream_name,
            follow=True,  # This will continue streaming
            lines=5,
            client=openobserve_client,
        )

        # Only consume first 10 items to avoid infinite loop
        items = list(islice(stream, 10))

        assert isinstance(items, list)
        # Should get some items (at least the initial ones)
        assert len(items) <= 10

    def test_tail_logs_creates_client_if_none(
        self,
        test_stream_name: str,
        skip_if_no_openobserve: None,
    ) -> None:
        """Test that tail_logs creates client if not provided."""
        stream = tail_logs(
            stream=test_stream_name,
            follow=False,
            lines=1,
        )

        items = list(stream)
        assert isinstance(items, list)


__all__ = [
    "TestBuildWhereClause",
    "TestStreamLogs",
    "TestStreamSearchHttp2",
    "TestTailLogs",
]

# 🧱🏗️🔚
