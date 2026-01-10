#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Additional tests for provide.foundation.utils to increase code coverage."""

from __future__ import annotations

import io
from typing import Any

from attrs import define, field, fields
from provide.testkit import FoundationTestCase

from provide.foundation import LoggingConfig, TelemetryConfig, get_hub, logger
from provide.foundation.formatting import format_table, to_camel_case
from provide.foundation.parsers import auto_parse, parse_typed_value
from provide.foundation.utils import timed_block


class TestCaseConversionCoverage(FoundationTestCase):
    """Coverage for case conversion functions."""

    def test_to_camel_case_empty_string(self) -> None:
        """Test to_camel_case with an empty string."""
        assert to_camel_case("") == ""


class TestTableFormattingCoverage(FoundationTestCase):
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


class TestParsingCoverage(FoundationTestCase):
    """Coverage for parsing utility functions."""

    def test_parse_typed_value_unsupported_origin(self) -> None:
        """Test parse_typed_value with a type origin it doesn't handle."""
        # It should fall back to returning the original string value.
        # Using frozenset as it's not currently supported
        result = parse_typed_value("some_value", frozenset)
        assert result == "some_value"

    def test_auto_parse_with_string_type_hints(self) -> None:
        """Test auto_parse for attrs fields with normal type hints."""

        @define
        class DummyConfig:
            int_val: int
            bool_val: bool
            list_val: list
            dict_val: dict
            unknown_val: str

        attrs_fields = {f.name: f for f in fields(DummyConfig)}

        # Type hints trigger appropriate parsing
        assert auto_parse(attrs_fields["int_val"], "42") == 42
        assert auto_parse(attrs_fields["bool_val"], "true") is True
        assert auto_parse(attrs_fields["list_val"], "a,b") == ["a", "b"]
        assert auto_parse(attrs_fields["dict_val"], "k=v") == {"k": "v"}
        assert auto_parse(attrs_fields["unknown_val"], "some_string") == "some_string"

    def test_auto_parse_no_type_hint(self) -> None:
        """Test auto_parse for an attrs field with no type hint."""

        @define
        class NoTypeHintConfig:
            val: Any = field()

        no_type_field = fields(NoTypeHintConfig).val
        assert auto_parse(no_type_field, "a_string") == "a_string"

    def test_auto_parse_with_converter_metadata(self) -> None:
        """Test auto_parse uses converter from metadata first."""

        @define
        class ConfigWithConverter:
            uppercase_val: str = field(metadata={"converter": lambda x: x.upper()})
            int_val: int = field(metadata={"converter": lambda x: int(x) * 2})
            no_converter: str = field()

        attrs_fields = {f.name: f for f in fields(ConfigWithConverter)}

        # Test that converter in metadata is used
        assert auto_parse(attrs_fields["uppercase_val"], "hello") == "HELLO"
        assert auto_parse(attrs_fields["int_val"], "5") == 10

        # Test fallback to type-based parsing when no converter
        assert auto_parse(attrs_fields["no_converter"], "plain") == "plain"

    def test_auto_parse_converter_fallback(self) -> None:
        """Test auto_parse falls back to type parsing if converter fails."""

        @define
        class ConfigWithFailingConverter:
            # Converter that always fails
            val: int = field(metadata={"converter": lambda x: int(x[100])})

        failing_field = fields(ConfigWithFailingConverter).val

        # Should fall back to type-based parsing when converter fails
        assert auto_parse(failing_field, "42") == 42


class TestTimingCoverage(FoundationTestCase):
    """Coverage for timing utility functions."""

    def test_timed_block_context_modification(
        self,
        captured_stderr_for_foundation: io.StringIO,
    ) -> None:
        """Test that modifying the context dict within a timed_block works."""
        from provide.foundation.logger.config.logging import LoggingConfig

        config = TelemetryConfig(logging=LoggingConfig(default_level="INFO"))
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        with timed_block(logger, "test_op") as ctx:
            ctx["records"] = 100
            ctx["status_custom"] = "success"  # Use a non-special key

        output = captured_stderr_for_foundation.getvalue()
        # Verify that the modifications to the context dict are present in the final log.
        assert "records=100" in output
        assert "status_custom=success" in output
        assert "outcome=success" in output

    def test_timed_block_debug_message(
        self,
        captured_stderr_for_foundation: io.StringIO,
    ) -> None:
        """Test that the initial debug message is logged when level is DEBUG."""
        hub = get_hub()
        hub.initialize_foundation(TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")), force=True)

        with timed_block(logger, "debug_test_op"):
            pass

        output = captured_stderr_for_foundation.getvalue()
        # Check for both the "started" and "completed" messages
        assert "debug_test_op started" in output
        assert "debug_test_op completed" in output


class TestEnvUtilsCoverage(FoundationTestCase):
    """Coverage for environment utilities."""

    def test_get_bool_edge_cases(self) -> None:
        """Test edge cases for get_bool function."""
        import os

        from provide.testkit.mocking import patch

        from provide.foundation.errors.config import ValidationError
        from provide.foundation.utils.environment import get_bool

        # Test with empty string (returns None with warning)
        with patch.dict(os.environ, {"TEST_BOOL": ""}):
            assert get_bool("TEST_BOOL") is None

        # Test with whitespace
        with patch.dict(os.environ, {"TEST_BOOL": "  true  "}):
            assert get_bool("TEST_BOOL") is True

        # Test invalid value raises ValidationError
        with patch.dict(os.environ, {"TEST_BOOL": "invalid"}):
            try:
                get_bool("TEST_BOOL")
                raise AssertionError("Should have raised ValidationError")
            except ValidationError as e:
                assert "Invalid boolean value" in str(e)

    def test_get_int_edge_cases(self) -> None:
        """Test edge cases for get_int function."""
        import os

        from provide.testkit.mocking import patch

        from provide.foundation.errors.config import ValidationError
        from provide.foundation.utils.environment import get_int

        # Test negative numbers
        with patch.dict(os.environ, {"TEST_INT": "-42"}):
            assert get_int("TEST_INT") == -42

        # Test zero
        with patch.dict(os.environ, {"TEST_INT": "0"}):
            assert get_int("TEST_INT") == 0

        # Test invalid value raises ValidationError
        with patch.dict(os.environ, {"TEST_INT": "not_a_number"}):
            try:
                get_int("TEST_INT")
                raise AssertionError("Should have raised ValidationError")
            except ValidationError as e:
                assert "Invalid integer value" in str(e)

    def test_get_float_edge_cases(self) -> None:
        """Test edge cases for get_float function."""
        import os

        from provide.testkit.mocking import patch

        from provide.foundation.errors.config import ValidationError
        from provide.foundation.utils.environment import get_float

        # Test scientific notation
        with patch.dict(os.environ, {"TEST_FLOAT": "1e-3"}):
            assert get_float("TEST_FLOAT") == 0.001

        # Test negative float
        with patch.dict(os.environ, {"TEST_FLOAT": "-3.14"}):
            assert get_float("TEST_FLOAT") == -3.14

        # Test invalid value
        with patch.dict(os.environ, {"TEST_FLOAT": "not_a_float"}):
            try:
                get_float("TEST_FLOAT")
                raise AssertionError("Should have raised ValidationError")
            except ValidationError as e:
                assert "Invalid float value" in str(e)

    def test_get_str_with_default(self) -> None:
        """Test get_str with default value."""
        import os

        from provide.testkit.mocking import patch

        from provide.foundation.utils.environment import get_str

        # Test with missing env var (should use default)
        result = get_str("NON_EXISTENT_STR", default="default_value")
        assert result == "default_value"

        # Test with existing env var
        with patch.dict(os.environ, {"TEST_STR": "actual_value"}):
            result = get_str("TEST_STR", default="default_value")
            assert result == "actual_value"


# 🧱🏗️🔚
