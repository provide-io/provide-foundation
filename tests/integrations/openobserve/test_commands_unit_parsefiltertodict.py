"""Unit tests for OpenObserve CLI commands.

This module contains unit tests for CLI command functionality with mocked dependencies.
Run with: pytest tests/integrations/openobserve/test_commands_unit.py -v
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from provide.testkit import FoundationTestCase

from provide.foundation.integrations.openobserve.commands import _parse_filter_to_dict


class TestParseFilterToDict(FoundationTestCase):
    """Tests for _parse_filter_to_dict helper function."""

    def test_parse_single_filter(self) -> None:
        """Test parsing single filter."""
        result = _parse_filter_to_dict("level=ERROR")
        assert result == {"level": "ERROR"}

    def test_parse_single_filter_with_quotes(self) -> None:
        """Test parsing filter with single quotes."""
        result = _parse_filter_to_dict("level='ERROR'")
        assert result == {"level": "ERROR"}

    def test_parse_single_filter_with_double_quotes(self) -> None:
        """Test parsing filter with double quotes."""
        result = _parse_filter_to_dict('level="ERROR"')
        assert result == {"level": "ERROR"}

    def test_parse_multiple_filters(self) -> None:
        """Test parsing multiple comma-separated filters."""
        result = _parse_filter_to_dict("level=ERROR,service=api")
        assert result == {"level": "ERROR", "service": "api"}

    def test_parse_multiple_filters_with_spaces(self) -> None:
        """Test parsing filters with spaces."""
        result = _parse_filter_to_dict("level = ERROR , service = api")
        assert result == {"level": "ERROR", "service": "api"}

    def test_parse_filter_with_value_containing_spaces(self) -> None:
        """Test parsing filter with spaces in value."""
        result = _parse_filter_to_dict("message=error occurred")
        assert result == {"message": "error occurred"}

    def test_parse_empty_filter_string(self) -> None:
        """Test parsing empty string returns empty dict."""
        result = _parse_filter_to_dict("")
        assert result == {}

    def test_parse_filter_with_underscore_in_key(self) -> None:
        """Test parsing filter with underscore in key name."""
        result = _parse_filter_to_dict("log_level=ERROR")
        assert result == {"log_level": "ERROR"}

    def test_parse_filter_with_numbers_in_key(self) -> None:
        """Test parsing filter with numbers in key name."""
        result = _parse_filter_to_dict("http_status_code=500")
        assert result == {"http_status_code": "500"}


# Only test CLI commands if click is available
if _HAS_CLICK:
    from provide.foundation.integrations.openobserve.commands import openobserve_group

    class TestOpenObserveGroupCommand(FoundationTestCase):
        """Tests for openobserve CLI group command."""

        def test_openobserve_group_initialization_success(self) -> None:
            """Test openobserve group initializes client successfully."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_client = MagicMock()
                mock_from_config.return_value = mock_client

                result = runner.invoke(openobserve_group, ["--help"])

                assert result.exit_code == 0
                assert "Query and manage OpenObserve logs" in result.output

        def test_openobserve_group_initialization_failure(self) -> None:
            """Test openobserve group handles client initialization failure."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_from_config.side_effect = ValueError("Config error")

                # Help should still work even if client init fails
                result = runner.invoke(openobserve_group, ["--help"])
                assert result.exit_code == 0

    class TestQueryCommand(FoundationTestCase):
        """Tests for query command."""

        def test_query_command_success(self) -> None:
            """Test successful query execution."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.hits = [{"message": "test log"}]
            mock_response.total = 1

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.format_output",
                    return_value="formatted output",
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 0
                assert "formatted output" in result.output

        def test_query_command_no_client(self) -> None:
            """Test query command when client is not configured."""
            runner = CliRunner()

            with patch(
                "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config"
            ) as mock_from_config:
                mock_from_config.side_effect = ValueError("Config error")

                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 1
                assert "not configured" in result.output

        def test_query_command_failure(self) -> None:
            """Test query command when query fails."""
            runner = CliRunner()

            mock_client = MagicMock()

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch("provide.foundation.integrations.openobserve.commands.run_async") as mock_run_async,
            ):
                mock_run_async.side_effect = ValueError("Query failed")

                result = runner.invoke(
                    openobserve_group,
                    ["query", "--sql", "SELECT * FROM logs"],
                )

                assert result.exit_code == 1
                assert "Query failed" in result.output

    class TestTailCommand(FoundationTestCase):
        """Tests for tail command."""

        def test_tail_command_success(self) -> None:
            """Test successful tail execution."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> list[dict]:
                return [{"message": "log1"}, {"message": "log2"}]

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["tail", "--stream", "default", "--follow=False"],
                )

                assert result.exit_code == 0

        def test_tail_command_with_filter(self) -> None:
            """Test tail command with filter."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> list[dict]:
                return []

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    [
                        "tail",
                        "--stream",
                        "default",
                        "--filter",
                        "level=ERROR",
                        "--follow=False",
                    ],
                )

                assert result.exit_code == 0

        def test_tail_command_keyboard_interrupt(self) -> None:
            """Test tail command handles keyboard interrupt."""
            runner = CliRunner()

            mock_client = MagicMock()

            def mock_tail_logs(*args: object, **kwargs: object) -> None:
                raise KeyboardInterrupt()
                if False:  # Make it a generator
                    yield {}

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.tail_logs",
                    side_effect=mock_tail_logs,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["tail", "--stream", "default"],
                )

                assert result.exit_code == 0
                assert "Stopped tailing" in result.output

    class TestStreamsCommand(FoundationTestCase):
        """Tests for streams command."""

        def test_streams_command_success(self) -> None:
            """Test successful streams listing."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_stream = MagicMock()
            mock_stream.name = "test_stream"
            mock_stream.stream_type = "logs"
            mock_stream.doc_count = 100
            mock_stream.original_size = 1024

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=[mock_stream],
                ),
            ):
                result = runner.invoke(openobserve_group, ["streams"])

                assert result.exit_code == 0
                assert "Available streams" in result.output
                assert "test_stream" in result.output

        def test_streams_command_no_streams(self) -> None:
            """Test streams command when no streams exist."""
            runner = CliRunner()

            mock_client = MagicMock()

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=[],
                ),
            ):
                result = runner.invoke(openobserve_group, ["streams"])

                assert result.exit_code == 0
                assert "No streams found" in result.output

    class TestTestCommand(FoundationTestCase):
        """Tests for test command."""

        def test_test_command_success(self) -> None:
            """Test successful connection test."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_client.url = "http://localhost:5080"
            mock_client.organization = "default"
            mock_client.username = "test@example.com"

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=True,
                ),
            ):
                result = runner.invoke(openobserve_group, ["test"])

                assert result.exit_code == 0
                assert "Connection successful" in result.output

        def test_test_command_failure(self) -> None:
            """Test failed connection test."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_client.url = "http://localhost:5080"

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=False,
                ),
            ):
                result = runner.invoke(openobserve_group, ["test"])

                assert result.exit_code == 1
                assert "Connection failed" in result.output

    class TestHistoryCommand(FoundationTestCase):
        """Tests for history command."""

        def test_history_command_success(self) -> None:
            """Test successful history retrieval."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 2
            mock_response.hits = [
                {"sql": "SELECT * FROM logs", "took": 10.5, "scan_records": 100},
                {"sql": "SELECT * FROM errors", "took": 5.2, "scan_records": 50},
            ]

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(openobserve_group, ["history"])

                assert result.exit_code == 0
                assert "Search history" in result.output

        def test_history_command_no_history(self) -> None:
            """Test history command when no history exists."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0
            mock_response.hits = []

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(openobserve_group, ["history"])

                assert result.exit_code == 0
                assert "No search history found" in result.output

    class TestErrorsCommand(FoundationTestCase):
        """Tests for errors command."""

        def test_errors_command_success(self) -> None:
            """Test successful errors search."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 5

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.format_output",
                    return_value="error logs",
                ),
            ):
                result = runner.invoke(openobserve_group, ["errors"])

                assert result.exit_code == 0

        def test_errors_command_no_errors(self) -> None:
            """Test errors command when no errors found."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(openobserve_group, ["errors"])

                assert result.exit_code == 0
                assert "No errors found" in result.output

    class TestTraceCommand(FoundationTestCase):
        """Tests for trace command."""

        def test_trace_command_success(self) -> None:
            """Test successful trace search."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 3

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.format_output",
                    return_value="trace logs",
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["trace", "abc123"],
                )

                assert result.exit_code == 0

        def test_trace_command_not_found(self) -> None:
            """Test trace command when trace not found."""
            runner = CliRunner()

            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.total = 0

            with (
                patch(
                    "provide.foundation.integrations.openobserve.commands.OpenObserveClient.from_config",
                    return_value=mock_client,
                ),
                patch(
                    "provide.foundation.integrations.openobserve.commands.run_async",
                    return_value=mock_response,
                ),
            ):
                result = runner.invoke(
                    openobserve_group,
                    ["trace", "abc123"],
                )

                assert result.exit_code == 0
                assert "No logs found" in result.output


else:
    # Placeholder when click is not available
    class TestCommandsNotAvailable(FoundationTestCase):
        """Test that commands are not available when click is missing."""

        def test_commands_require_click(self) -> None:
            """Test that click is required for CLI commands."""
            # Just verify that the module doesn't crash without click
            assert not _HAS_CLICK


__all__ = [
    "TestParseFilterToDict",
]
