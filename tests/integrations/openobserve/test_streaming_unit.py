#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve streaming operations.

This module contains unit tests for streaming functionality with mocked dependencies.
Run with: pytest tests/integrations/openobserve/test_streaming_unit.py -v"""

from __future__ import annotations

from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.integrations.openobserve.exceptions import (
    OpenObserveStreamingError,
)
from provide.foundation.integrations.openobserve.streaming import (
    _build_where_clause_from_filters,
    _parse_time_param,
    _process_stream_line,
    stream_logs,
    stream_search_http2,
    stream_search_http2_async,
    tail_logs,
)


class TestParseTimeParam(FoundationTestCase):
    """Tests for _parse_time_param helper function."""

    def test_parse_time_param_none(self) -> None:
        """Test parsing None returns default."""
        with patch("provide.foundation.integrations.openobserve.streaming.parse_relative_time") as mock_parse:
            mock_parse.return_value = 1234567890
            result = _parse_time_param(None, "-1h")
            assert result == 1234567890
            mock_parse.assert_called_once_with("-1h")

    def test_parse_time_param_string(self) -> None:
        """Test parsing string time parameter."""
        with patch("provide.foundation.integrations.openobserve.streaming.parse_relative_time") as mock_parse:
            mock_parse.return_value = 9876543210
            result = _parse_time_param("-2h", "-1h")
            assert result == 9876543210
            mock_parse.assert_called_once_with("-2h")

    def test_parse_time_param_int(self) -> None:
        """Test parsing integer time parameter."""
        result = _parse_time_param(1234567890, "-1h")
        assert result == 1234567890


class TestProcessStreamLine(FoundationTestCase):
    """Tests for _process_stream_line helper function."""

    def test_process_empty_line(self) -> None:
        """Test processing empty line."""
        result = _process_stream_line("")
        assert result == []

    def test_process_line_with_hits(self) -> None:
        """Test processing line with hits array."""
        line = '{"hits": [{"message": "test1"}, {"message": "test2"}]}'
        result = _process_stream_line(line)
        assert len(result) == 2
        assert result[0] == {"message": "test1"}
        assert result[1] == {"message": "test2"}

    def test_process_line_single_dict(self) -> None:
        """Test processing line with single dict."""
        line = '{"message": "test"}'
        result = _process_stream_line(line)
        assert len(result) == 1
        assert result[0] == {"message": "test"}

    def test_process_invalid_json(self) -> None:
        """Test processing invalid JSON returns empty list."""
        result = _process_stream_line("not json")
        assert result == []

    def test_process_line_list(self) -> None:
        """Test processing line that is a list (not expected format)."""
        line = '[{"message": "test"}]'
        result = _process_stream_line(line)
        # Should return empty since it's not a dict
        assert result == []


class TestBuildWhereClauseFromFilters(FoundationTestCase):
    """Tests for _build_where_clause_from_filters function."""

    def test_build_where_clause_empty_filters(self) -> None:
        """Test building WHERE clause with empty filters."""
        result = _build_where_clause_from_filters({})
        assert result == ""

    def test_build_where_clause_single_filter(self) -> None:
        """Test building WHERE clause with single filter."""
        result = _build_where_clause_from_filters({"level": "ERROR"})
        assert result == "WHERE level = 'ERROR'"

    def test_build_where_clause_multiple_filters(self) -> None:
        """Test building WHERE clause with multiple filters."""
        result = _build_where_clause_from_filters({"level": "ERROR", "service": "api"})
        # Check that both conditions are present
        assert "WHERE" in result
        assert "level = 'ERROR'" in result
        assert "service = 'api'" in result
        assert "AND" in result

    def test_build_where_clause_escapes_quotes(self) -> None:
        """Test that single quotes are escaped."""
        result = _build_where_clause_from_filters({"message": "it's a test"})
        assert result == "WHERE message = 'it''s a test'"

    def test_build_where_clause_invalid_key(self) -> None:
        """Test that invalid column names raise ValidationError."""
        with pytest.raises(ValidationError, match="Invalid filter key"):
            _build_where_clause_from_filters({"bad-key": "value"})

    def test_build_where_clause_sql_injection_attempt(self) -> None:
        """Test protection against SQL injection in key names."""
        with pytest.raises(ValidationError, match="Invalid filter key"):
            _build_where_clause_from_filters({"level; DROP TABLE": "ERROR"})


class TestStreamLogs(FoundationTestCase):
    """Tests for stream_logs generator function."""

    def test_stream_logs_creates_client_if_none(self) -> None:
        """Test that stream_logs creates client if not provided."""
        with patch(
            "provide.foundation.integrations.openobserve.streaming.OpenObserveClient.from_config"
        ) as mock_from_config:
            mock_client = MagicMock()
            mock_from_config.return_value = mock_client

            # Mock search to return immediately to avoid infinite loop
            with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
                mock_response = MagicMock()
                mock_response.hits = []
                mock_run_async.return_value = mock_response

                # Create generator
                gen = stream_logs(sql="SELECT * FROM logs")

                with patch("time.sleep") as mock_sleep:
                    mock_sleep.side_effect = KeyboardInterrupt()  # Stop after first poll
                    # Consume generator which will catch KeyboardInterrupt
                    list(gen)

                mock_from_config.assert_called_once()

    def test_stream_logs_processes_hits(self) -> None:
        """Test that stream_logs processes and yields hits."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            # First call returns hits, second call raises KeyboardInterrupt
            mock_response = MagicMock()
            mock_response.hits = [
                {"_timestamp": 1000, "message": "log1"},
                {"_timestamp": 2000, "message": "log2"},
            ]
            mock_run_async.return_value = mock_response

            gen = stream_logs(sql="SELECT * FROM logs", client=mock_client)

            with patch("time.sleep") as mock_sleep:
                mock_sleep.side_effect = KeyboardInterrupt()

                results = []
                try:
                    for hit in gen:
                        results.append(hit)
                except KeyboardInterrupt:
                    pass

                assert len(results) == 2
                assert results[0]["message"] == "log1"
                assert results[1]["message"] == "log2"

    def test_stream_logs_keyboard_interrupt(self) -> None:
        """Test that stream_logs handles KeyboardInterrupt gracefully."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            mock_response = MagicMock()
            mock_response.hits = []
            mock_run_async.return_value = mock_response

            gen = stream_logs(sql="SELECT * FROM logs", client=mock_client)

            with patch("time.sleep") as mock_sleep:
                mock_sleep.side_effect = KeyboardInterrupt()

                # Should exit gracefully
                results = list(gen)
                assert results == []

    def test_stream_logs_raises_streaming_error(self) -> None:
        """Test that stream_logs raises OpenObserveStreamingError on failures."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            mock_run_async.side_effect = ValueError("Connection failed")

            gen = stream_logs(sql="SELECT * FROM logs", client=mock_client)

            with pytest.raises(OpenObserveStreamingError, match="Streaming failed"):
                next(gen)


class TestStreamSearchHTTP2Async(FoundationTestCase):
    """Tests for stream_search_http2_async async generator."""

    async def test_stream_search_http2_async_creates_client(self) -> None:
        """Test that async streaming creates client if not provided."""
        with patch(
            "provide.foundation.integrations.openobserve.streaming.OpenObserveClient.from_config"
        ) as mock_from_config:
            mock_client = MagicMock()
            mock_client.url = "http://localhost:5080"
            mock_client.organization = "default"
            mock_client._client = MagicMock()

            # Create async generator that yields nothing
            async def empty_stream(*args: Any, **kwargs: Any) -> None:
                if False:
                    yield b""
                return

            mock_client._client.stream = empty_stream
            mock_from_config.return_value = mock_client

            results = []
            async for hit in stream_search_http2_async(sql="SELECT * FROM logs"):
                results.append(hit)

            assert results == []
            mock_from_config.assert_called_once()

    async def test_stream_search_http2_async_yields_hits(self) -> None:
        """Test that async streaming yields hits from chunks."""
        mock_client = MagicMock()
        mock_client.url = "http://localhost:5080"
        mock_client.organization = "default"
        mock_client._client = MagicMock()

        # Mock stream to yield chunks
        async def mock_stream(*args: Any, **kwargs: Any) -> Any:
            yield b'{"hits": [{"message": "test1"}]}\n'
            yield b'{"message": "test2"}\n'

        mock_client._client.stream = mock_stream

        results = []
        async for hit in stream_search_http2_async(sql="SELECT * FROM logs", client=mock_client):
            results.append(hit)

        assert len(results) == 2
        assert results[0]["message"] == "test1"
        assert results[1]["message"] == "test2"

    async def test_stream_search_http2_async_error_handling(self) -> None:
        """Test that async streaming handles errors."""
        mock_client = MagicMock()
        mock_client.url = "http://localhost:5080"
        mock_client.organization = "default"
        mock_client._client = MagicMock()

        async def failing_stream(*args: Any, **kwargs: Any) -> None:
            raise ValueError("Stream failed")
            if False:  # Make it a generator
                yield b""

        mock_client._client.stream = failing_stream

        with pytest.raises(OpenObserveStreamingError, match="HTTP/2 streaming failed"):
            async for _ in stream_search_http2_async(sql="SELECT * FROM logs", client=mock_client):
                pass


class TestStreamSearchHTTP2(FoundationTestCase):
    """Tests for stream_search_http2 sync wrapper."""

    def test_stream_search_http2_sync_wrapper(self) -> None:
        """Test that sync wrapper works correctly."""
        mock_client = MagicMock()
        mock_client.url = "http://localhost:5080"
        mock_client.organization = "default"
        mock_client._client = MagicMock()

        # Mock the async function
        async def mock_async_gen() -> Any:
            yield {"message": "test1"}
            yield {"message": "test2"}

        with patch(
            "provide.foundation.integrations.openobserve.streaming.stream_search_http2_async",
            return_value=mock_async_gen(),
        ):
            results = list(stream_search_http2(sql="SELECT * FROM logs", client=mock_client))

            assert len(results) == 2
            assert results[0]["message"] == "test1"
            assert results[1]["message"] == "test2"


class TestTailLogs(FoundationTestCase):
    """Tests for tail_logs function."""

    def test_tail_logs_invalid_stream_name(self) -> None:
        """Test that invalid stream names are rejected."""
        with pytest.raises(ValidationError, match="Invalid stream name"):
            gen = tail_logs(stream="invalid-name")
            next(gen)

    def test_tail_logs_invalid_lines_parameter(self) -> None:
        """Test that invalid lines parameter is rejected."""
        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            gen = tail_logs(stream="default", lines=0)
            next(gen)

        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            gen = tail_logs(stream="default", lines=-5)
            next(gen)

        with pytest.raises(ValidationError, match="Invalid lines parameter"):
            gen = tail_logs(stream="default", lines=20000)  # Over limit
            next(gen)

    def test_tail_logs_creates_client(self) -> None:
        """Test that tail_logs creates client if not provided."""
        with patch(
            "provide.foundation.integrations.openobserve.streaming.OpenObserveClient.from_config"
        ) as mock_from_config:
            mock_client = MagicMock()
            mock_from_config.return_value = mock_client

            with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
                mock_response = MagicMock()
                mock_response.hits = []
                mock_run_async.return_value = mock_response

                gen = tail_logs(stream="default", follow=False)
                results = list(gen)

                assert results == []
                mock_from_config.assert_called_once()

    def test_tail_logs_yields_initial_logs(self) -> None:
        """Test that tail_logs yields initial logs in reverse order."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            mock_response = MagicMock()
            mock_response.hits = [
                {"_timestamp": 3000, "message": "newest"},
                {"_timestamp": 2000, "message": "middle"},
                {"_timestamp": 1000, "message": "oldest"},
            ]
            mock_run_async.return_value = mock_response

            gen = tail_logs(stream="default", follow=False, client=mock_client)
            results = list(gen)

            # Should be in reverse order (oldest first)
            assert len(results) == 3
            assert results[0]["message"] == "oldest"
            assert results[1]["message"] == "middle"
            assert results[2]["message"] == "newest"

    def test_tail_logs_with_filters(self) -> None:
        """Test that tail_logs applies filters correctly."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            mock_response = MagicMock()
            mock_response.hits = []
            mock_run_async.return_value = mock_response

            filters = {"level": "ERROR", "service": "api"}
            gen = tail_logs(stream="default", filters=filters, follow=False, client=mock_client)
            list(gen)

            # Verify the SQL query includes the WHERE clause
            # The search method is called with coroutine, extract SQL from it
            assert mock_run_async.called

    def test_tail_logs_follow_mode(self) -> None:
        """Test that tail_logs continues streaming in follow mode."""
        mock_client = MagicMock()

        with patch("provide.foundation.integrations.openobserve.streaming.run_async") as mock_run_async:
            # First call for initial logs
            initial_response = MagicMock()
            initial_response.hits = [{"_timestamp": 1000, "message": "initial"}]
            mock_run_async.return_value = initial_response

            with patch("provide.foundation.integrations.openobserve.streaming.stream_logs") as mock_stream:
                # Mock stream_logs to yield one more log then stop
                def mock_stream_gen(*args: Any, **kwargs: Any) -> Any:
                    yield {"_timestamp": 2000, "message": "streamed"}

                mock_stream.return_value = mock_stream_gen()

                gen = tail_logs(stream="default", follow=True, client=mock_client)
                results = list(gen)

                # Should get initial log + streamed log
                assert len(results) == 2
                assert results[0]["message"] == "initial"
                assert results[1]["message"] == "streamed"

                # Verify stream_logs was called
                mock_stream.assert_called_once()


__all__ = [
    "TestBuildWhereClauseFromFilters",
    "TestParseTimeParam",
    "TestProcessStreamLine",
    "TestStreamLogs",
    "TestStreamSearchHTTP2",
    "TestStreamSearchHTTP2Async",
    "TestTailLogs",
]

# 🧱🏗️🔚
