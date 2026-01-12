#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for formatting utilities."""

from provide.testkit import FoundationTestCase

from provide.foundation.formatting import (
    format_duration,
    format_number,
    format_percentage,
    format_size,
    format_table,
    indent,
    pluralize,
    strip_ansi,
    to_camel_case,
    to_kebab_case,
    to_snake_case,
    truncate,
    wrap_text,
)


class TestSizeFormatting(FoundationTestCase):
    """Test size formatting."""

    def test_format_size_bytes(self) -> None:
        """Test formatting bytes."""
        assert format_size(0) == "0 B"
        assert format_size(1) == "1 B"
        assert format_size(999) == "999 B"
        assert format_size(1023) == "1023 B"

    def test_format_size_kilobytes(self) -> None:
        """Test formatting kilobytes."""
        assert format_size(1024) == "1.0 KB"
        assert format_size(1536) == "1.5 KB"
        assert format_size(2048) == "2.0 KB"
        assert format_size(1024 * 10) == "10.0 KB"

    def test_format_size_megabytes(self) -> None:
        """Test formatting megabytes."""
        assert format_size(1024 * 1024) == "1.0 MB"
        assert format_size(1024 * 1024 * 1.5) == "1.5 MB"
        assert format_size(1024 * 1024 * 100) == "100.0 MB"

    def test_format_size_gigabytes(self) -> None:
        """Test formatting gigabytes."""
        assert format_size(1024**3) == "1.0 GB"
        assert format_size(1024**3 * 2.5) == "2.5 GB"

    def test_format_size_terabytes(self) -> None:
        """Test formatting terabytes."""
        assert format_size(1024**4) == "1.0 TB"
        assert format_size(1024**4 * 5) == "5.0 TB"

    def test_format_size_precision(self) -> None:
        """Test precision control."""
        size = 1536  # 1.5 KB
        # With precision=0, 1.5 rounds to 2
        assert format_size(size, precision=0) == "2 KB"
        assert format_size(size, precision=1) == "1.5 KB"
        assert format_size(size, precision=2) == "1.50 KB"

    def test_format_size_negative(self) -> None:
        """Test negative sizes."""
        assert format_size(-1024) == "-1.0 KB"
        assert format_size(-1536) == "-1.5 KB"


class TestDurationFormatting(FoundationTestCase):
    """Test duration formatting."""

    def test_format_duration_seconds(self) -> None:
        """Test formatting seconds."""
        assert format_duration(0) == "0 seconds"
        assert format_duration(1) == "1 second"
        assert format_duration(30) == "30 seconds"
        assert format_duration(59) == "59 seconds"

    def test_format_duration_minutes(self) -> None:
        """Test formatting minutes."""
        assert format_duration(60) == "1 minute"
        assert format_duration(90) == "1 minute 30 seconds"
        assert format_duration(120) == "2 minutes"
        assert format_duration(121) == "2 minutes 1 second"

    def test_format_duration_hours(self) -> None:
        """Test formatting hours."""
        assert format_duration(3600) == "1 hour"
        assert format_duration(3661) == "1 hour 1 minute 1 second"
        assert format_duration(7200) == "2 hours"
        assert format_duration(3900) == "1 hour 5 minutes"

    def test_format_duration_days(self) -> None:
        """Test formatting days."""
        assert format_duration(86400) == "1 day"
        assert format_duration(86400 * 2) == "2 days"
        assert format_duration(86400 + 3600) == "1 day 1 hour"
        assert format_duration(86400 + 3661) == "1 day 1 hour 1 minute 1 second"

    def test_format_duration_short(self) -> None:
        """Test short format."""
        assert format_duration(0, short=True) == "0s"
        assert format_duration(1, short=True) == "1s"
        assert format_duration(60, short=True) == "1m"
        assert format_duration(90, short=True) == "1m30s"
        assert format_duration(3661, short=True) == "1h1m1s"
        assert format_duration(86400, short=True) == "1d"
        assert format_duration(90061, short=True) == "1d1h1m1s"

    def test_format_duration_negative(self) -> None:
        """Test negative durations."""
        assert format_duration(-60) == "-1 minute"
        assert format_duration(-90, short=True) == "-1m30s"

    def test_format_duration_components(self) -> None:
        """Test duration components helper function."""
        from provide.foundation.formatting.numbers import _format_duration_components

        # Test the tuple return from the helper function
        result = _format_duration_components(1, 2, 3, 4)
        assert result == (1, 2, 3, 4)

        # Test with zeros
        result = _format_duration_components(0, 0, 0, 30)
        assert result == (0, 0, 0, 30)


class TestNumberFormatting(FoundationTestCase):
    """Test number formatting."""

    def test_format_number_integers(self) -> None:
        """Test formatting integers."""
        assert format_number(0) == "0"
        assert format_number(1000) == "1,000"
        assert format_number(1234567) == "1,234,567"
        assert format_number(-1234567) == "-1,234,567"

    def test_format_number_floats(self) -> None:
        """Test formatting floats."""
        assert format_number(1234.5) == "1,234.5"
        assert format_number(1234.0) == "1,234"
        assert format_number(1234.56789) == "1,234.56789"

    def test_format_number_precision(self) -> None:
        """Test precision control."""
        assert format_number(1234.5678, precision=2) == "1,234.57"
        assert format_number(1234.5678, precision=0) == "1,235"
        assert format_number(1234, precision=2) == "1,234.00"


class TestPercentageFormatting(FoundationTestCase):
    """Test percentage formatting."""

    def test_format_percentage(self) -> None:
        """Test basic percentage formatting."""
        assert format_percentage(0.5) == "50.0%"
        assert format_percentage(0.1234) == "12.3%"
        assert format_percentage(1.0) == "100.0%"
        assert format_percentage(0.0) == "0.0%"
        assert format_percentage(-0.25) == "-25.0%"

    def test_format_percentage_precision(self) -> None:
        """Test precision control."""
        assert format_percentage(0.12345, precision=2) == "12.35%"
        assert format_percentage(0.12345, precision=0) == "12%"
        assert format_percentage(0.12345, precision=3) == "12.345%"

    def test_format_percentage_sign(self) -> None:
        """Test include_sign option."""
        assert format_percentage(0.05, include_sign=True) == "+5.0%"
        assert format_percentage(-0.05, include_sign=True) == "-5.0%"
        assert format_percentage(0.0, include_sign=True) == "0.0%"


class TestTextOperations(FoundationTestCase):
    """Test text manipulation operations."""

    def test_truncate(self) -> None:
        """Test text truncation."""
        assert truncate("Hello world", 20) == "Hello world"
        assert truncate("Hello world", 8) == "Hello..."
        assert truncate("Hello world", 8, suffix="…") == "Hello…"
        assert truncate("Hello world", 8, whole_words=False) == "Hello..."
        assert truncate("Hello beautiful world", 15) == "Hello..."
        assert truncate("Short", 3, suffix="...") == "..."

    def test_pluralize(self) -> None:
        """Test pluralization."""
        assert pluralize(0, "file") == "0 files"
        assert pluralize(1, "file") == "1 file"
        assert pluralize(2, "file") == "2 files"
        assert pluralize(1, "child", "children") == "1 child"
        assert pluralize(2, "child", "children") == "2 children"

    def test_indent(self) -> None:
        """Test text indentation."""
        assert indent("line1", 2) == "  line1"
        assert indent("line1\nline2", 2) == "  line1\n  line2"
        assert indent("line1\nline2", 4) == "    line1\n    line2"
        assert indent("line1\nline2", 2, first_line=False) == "line1\n  line2"
        assert indent("", 2) == ""

    def test_wrap_text(self) -> None:
        """Test text wrapping."""
        long_text = "This is a very long line that should be wrapped at the specified width"
        wrapped = wrap_text(long_text, width=20)
        lines = wrapped.split("\n")
        assert all(len(line) <= 20 for line in lines)
        assert len(lines) > 1

        # Test with indentation
        wrapped = wrap_text(long_text, width=30, indent_first=2, indent_rest=4)
        lines = wrapped.split("\n")
        assert lines[0].startswith("  ")
        if len(lines) > 1:
            assert lines[1].startswith("    ")

    def test_strip_ansi(self) -> None:
        """Test ANSI code stripping."""
        assert strip_ansi("plain text") == "plain text"
        assert strip_ansi("\x1b[31mred text\x1b[0m") == "red text"
        assert strip_ansi("\x1b[1;32mgreen bold\x1b[0m") == "green bold"
        assert strip_ansi("\x1b[31mred\x1b[0m \x1b[32mgreen\x1b[0m") == "red green"


class TestCaseConversion(FoundationTestCase):
    """Test case conversion functions."""

    def test_to_snake_case(self) -> None:
        """Test snake_case conversion."""
        assert to_snake_case("HelloWorld") == "hello_world"
        assert to_snake_case("some-kebab-case") == "some_kebab_case"
        assert to_snake_case("someVariableName") == "some_variable_name"
        assert to_snake_case("HTTPResponse") == "httpresponse"
        assert to_snake_case("already_snake_case") == "already_snake_case"

    def test_to_kebab_case(self) -> None:
        """Test kebab-case conversion."""
        assert to_kebab_case("HelloWorld") == "hello-world"
        assert to_kebab_case("some_snake_case") == "some-snake-case"
        assert to_kebab_case("someVariableName") == "some-variable-name"
        assert to_kebab_case("already-kebab-case") == "already-kebab-case"

    def test_to_camel_case(self) -> None:
        """Test camelCase conversion."""
        assert to_camel_case("hello_world") == "helloWorld"
        assert to_camel_case("hello-world") == "helloWorld"
        assert to_camel_case("hello world") == "helloWorld"
        assert to_camel_case("hello_world", upper_first=True) == "HelloWorld"
        assert to_camel_case("hello-world", upper_first=True) == "HelloWorld"
        assert to_camel_case("HELLO_WORLD") == "helloWorld"


class TestTableFormatting(FoundationTestCase):
    """Test table formatting."""

    def test_format_table_basic(self) -> None:
        """Test basic table formatting."""
        headers = ["Name", "Age"]
        rows = [["Alice", 30], ["Bob", 25]]
        table = format_table(headers, rows)
        lines = table.split("\n")

        assert len(lines) == 4  # Header + separator + 2 rows
        assert "Name" in lines[0]
        assert "Age" in lines[0]
        assert "---" in lines[1]
        assert "Alice" in lines[2]
        assert "30" in lines[2]
        assert "Bob" in lines[3]
        assert "25" in lines[3]

    def test_format_table_empty(self) -> None:
        """Test empty table."""
        assert format_table([], []) == ""

    def test_format_table_mixed_types(self) -> None:
        """Test table with mixed types."""
        headers = ["String", "Int", "Float", "Bool"]
        rows = [["test", 123, 45.67, True], ["another", 456, 89.01, False]]

        table = format_table(headers, rows)
        assert "test" in table
        assert "123" in table
        assert "45.67" in table
        assert "True" in table
        assert "False" in table


# 🧱🏗️🔚
