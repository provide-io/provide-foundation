#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve data models.

This module contains unit tests for OpenObserve API models including
SearchQuery, SearchResponse, StreamInfo, and time parsing utilities.
These are pure unit tests that don't require a running OpenObserve instance."""

from __future__ import annotations

from datetime import datetime, timedelta

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.integrations.openobserve.models import (
    SearchQuery,
    SearchResponse,
    StreamInfo,
    parse_relative_time,
)


class TestSearchQuery(FoundationTestCase):
    """Tests for SearchQuery model."""

    def test_search_query_basic(self) -> None:
        """Test basic SearchQuery creation and to_dict conversion."""
        query = SearchQuery(
            sql="SELECT * FROM logs",
            start_time=1609459200000000,  # 2021-01-01 00:00:00 in microseconds
            end_time=1609545600000000,  # 2021-01-02 00:00:00 in microseconds
            from_offset=0,
            size=100,
        )

        result = query.to_dict()

        assert result == {
            "query": {
                "sql": "SELECT * FROM logs",
                "start_time": 1609459200000000,
                "end_time": 1609545600000000,
                "from": 0,
                "size": 100,
            },
        }

    def test_search_query_with_offset(self) -> None:
        """Test SearchQuery with non-zero offset."""
        query = SearchQuery(
            sql="SELECT level, message FROM logs WHERE level='ERROR'",
            start_time=1609459200000000,
            end_time=1609545600000000,
            from_offset=50,
            size=25,
        )

        result = query.to_dict()

        assert result["query"]["from"] == 50
        assert result["query"]["size"] == 25

    def test_search_query_defaults(self) -> None:
        """Test SearchQuery with default values."""
        query = SearchQuery(
            sql="SELECT * FROM logs",
            start_time=1000000,
            end_time=2000000,
        )

        result = query.to_dict()

        assert result["query"]["from"] == 0
        assert result["query"]["size"] == 100


class TestSearchResponse(FoundationTestCase):
    """Tests for SearchResponse model."""

    def test_search_response_basic(self) -> None:
        """Test basic SearchResponse creation from dict."""
        data = {
            "hits": [
                {"_timestamp": 1609459200000000, "message": "Test log"},
                {"_timestamp": 1609459201000000, "message": "Another log"},
            ],
            "total": 2,
            "took": 42,
            "scan_size": 1024,
            "from": 0,
            "size": 100,
        }

        response = SearchResponse.from_dict(data)

        assert len(response.hits) == 2
        assert response.total == 2
        assert response.took == 42
        assert response.scan_size == 1024
        assert response.from_offset == 0
        assert response.size == 100
        assert response.is_partial is False
        assert response.function_error == []

    def test_search_response_with_trace_id(self) -> None:
        """Test SearchResponse with trace_id."""
        data = {
            "hits": [],
            "total": 0,
            "took": 10,
            "scan_size": 0,
            "trace_id": "abc123def456",
        }

        response = SearchResponse.from_dict(data)

        assert response.trace_id == "abc123def456"

    def test_search_response_partial_results(self) -> None:
        """Test SearchResponse with partial results flag."""
        data = {
            "hits": [{"message": "partial"}],
            "total": 100,
            "took": 1000,
            "scan_size": 5000,
            "is_partial": True,
        }

        response = SearchResponse.from_dict(data)

        assert response.is_partial is True
        assert response.total == 100
        assert len(response.hits) == 1

    def test_search_response_with_function_error(self) -> None:
        """Test SearchResponse with function errors."""
        data = {
            "hits": [],
            "total": 0,
            "took": 5,
            "scan_size": 0,
            "function_error": [
                "UDF function failed: division by zero",
                "Syntax error in SQL",
            ],
        }

        response = SearchResponse.from_dict(data)

        assert len(response.function_error) == 2
        assert "division by zero" in response.function_error[0]
        assert "Syntax error" in response.function_error[1]

    def test_search_response_empty_defaults(self) -> None:
        """Test SearchResponse with minimal/missing fields uses defaults."""
        data = {}  # Empty response

        response = SearchResponse.from_dict(data)

        assert response.hits == []
        assert response.total == 0
        assert response.took == 0
        assert response.scan_size == 0
        assert response.trace_id is None
        assert response.from_offset == 0
        assert response.size == 0
        assert response.is_partial is False
        assert response.function_error == []


class TestStreamInfo(FoundationTestCase):
    """Tests for StreamInfo model."""

    def test_stream_info_basic(self) -> None:
        """Test basic StreamInfo creation from dict."""
        data = {
            "name": "logs",
            "storage_type": "disk",
            "stream_type": "logs",
            "stats": {
                "doc_count": 1000,
                "compressed_size": 512000,
                "original_size": 2048000,
            },
        }

        stream = StreamInfo.from_dict(data)

        assert stream.name == "logs"
        assert stream.storage_type == "disk"
        assert stream.stream_type == "logs"
        assert stream.doc_count == 1000
        assert stream.compressed_size == 512000
        assert stream.original_size == 2048000

    def test_stream_info_empty_stats(self) -> None:
        """Test StreamInfo with missing stats uses defaults."""
        data = {
            "name": "metrics",
            "storage_type": "memory",
            "stream_type": "metrics",
        }

        stream = StreamInfo.from_dict(data)

        assert stream.name == "metrics"
        assert stream.doc_count == 0
        assert stream.compressed_size == 0
        assert stream.original_size == 0

    def test_stream_info_partial_stats(self) -> None:
        """Test StreamInfo with partial stats."""
        data = {
            "name": "traces",
            "storage_type": "disk",
            "stream_type": "traces",
            "stats": {
                "doc_count": 500,
                # compressed_size and original_size missing
            },
        }

        stream = StreamInfo.from_dict(data)

        assert stream.name == "traces"
        assert stream.doc_count == 500
        assert stream.compressed_size == 0
        assert stream.original_size == 0

    def test_stream_info_minimal(self) -> None:
        """Test StreamInfo with minimal data."""
        data = {}  # Empty dict

        stream = StreamInfo.from_dict(data)

        assert stream.name == ""
        assert stream.storage_type == ""
        assert stream.stream_type == ""
        assert stream.doc_count == 0


class TestParseRelativeTime(FoundationTestCase):
    """Tests for parse_relative_time utility function."""

    def test_parse_now(self) -> None:
        """Test parsing 'now' returns current time."""
        fixed_time = datetime(2021, 1, 1, 12, 0, 0)
        result = parse_relative_time("now", now=fixed_time)

        expected = int(fixed_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_hours_ago(self) -> None:
        """Test parsing relative hours (e.g., '-1h', '-2h')."""
        fixed_time = datetime(2021, 1, 1, 12, 0, 0)

        # 1 hour ago
        result = parse_relative_time("-1h", now=fixed_time)
        expected_time = fixed_time - timedelta(hours=1)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

        # 24 hours ago
        result = parse_relative_time("-24h", now=fixed_time)
        expected_time = fixed_time - timedelta(hours=24)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_minutes_ago(self) -> None:
        """Test parsing relative minutes (e.g., '-30m', '-5m')."""
        fixed_time = datetime(2021, 1, 1, 12, 0, 0)

        # 30 minutes ago
        result = parse_relative_time("-30m", now=fixed_time)
        expected_time = fixed_time - timedelta(minutes=30)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

        # 5 minutes ago
        result = parse_relative_time("-5m", now=fixed_time)
        expected_time = fixed_time - timedelta(minutes=5)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_seconds_ago(self) -> None:
        """Test parsing relative seconds (e.g., '-60s', '-10s')."""
        fixed_time = datetime(2021, 1, 1, 12, 0, 0)

        # 60 seconds ago
        result = parse_relative_time("-60s", now=fixed_time)
        expected_time = fixed_time - timedelta(seconds=60)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_days_ago(self) -> None:
        """Test parsing relative days (e.g., '-1d', '-7d')."""
        fixed_time = datetime(2021, 1, 8, 12, 0, 0)

        # 1 day ago
        result = parse_relative_time("-1d", now=fixed_time)
        expected_time = fixed_time - timedelta(days=1)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

        # 7 days ago
        result = parse_relative_time("-7d", now=fixed_time)
        expected_time = fixed_time - timedelta(days=7)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_seconds_no_unit(self) -> None:
        """Test parsing relative time with no unit (assumes seconds)."""
        fixed_time = datetime(2021, 1, 1, 12, 0, 0)

        # -300 (should be interpreted as 300 seconds ago)
        result = parse_relative_time("-300", now=fixed_time)
        expected_time = fixed_time - timedelta(seconds=300)
        expected = int(expected_time.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_timestamp_microseconds(self) -> None:
        """Test parsing timestamp already in microseconds."""
        # Large number indicates microseconds
        microseconds = 1609459200000000  # 2021-01-01 00:00:00 in microseconds

        result = parse_relative_time(str(microseconds))

        assert result == microseconds

    def test_parse_timestamp_seconds(self) -> None:
        """Test parsing timestamp in seconds (gets converted to microseconds)."""
        # Smaller number indicates seconds
        seconds = 1609459200  # 2021-01-01 00:00:00 in seconds

        result = parse_relative_time(str(seconds))

        expected = seconds * 1_000_000
        assert result == expected

    def test_parse_iso_datetime(self) -> None:
        """Test parsing ISO format datetime string."""
        iso_string = "2021-01-01T12:00:00"

        result = parse_relative_time(iso_string)

        dt = datetime.fromisoformat(iso_string)
        expected = int(dt.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_iso_datetime_with_timezone(self) -> None:
        """Test parsing ISO format datetime with timezone."""
        iso_string = "2021-01-01T12:00:00+00:00"

        result = parse_relative_time(iso_string)

        dt = datetime.fromisoformat(iso_string)
        expected = int(dt.timestamp() * 1_000_000)
        assert result == expected

    def test_parse_invalid_format_raises_error(self) -> None:
        """Test that invalid time format raises ValueError."""
        with pytest.raises(ValueError):
            parse_relative_time("invalid-time-format")

    def test_parse_with_default_now(self) -> None:
        """Test parse_relative_time uses current time when now=None."""
        # Test that it doesn't crash and returns a reasonable value
        result = parse_relative_time("now")

        # Should be close to current time
        current_microseconds = int(datetime.now().timestamp() * 1_000_000)
        # Allow 1 second tolerance
        assert abs(result - current_microseconds) < 1_000_000


# 🧱🏗️🔚
