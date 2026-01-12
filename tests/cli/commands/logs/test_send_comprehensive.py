#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for CLI logs send command."""

from __future__ import annotations

from io import StringIO

from provide.testkit.mocking import patch


class TestGetMessageFromInput:
    """Test _get_message_from_input function."""

    def test_message_provided_returns_message(self) -> None:
        """Test that when message is provided, returns it directly."""
        from provide.foundation.cli.commands.logs.send import _get_message_from_input

        result_msg, result_code = _get_message_from_input("Test message")
        assert result_msg == "Test message"
        assert result_code == 0

    def test_no_message_tty_returns_error(self) -> None:
        """Test that when no message and stdin is tty, returns error."""
        from provide.foundation.cli.commands.logs.send import _get_message_from_input

        with patch("sys.stdin.isatty", return_value=True), patch("click.echo") as mock_echo:
            result_msg, result_code = _get_message_from_input(None)

            assert result_msg is None
            assert result_code == 1
            mock_echo.assert_called_once_with("Error: No message provided. Use -m or pipe input.", err=True)

    def test_stdin_message_success(self) -> None:
        """Test reading message from stdin successfully."""
        from provide.foundation.cli.commands.logs.send import _get_message_from_input

        stdin_content = "Message from stdin"
        mock_stdin = StringIO(stdin_content)

        with patch("sys.stdin", mock_stdin), patch("sys.stdin.isatty", return_value=False):
            result_msg, result_code = _get_message_from_input(None)

            assert result_msg == "Message from stdin"
            assert result_code == 0

    def test_empty_stdin_returns_error(self) -> None:
        """Test that empty stdin returns error."""
        from provide.foundation.cli.commands.logs.send import _get_message_from_input

        mock_stdin = StringIO("   \n  ")  # Only whitespace

        with (
            patch("sys.stdin", mock_stdin),
            patch("sys.stdin.isatty", return_value=False),
            patch("click.echo") as mock_echo,
        ):
            result_msg, result_code = _get_message_from_input(None)

            assert result_msg is None
            assert result_code == 1
            mock_echo.assert_called_once_with("Error: Empty input from stdin.", err=True)


class TestBuildAttributes:
    """Test _build_attributes function."""

    def test_no_attributes_returns_empty_dict(self) -> None:
        """Test that no attributes returns empty dict."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        result_attrs, result_code = _build_attributes(None, ())
        assert result_attrs == {}
        assert result_code == 0

    def test_valid_json_attributes(self) -> None:
        """Test parsing valid JSON attributes."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        json_attrs = '{"key1": "value1", "key2": 123, "key3": true}'
        result_attrs, result_code = _build_attributes(json_attrs, ())

        assert result_attrs == {"key1": "value1", "key2": 123, "key3": True}
        assert result_code == 0

    def test_invalid_json_attributes(self) -> None:
        """Test handling invalid JSON attributes."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        json_attrs = '{"key1": invalid_json}'
        with patch("click.echo") as mock_echo:
            result_attrs, result_code = _build_attributes(json_attrs, ())

            assert result_attrs == {}
            assert result_code == 1
            assert "Error: Invalid JSON attributes:" in mock_echo.call_args[0][0]

    def test_key_value_attributes_strings(self) -> None:
        """Test parsing key=value attributes as strings."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("key1=value1", "key2=value2")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"key1": "value1", "key2": "value2"}
        assert result_code == 0

    def test_key_value_attributes_boolean_true(self) -> None:
        """Test parsing boolean true values."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("bool1=true", "bool2=True")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"bool1": True, "bool2": True}
        assert result_code == 0

    def test_key_value_attributes_boolean_false(self) -> None:
        """Test parsing boolean false values."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("bool1=false", "bool2=False")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"bool1": False, "bool2": False}
        assert result_code == 0

    def test_key_value_attributes_integers(self) -> None:
        """Test parsing integer values."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("count=123", "age=0", "negative=-456")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"count": 123, "age": 0, "negative": "-456"}  # negative handled as string
        assert result_code == 0

    def test_key_value_attributes_floats(self) -> None:
        """Test parsing float values."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("price=99.99", "rate=0.05")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"price": 99.99, "rate": 0.05}
        assert result_code == 0

    def test_key_value_attributes_mixed_types(self) -> None:
        """Test parsing mixed attribute types."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("name=John", "count=42", "active=true", "score=98.5")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        expected = {"name": "John", "count": 42, "active": True, "score": 98.5}
        assert result_attrs == expected
        assert result_code == 0

    def test_invalid_key_value_format(self) -> None:
        """Test handling invalid key=value format."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("valid=value", "invalid_no_equals")
        with patch("click.echo") as mock_echo:
            result_attrs, result_code = _build_attributes(None, attr_pairs)

            assert result_attrs == {}
            assert result_code == 1
            mock_echo.assert_called_once_with(
                "Error: Invalid attribute format 'invalid_no_equals'. Use key=value.", err=True
            )

    def test_json_and_key_value_combined(self) -> None:
        """Test combining JSON and key=value attributes."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        json_attrs = '{"from_json": "value1"}'
        attr_pairs = ("from_kv=value2",)

        result_attrs, result_code = _build_attributes(json_attrs, attr_pairs)

        expected = {"from_json": "value1", "from_kv": "value2"}
        assert result_attrs == expected
        assert result_code == 0

    def test_key_value_overrides_json(self) -> None:
        """Test that key=value pairs override JSON attributes."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        json_attrs = '{"shared_key": "json_value"}'
        attr_pairs = ("shared_key=kv_value",)

        result_attrs, result_code = _build_attributes(json_attrs, attr_pairs)

        # Key=value should override JSON
        expected = {"shared_key": "kv_value"}
        assert result_attrs == expected
        assert result_code == 0


class TestSendLogEntry:
    """Test _send_log_entry function."""

    def test_send_success(self) -> None:
        """Test successful log sending via logger."""
        from provide.foundation.cli.commands.logs.send import _send_log_entry

        with (
            patch("provide.foundation.cli.commands.logs.send.get_logger") as mock_get_logger,
            patch("provide.foundation.cli.commands.logs.send.pout") as mock_pout,
        ):
            mock_logger = mock_get_logger.return_value
            mock_info = mock_logger.info

            result_code = _send_log_entry(
                message="Test message",
                level="INFO",
                service_name="test-service",
                attributes={"key": "value"},
                trace_id="trace123",
                span_id="span456",
            )

            assert result_code == 0
            mock_get_logger.assert_called_once_with("test-service")
            # The implementation adds trace_id and span_id to attributes
            mock_info.assert_called_once_with(
                "Test message",
                key="value",
                trace_id="trace123",
                span_id="span456",
            )
            mock_pout.assert_called_once_with("✓ Log sent successfully", color="green")

    def test_send_exception_handling(self) -> None:
        """Test exception handling for log sending."""
        from provide.foundation.cli.commands.logs.send import _send_log_entry

        with (
            patch(
                "provide.foundation.cli.commands.logs.send.get_logger",
                side_effect=Exception("Logger connection failed"),
            ),
            patch("provide.foundation.cli.commands.logs.send.perr") as mock_perr,
        ):
            result_code = _send_log_entry(
                message="Test message",
                level="INFO",
                service_name=None,
                attributes={},
                trace_id=None,
                span_id=None,
            )

            assert result_code == 1
            mock_perr.assert_called_once_with("✗ Failed to send log: Logger connection failed", color="red")


class TestModuleStructure:
    """Test basic module structure and imports."""

    def test_module_has_required_functions(self) -> None:
        """Test that module has all required functions."""
        from provide.foundation.cli.commands.logs import send

        assert hasattr(send, "_get_message_from_input")
        assert hasattr(send, "_send_log_entry")
        assert hasattr(send, "send_command")

        # _build_attributes was moved to cli.helpers
        from provide.foundation import cli

        assert hasattr(cli.helpers, "build_attributes_from_args")

    def test_module_uses_get_logger(self) -> None:
        """Test that module uses get_logger function."""
        from provide.foundation.cli.commands.logs import send

        # Module should have access to get_logger via import
        assert hasattr(send, "get_logger")
        # The actual logging is done through dynamically created loggers
        # via get_logger() rather than a module-level log variable


class TestEdgeCases:
    """Test various edge cases."""

    def test_build_attributes_with_equals_in_value(self) -> None:
        """Test key=value parsing when value contains equals sign."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        attr_pairs = ("url=https://example.com?a=1&b=2",)
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        assert result_attrs == {"url": "https://example.com?a=1&b=2"}
        assert result_code == 0

    def test_build_attributes_float_edge_cases(self) -> None:
        """Test float parsing edge cases."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        # Test various float formats
        attr_pairs = ("float1=123.0", "float2=0.5", "not_float=123.abc")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        # 123.abc should not be parsed as float
        expected = {"float1": 123.0, "float2": 0.5, "not_float": "123.abc"}
        assert result_attrs == expected
        assert result_code == 0

    def test_stdin_with_newlines(self) -> None:
        """Test stdin input with newlines gets stripped."""
        from provide.foundation.cli.commands.logs.send import _get_message_from_input

        stdin_content = "\n  Message with newlines  \n\n"
        mock_stdin = StringIO(stdin_content)

        with patch("sys.stdin", mock_stdin), patch("sys.stdin.isatty", return_value=False):
            result_msg, result_code = _get_message_from_input(None)

            assert result_msg == "Message with newlines"
            assert result_code == 0

    def test_negative_float_parsing(self) -> None:
        """Test parsing negative numbers."""
        from provide.foundation.cli.helpers import build_attributes_from_args as _build_attributes

        # Test how negative numbers are actually parsed by the code
        attr_pairs = ("negative_float=-123.45", "negative_int=-123")
        result_attrs, result_code = _build_attributes(None, attr_pairs)

        # negative_float should be parsed as float, negative_int as string (no dot)
        expected = {"negative_float": -123.45, "negative_int": "-123"}
        assert result_attrs == expected
        assert result_code == 0


# 🧱🏗️🔚
