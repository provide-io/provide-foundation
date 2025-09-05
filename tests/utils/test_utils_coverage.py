"""
Additional tests for provide.foundation.utils to increase code coverage.
"""
import io
from typing import Any

from attrs import define, field, fields

from provide.foundation import LoggingConfig, TelemetryConfig, logger, setup_telemetry
from provide.foundation.utils import timed_block
from provide.foundation.utils.formatting import format_table, to_camel_case
from provide.foundation.utils.parsing import auto_parse, parse_typed_value


class TestCaseConversionCoverage:
    """Coverage for case conversion functions."""

    def test_to_camel_case_empty_string(self) -> None:
        """Test to_camel_case with an empty string."""
        assert to_camel_case("") == ""


class TestTableFormattingCoverage:
    """Coverage for table formatting edge cases."""

    def test_format_table_empty_rows(self) -> None:
        """Test format_table with headers but no rows."""
        headers = ["Header 1", "Header 2"]
        rows = []
        table = format_table(headers, rows)
        assert "Header 1" in table
        assert "Header 2" in table
        assert len(table.splitlines()) == 2  # Header and separator line

    def test_format_table_ragged_rows(self) -> None:
        """Test format_table with rows of different lengths."""
        headers = ["A", "B", "C"]
        rows = [["1", "2"], ["4", "5", "6"]]
        table = format_table(headers, rows)
        # Should not raise an error and should format correctly
        assert "1" in table
        assert "2" in table
        assert "6" in table

    def test_format_table_alignment_mismatch(self) -> None:
        """Test format_table with more alignment options than headers."""
        headers = ["A", "B"]
        rows = [["1", "2"]]
        table = format_table(headers, rows, alignment=["l", "c", "r"])
        assert "1" in table
        assert "2" in table

    def test_format_table_no_headers_or_rows(self) -> None:
        """Test format_table with no headers and no rows."""
        assert format_table([], []) == ""


class TestParsingCoverage:
    """Coverage for parsing utility functions."""

    def test_parse_typed_value_unsupported_origin(self) -> None:
        """Test parse_typed_value with a type origin it doesn't handle."""
        # It should fall back to returning the original string value.
        result = parse_typed_value("some_value", set)
        assert result == "some_value"

    def test_auto_parse_with_string_type_hints(self) -> None:
        """Test auto_parse for attrs fields with string type hints."""
        @define
        class DummyConfig:
            int_val: 'int'
            bool_val: 'bool'
            list_val: 'list'
            dict_val: 'dict'
            unknown_val: 'SomeUnknownType'

        attrs_fields = {f.name: f for f in fields(DummyConfig)}

        assert auto_parse(attrs_fields['int_val'], "42") == 42
        assert auto_parse(attrs_fields['bool_val'], "true") is True
        assert auto_parse(attrs_fields['list_val'], "a,b") == ["a", "b"]
        assert auto_parse(attrs_fields['dict_val'], "k=v") == {"k": "v"}
        assert auto_parse(attrs_fields['unknown_val'], "some_string") == "some_string"

    def test_auto_parse_no_type_hint(self) -> None:
        """Test auto_parse for an attrs field with no type hint."""
        @define
        class NoTypeHintConfig:
            val: Any = field()

        no_type_field = fields(NoTypeHintConfig).val
        assert auto_parse(no_type_field, "a_string") == "a_string"


class TestTimingCoverage:
    """Coverage for timing utility functions."""

    def test_timed_block_context_modification(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that modifying the context dict within a timed_block works."""
        setup_telemetry(TelemetryConfig())

        with timed_block(logger, "test_op") as ctx:
            ctx["records"] = 100
            ctx["status_custom"] = "success" # Use a non-special key

        output = captured_stderr_for_foundation.getvalue()
        # Verify that the modifications to the context dict are present in the final log.
        assert "records=100" in output
        assert "status_custom=success" in output
        assert "outcome=success" in output

    def test_timed_block_debug_message(self, captured_stderr_for_foundation: io.StringIO) -> None:
        """Test that the initial debug message is logged when level is DEBUG."""
        setup_telemetry(TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")))

        with timed_block(logger, "debug_test_op"):
            pass

        output = captured_stderr_for_foundation.getvalue()
        # Check for both the "started" and "completed" messages
        assert "debug_test_op started" in output
        assert "debug_test_op completed" in output
