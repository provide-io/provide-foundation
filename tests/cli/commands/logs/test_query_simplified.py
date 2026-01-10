#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Simplified tests for CLI logs query command focused on coverage."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest


class TestBuildQuerySql(FoundationTestCase):
    """Test _build_query_sql function - this is the most important uncovered code."""

    def test_basic_query_no_conditions(self) -> None:
        """Test basic query with no WHERE conditions."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, None, None, "default", 100)
        assert result == "SELECT * FROM default  ORDER BY _timestamp DESC LIMIT 100"

    def test_query_with_trace_id(self) -> None:
        """Test query with trace_id condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql("abc123def456", None, None, "logs", 50)
        assert result == "SELECT * FROM logs WHERE trace_id = 'abc123def456' ORDER BY _timestamp DESC LIMIT 50"

    def test_query_with_level(self) -> None:
        """Test query with level condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, "ERROR", None, "default", 25)
        assert result == "SELECT * FROM default WHERE level = 'ERROR' ORDER BY _timestamp DESC LIMIT 25"

    def test_query_with_service(self) -> None:
        """Test query with service condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, None, "auth-service", "default", 100)
        assert (
            result == "SELECT * FROM default WHERE service = 'auth-service' ORDER BY _timestamp DESC LIMIT 100"
        )

    def test_query_with_all_conditions(self) -> None:
        """Test query with all conditions."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql("abc123", "INFO", "api-gateway", "logs", 200)
        expected = "SELECT * FROM logs WHERE trace_id = 'abc123' AND level = 'INFO' AND service = 'api-gateway' ORDER BY _timestamp DESC LIMIT 200"
        assert result == expected

    def test_invalid_stream_name(self) -> None:
        """Test validation of stream name."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid stream name"):
            _build_query_sql(None, None, None, "invalid-stream!", 100)

        with pytest.raises(ValueError, match="Invalid stream name"):
            _build_query_sql(None, None, None, "stream with spaces", 100)

    def test_invalid_size(self) -> None:
        """Test validation of size parameter."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", 0)

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", -10)

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", 15000)

    def test_invalid_trace_id_format(self) -> None:
        """Test validation of trace_id format."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _build_query_sql("invalid trace!", None, None, "default", 100)

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _build_query_sql("trace@#$", None, None, "default", 100)

    def test_invalid_log_level(self) -> None:
        """Test validation of log level."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid log level"):
            _build_query_sql(None, "INVALID", None, "default", 100)

        with pytest.raises(ValueError, match="Invalid log level"):
            _build_query_sql(None, "info", None, "default", 100)  # wrong case

    def test_invalid_service_name(self) -> None:
        """Test validation of service name."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid service name"):
            _build_query_sql(None, None, "service with spaces", "default", 100)

        with pytest.raises(ValueError, match="Invalid service name"):
            _build_query_sql(None, None, "service@invalid", "default", 100)


class TestGetTraceIdIfNeeded(FoundationTestCase):
    """Test _get_trace_id_if_needed function."""

    def test_no_current_trace_returns_provided_trace_id(self) -> None:
        """Test that when current_trace=False, returns provided trace_id."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        result = _get_trace_id_if_needed(current_trace=False, trace_id="test_trace_123")
        assert result == "test_trace_123"

        result = _get_trace_id_if_needed(current_trace=False, trace_id=None)
        assert result is None

    def test_current_trace_import_error_handling(self) -> None:
        """Test import error handling."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        # Mock the actual import failure scenario by patching at the module level
        with (
            patch.dict("sys.modules", {"opentelemetry": None}),
            patch("builtins.__import__", side_effect=ImportError("No module named 'opentelemetry'")),
            patch("click.echo") as mock_echo,
        ):
            result = _get_trace_id_if_needed(current_trace=True, trace_id=None)
            assert result is None
            mock_echo.assert_called_with("Tracing not available.", err=True)


class TestExecuteAndDisplayQuery(FoundationTestCase):
    """Test _execute_and_display_query function."""

    def test_successful_query_with_results(self) -> None:
        """Test successful query execution with results."""
        from unittest.mock import AsyncMock

        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        # Mock the search_logs and format_output functions
        mock_response = Mock()
        mock_response.total = 5
        mock_response.hits = ["log1", "log2", "log3"]

        with (
            patch(
                "provide.foundation.integrations.openobserve.search_logs",
                new=AsyncMock(return_value=mock_response),
            ) as mock_search,
            patch(
                "provide.foundation.integrations.openobserve.format_output", return_value="formatted_logs"
            ) as mock_format,
            patch("click.echo"),
        ):
            mock_client = Mock()
            result = _execute_and_display_query("SELECT * FROM logs", "1h", 100, "json", mock_client)

            assert result == 0
            mock_search.assert_called_once_with(
                sql="SELECT * FROM logs", start_time="-1h", end_time="now", size=100, client=mock_client
            )
            mock_format.assert_called_once_with(mock_response, format_type="json")

    def test_successful_query_no_results(self) -> None:
        """Test successful query with no results."""
        from unittest.mock import AsyncMock

        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        mock_response = Mock()
        mock_response.total = 0

        with (
            patch(
                "provide.foundation.integrations.openobserve.search_logs",
                new=AsyncMock(return_value=mock_response),
            ),
            patch("click.echo") as mock_echo,
        ):
            mock_client = Mock()
            result = _execute_and_display_query("SELECT * FROM logs", "30m", 50, "log", mock_client)

            assert result == 0
            mock_echo.assert_called_once_with("No logs found matching the query.")

    def test_query_exception_handling(self) -> None:
        """Test exception handling in query execution."""
        from unittest.mock import AsyncMock

        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        with (
            patch(
                "provide.foundation.integrations.openobserve.search_logs",
                new=AsyncMock(side_effect=Exception("Connection failed")),
            ),
            patch("click.echo") as mock_echo,
        ):
            mock_client = Mock()
            result = _execute_and_display_query("SELECT * FROM logs", "1h", 100, "json", mock_client)

            assert result == 1
            mock_echo.assert_called_once_with("Query failed: Connection failed", err=True)


class TestValidationEdgeCases(FoundationTestCase):
    """Test edge cases in validation logic."""

    def test_trace_id_uuid_format_valid(self) -> None:
        """Test that UUID format trace IDs are valid."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Standard UUID format should work
        uuid_trace = "550e8400-e29b-41d4-a716-446655440000"
        result = _build_query_sql(uuid_trace, None, None, "default", 100)
        assert f"trace_id = '{uuid_trace}'" in result

    def test_trace_id_hex_format_valid(self) -> None:
        """Test that hex format trace IDs are valid."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Hex format should work
        hex_trace = "abcdef1234567890"
        result = _build_query_sql(hex_trace, None, None, "default", 100)
        assert f"trace_id = '{hex_trace}'" in result

    def test_boundary_size_values(self) -> None:
        """Test boundary values for size parameter."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Minimum valid size
        result = _build_query_sql(None, None, None, "default", 1)
        assert "LIMIT 1" in result

        # Maximum valid size
        result = _build_query_sql(None, None, None, "default", 10000)
        assert "LIMIT 10000" in result

        # Just over maximum should fail
        with pytest.raises(ValueError):
            _build_query_sql(None, None, None, "default", 10001)


class TestQueryCommandWithoutClick(FoundationTestCase):
    """Test query command behavior when click is not available."""

    def test_command_import_availability(self) -> None:
        """Test that the module can be imported and function exists."""
        from provide.foundation.cli.commands.logs.query import query_command
        from provide.foundation.cli.deps import _HAS_CLICK

        # Function should exist regardless of click availability
        assert callable(query_command)

        # If click is not available, should behave differently
        if not _HAS_CLICK:
            with pytest.raises(ImportError, match="CLI commands require optional dependencies"):
                query_command()


class TestModuleImports(FoundationTestCase):
    """Test basic module imports and structure."""

    def test_module_has_required_functions(self) -> None:
        """Test that module has all required functions."""
        from provide.foundation.cli.commands.logs import query

        assert hasattr(query, "_get_trace_id_if_needed")
        assert hasattr(query, "_build_query_sql")
        assert hasattr(query, "_execute_and_display_query")
        assert hasattr(query, "query_command")
        # _HAS_CLICK is in cli.deps, not in the query module

    def test_module_logger_instance(self) -> None:
        """Test that module has logger instance."""
        from provide.foundation.cli.commands.logs.query import log

        assert log is not None
        assert hasattr(log, "info")
        assert hasattr(log, "debug")
        assert hasattr(log, "error")


# 🧱🏗️🔚
