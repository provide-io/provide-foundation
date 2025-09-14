"""Comprehensive tests for CLI logs query command."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
from typing import Any


class TestGetTraceIdIfNeeded:
    """Test _get_trace_id_if_needed function."""

    def test_no_current_trace_returns_provided_trace_id(self):
        """Test that when current_trace=False, returns provided trace_id."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        result = _get_trace_id_if_needed(current_trace=False, trace_id="test_trace_123")
        assert result == "test_trace_123"

        result = _get_trace_id_if_needed(current_trace=False, trace_id=None)
        assert result is None

    def test_current_trace_with_opentelemetry_active_span(self):
        """Test getting trace ID from OpenTelemetry active span."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        mock_span_context = Mock()
        mock_span_context.trace_id = 0x123456789ABCDEF0123456789ABCDEF0

        mock_span = Mock()
        mock_span.is_recording.return_value = True
        mock_span.get_span_context.return_value = mock_span_context

        with patch('opentelemetry.trace') as mock_otel_trace:
            mock_otel_trace.get_current_span.return_value = mock_span

            result = _get_trace_id_if_needed(current_trace=True, trace_id=None)

            # Should format trace ID as 32-character hex string
            assert result == "123456789abcdef0123456789abcdef0"

    def test_current_trace_otel_span_not_recording(self):
        """Test fallback to Foundation tracer when OTEL span not recording."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        mock_span = Mock()
        mock_span.is_recording.return_value = False

        with patch('opentelemetry.trace') as mock_otel_trace, \
             patch('provide.foundation.tracer.context.get_current_trace_id') as mock_foundation_trace:

            mock_otel_trace.get_current_span.return_value = mock_span
            mock_foundation_trace.return_value = "foundation_trace_123"

            result = _get_trace_id_if_needed(current_trace=True, trace_id=None)

            assert result == "foundation_trace_123"

    def test_current_trace_no_active_trace(self):
        """Test when no active trace is found."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        mock_span = Mock()
        mock_span.is_recording.return_value = False

        with patch('provide.foundation.cli.commands.logs.query.trace') as mock_otel_trace, \
             patch('provide.foundation.cli.commands.logs.query.get_current_trace_id') as mock_foundation_trace, \
             patch('click') as mock_click:

            mock_otel_trace.get_current_span.return_value = mock_span
            mock_foundation_trace.return_value = None

            result = _get_trace_id_if_needed(current_trace=True, trace_id=None)

            assert result is None
            mock_click.echo.assert_called_with("No active trace found.", err=True)

    def test_current_trace_import_error(self):
        """Test when tracing imports fail."""
        from provide.foundation.cli.commands.logs.query import _get_trace_id_if_needed

        with patch('provide.foundation.cli.commands.logs.query.trace', side_effect=ImportError), \
             patch('click') as mock_click:

            result = _get_trace_id_if_needed(current_trace=True, trace_id=None)

            assert result is None
            mock_click.echo.assert_called_with("Tracing not available.", err=True)


class TestBuildQuerySql:
    """Test _build_query_sql function."""

    def test_basic_query_no_conditions(self):
        """Test basic query with no WHERE conditions."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, None, None, "default", 100)
        assert result == "SELECT * FROM default  ORDER BY _timestamp DESC LIMIT 100"

    def test_query_with_trace_id(self):
        """Test query with trace_id condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql("abc123def456", None, None, "logs", 50)
        assert result == "SELECT * FROM logs WHERE trace_id = 'abc123def456' ORDER BY _timestamp DESC LIMIT 50"

    def test_query_with_level(self):
        """Test query with level condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, "ERROR", None, "default", 25)
        assert result == "SELECT * FROM default WHERE level = 'ERROR' ORDER BY _timestamp DESC LIMIT 25"

    def test_query_with_service(self):
        """Test query with service condition."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql(None, None, "auth-service", "default", 100)
        assert result == "SELECT * FROM default WHERE service = 'auth-service' ORDER BY _timestamp DESC LIMIT 100"

    def test_query_with_all_conditions(self):
        """Test query with all conditions."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        result = _build_query_sql("abc123", "INFO", "api-gateway", "logs", 200)
        expected = "SELECT * FROM logs WHERE trace_id = 'abc123' AND level = 'INFO' AND service = 'api-gateway' ORDER BY _timestamp DESC LIMIT 200"
        assert result == expected

    def test_invalid_stream_name(self):
        """Test validation of stream name."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid stream name"):
            _build_query_sql(None, None, None, "invalid-stream!", 100)

        with pytest.raises(ValueError, match="Invalid stream name"):
            _build_query_sql(None, None, None, "stream with spaces", 100)

    def test_invalid_size(self):
        """Test validation of size parameter."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", 0)

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", -10)

        with pytest.raises(ValueError, match="Invalid size parameter"):
            _build_query_sql(None, None, None, "default", 15000)

    def test_invalid_trace_id_format(self):
        """Test validation of trace_id format."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _build_query_sql("invalid trace!", None, None, "default", 100)

        with pytest.raises(ValueError, match="Invalid trace_id format"):
            _build_query_sql("trace@#$", None, None, "default", 100)

    def test_invalid_log_level(self):
        """Test validation of log level."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid log level"):
            _build_query_sql(None, "INVALID", None, "default", 100)

        with pytest.raises(ValueError, match="Invalid log level"):
            _build_query_sql(None, "info", None, "default", 100)  # wrong case

    def test_invalid_service_name(self):
        """Test validation of service name."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        with pytest.raises(ValueError, match="Invalid service name"):
            _build_query_sql(None, None, "service with spaces", "default", 100)

        with pytest.raises(ValueError, match="Invalid service name"):
            _build_query_sql(None, None, "service@invalid", "default", 100)

    def test_valid_complex_names(self):
        """Test valid complex names for stream and service."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Should work with valid characters
        result = _build_query_sql(None, None, "auth-service_v2.production", "logs_stream_1", 100)
        expected = "SELECT * FROM logs_stream_1 WHERE service = 'auth-service_v2.production' ORDER BY _timestamp DESC LIMIT 100"
        assert result == expected


class TestExecuteAndDisplayQuery:
    """Test _execute_and_display_query function."""

    def test_successful_query_with_results(self):
        """Test successful query execution with results."""
        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        # Mock response with results
        mock_response = Mock()
        mock_response.total = 5
        mock_response.hits = ["log1", "log2", "log3"]

        with patch('provide.foundation.cli.commands.logs.query.search_logs') as mock_search, \
             patch('provide.foundation.cli.commands.logs.query.format_output') as mock_format, \
             patch('click') as mock_click:

            mock_search.return_value = mock_response
            mock_format.return_value = "formatted_logs"
            mock_client = Mock()

            result = _execute_and_display_query("SELECT * FROM logs", "1h", 100, "json", mock_client)

            assert result == 0
            mock_search.assert_called_once_with(
                sql="SELECT * FROM logs",
                start_time="-1h",
                end_time="now",
                size=100,
                client=mock_client
            )
            mock_format.assert_called_once_with(mock_response, format_type="json")
            mock_click.echo.assert_any_call("formatted_logs")
            mock_click.echo.assert_any_call("\n📊 Found 5 logs, showing 3")

    def test_successful_query_no_results(self):
        """Test successful query with no results."""
        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        mock_response = Mock()
        mock_response.total = 0

        with patch('provide.foundation.cli.commands.logs.query.search_logs') as mock_search, \
             patch('click') as mock_click:

            mock_search.return_value = mock_response
            mock_client = Mock()

            result = _execute_and_display_query("SELECT * FROM logs", "30m", 50, "log", mock_client)

            assert result == 0
            mock_search.assert_called_once_with(
                sql="SELECT * FROM logs",
                start_time="-30m",
                end_time="now",
                size=50,
                client=mock_client
            )
            mock_click.echo.assert_called_once_with("No logs found matching the query.")

    def test_query_with_summary_format(self):
        """Test query with summary format doesn't show count."""
        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        mock_response = Mock()
        mock_response.total = 10
        mock_response.hits = ["log1"]

        with patch('provide.foundation.cli.commands.logs.query.search_logs') as mock_search, \
             patch('provide.foundation.cli.commands.logs.query.format_output') as mock_format, \
             patch('click') as mock_click:

            mock_search.return_value = mock_response
            mock_format.return_value = "summary_output"
            mock_client = Mock()

            result = _execute_and_display_query("SELECT * FROM logs", "2h", 100, "summary", mock_client)

            assert result == 0
            # Should only echo the formatted output, not the count
            mock_click.echo.assert_called_once_with("summary_output")

    def test_query_exception_handling(self):
        """Test exception handling in query execution."""
        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        with patch('provide.foundation.cli.commands.logs.query.search_logs') as mock_search, \
             patch('click') as mock_click:

            mock_search.side_effect = Exception("Connection failed")
            mock_client = Mock()

            result = _execute_and_display_query("SELECT * FROM logs", "1h", 100, "json", mock_client)

            assert result == 1
            mock_click.echo.assert_called_once_with("Query failed: Connection failed", err=True)

    def test_no_last_parameter_uses_default(self):
        """Test that None or empty last parameter uses default."""
        from provide.foundation.cli.commands.logs.query import _execute_and_display_query

        mock_response = Mock()
        mock_response.total = 0

        with patch('provide.foundation.cli.commands.logs.query.search_logs') as mock_search, \
             patch('provide.foundation.cli.commands.logs.query.click'):

            mock_search.return_value = mock_response
            mock_client = Mock()

            _execute_and_display_query("SELECT * FROM logs", "", 100, "json", mock_client)

            # Should use default "-1h" when last is empty
            mock_search.assert_called_once_with(
                sql="SELECT * FROM logs",
                start_time="-1h",
                end_time="now",
                size=100,
                client=mock_client
            )


@pytest.mark.skipif(
    not hasattr(__builtins__, '__dict__') or 'click' not in str(__builtins__),
    reason="click not available"
)
class TestQueryCommand:
    """Test the query_command click command."""

    def test_command_available_when_click_imported(self):
        """Test that command is available when click is imported."""
        from provide.foundation.cli.commands.logs.query import query_command, _HAS_CLICK

        if _HAS_CLICK:
            assert callable(query_command)
        else:
            pytest.skip("click not available")

    def test_command_with_no_client_configured(self):
        """Test command behavior when no client is configured."""
        from provide.foundation.cli.commands.logs.query import query_command, _HAS_CLICK

        if not _HAS_CLICK:
            pytest.skip("click not available")

        runner = CliRunner()

        # Create a mock context with no client
        with runner.isolated_filesystem():
            result = runner.invoke(query_command, [], obj={})

        assert result.exit_code == 1
        assert "Error: OpenObserve not configured." in result.output

    def test_command_with_custom_sql(self):
        """Test command with custom SQL query."""
        from provide.foundation.cli.commands.logs.query import query_command, _HAS_CLICK

        if not _HAS_CLICK:
            pytest.skip("click not available")

        runner = CliRunner()
        mock_client = Mock()

        with patch('provide.foundation.cli.commands.logs.query._execute_and_display_query') as mock_execute:
            mock_execute.return_value = 0

            result = runner.invoke(
                query_command,
                ['--sql', 'SELECT * FROM custom'],
                obj={'client': mock_client}
            )

        assert result.exit_code == 0
        mock_execute.assert_called_once()
        # Should call with the custom SQL
        args = mock_execute.call_args[0]
        assert args[0] == 'SELECT * FROM custom'


class TestQueryCommandWithoutClick:
    """Test query command behavior when click is not available."""

    def test_command_raises_import_error_without_click(self):
        """Test that command raises ImportError when click is not available."""
        # Mock the module to simulate click not being available
        with patch('provide.foundation.cli.commands.logs.query._HAS_CLICK', False):
            from provide.foundation.cli.commands.logs.query import query_command

            with pytest.raises(ImportError, match="CLI commands require optional dependencies"):
                query_command()


class TestValidationEdgeCases:
    """Test edge cases in validation logic."""

    def test_trace_id_uuid_format_valid(self):
        """Test that UUID format trace IDs are valid."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Standard UUID format should work
        uuid_trace = "550e8400-e29b-41d4-a716-446655440000"
        result = _build_query_sql(uuid_trace, None, None, "default", 100)
        assert f"trace_id = '{uuid_trace}'" in result

    def test_trace_id_hex_format_valid(self):
        """Test that hex format trace IDs are valid."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Hex format should work
        hex_trace = "abcdef1234567890"
        result = _build_query_sql(hex_trace, None, None, "default", 100)
        assert f"trace_id = '{hex_trace}'" in result

    def test_service_name_complex_valid(self):
        """Test complex but valid service names."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        # Complex service name with dots, hyphens, underscores
        service = "auth-service_v2.production"
        result = _build_query_sql(None, None, service, "default", 100)
        assert f"service = '{service}'" in result

    def test_stream_name_with_numbers(self):
        """Test stream names with numbers."""
        from provide.foundation.cli.commands.logs.query import _build_query_sql

        stream = "logs_stream_123"
        result = _build_query_sql(None, None, None, stream, 100)
        assert f"FROM {stream}" in result

    def test_boundary_size_values(self):
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