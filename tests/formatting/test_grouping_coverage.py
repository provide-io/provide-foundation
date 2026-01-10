#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive tests for formatting/grouping.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.formatting.grouping import format_grouped


class TestFormatGrouped(FoundationTestCase):
    """Test format_grouped function."""

    def test_format_grouped_basic(self) -> None:
        """Test basic grouping functionality."""
        result = format_grouped("1234567890abcdef", group_size=4)
        assert result == "1234 5678 90ab cdef"

    def test_format_grouped_custom_separator(self) -> None:
        """Test with custom separator."""
        result = format_grouped("abc123def456", group_size=4, separator="-")
        assert result == "abc1-23de-f456"

    def test_format_grouped_custom_groups(self) -> None:
        """Test with limited number of groups."""
        result = format_grouped("abc123def456", group_size=4, groups=2)
        assert result == "abc1 23de"

    def test_format_grouped_empty_string(self) -> None:
        """Test with empty string."""
        result = format_grouped("", group_size=4)
        assert result == ""

    def test_format_grouped_single_character(self) -> None:
        """Test with single character."""
        result = format_grouped("a", group_size=4)
        assert result == "a"

    def test_format_grouped_exact_group_size(self) -> None:
        """Test with text exactly matching group size."""
        result = format_grouped("abcd", group_size=4)
        assert result == "abcd"

    def test_format_grouped_multiple_exact_groups(self) -> None:
        """Test with text exactly matching multiple groups."""
        result = format_grouped("abcdefgh", group_size=4)
        assert result == "abcd efgh"

    def test_format_grouped_group_size_one(self) -> None:
        """Test with group size of 1."""
        result = format_grouped("abc", group_size=1)
        assert result == "a b c"

    def test_format_grouped_group_size_larger_than_text(self) -> None:
        """Test with group size larger than text length."""
        result = format_grouped("abc", group_size=10)
        assert result == "abc"

    def test_format_grouped_invalid_group_size_zero(self) -> None:
        """Test with group size of 0."""
        result = format_grouped("abcdef", group_size=0)
        assert result == "abcdef"  # Returns original text

    def test_format_grouped_invalid_group_size_negative(self) -> None:
        """Test with negative group size."""
        result = format_grouped("abcdef", group_size=-1)
        assert result == "abcdef"  # Returns original text

    def test_format_grouped_groups_zero(self) -> None:
        """Test with groups=0 (show all groups)."""
        result = format_grouped("123456789", group_size=3, groups=0)
        assert result == "123 456 789"

    def test_format_grouped_groups_one(self) -> None:
        """Test with groups=1 (show only first group)."""
        result = format_grouped("123456789", group_size=3, groups=1)
        assert result == "123"

    def test_format_grouped_groups_more_than_available(self) -> None:
        """Test with groups more than available."""
        result = format_grouped("123456", group_size=3, groups=5)
        assert result == "123 456"  # Only 2 groups available

    def test_format_grouped_custom_separator_empty(self) -> None:
        """Test with empty separator."""
        result = format_grouped("abcdef", group_size=2, separator="")
        assert result == "abcdef"

    def test_format_grouped_custom_separator_multiple_chars(self) -> None:
        """Test with multi-character separator."""
        result = format_grouped("abcdef", group_size=2, separator=" | ")
        assert result == "ab | cd | ef"

    def test_format_grouped_special_characters(self) -> None:
        """Test with special characters in text."""
        result = format_grouped("!@#$%^&*()", group_size=3)
        assert result == "!@# $%^ &*( )"

    def test_format_grouped_unicode_characters(self) -> None:
        """Test with unicode characters."""
        result = format_grouped("αβγδεζηθ", group_size=2)
        assert result == "αβ γδ εζ ηθ"

    def test_format_grouped_numbers_as_string(self) -> None:
        """Test with numeric strings."""
        result = format_grouped("1234567890", group_size=3, separator=",")
        assert result == "123,456,789,0"

    def test_format_grouped_mixed_alphanumeric(self) -> None:
        """Test with mixed alphanumeric strings."""
        result = format_grouped("abc123XYZ789", group_size=4, separator="-")
        assert result == "abc1-23XY-Z789"

    def test_format_grouped_whitespace_in_text(self) -> None:
        """Test with whitespace in original text."""
        result = format_grouped("ab cd ef", group_size=3)
        assert result == "ab  cd  ef"

    def test_format_grouped_newlines_in_text(self) -> None:
        """Test with newlines in original text."""
        result = format_grouped("ab\ncd\nef", group_size=2)
        assert result == "ab \nc d\n ef"

    def test_format_grouped_tabs_in_text(self) -> None:
        """Test with tabs in original text."""
        result = format_grouped("ab\tcd\tef", group_size=2)
        assert result == "ab \tc d\t ef"

    def test_format_grouped_very_long_string(self) -> None:
        """Test with very long string."""
        long_string = "a" * 100
        result = format_grouped(long_string, group_size=10, groups=3)
        assert result == "aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa"

    def test_format_grouped_edge_case_partial_last_group(self) -> None:
        """Test edge case with partial last group."""
        result = format_grouped("12345", group_size=3)
        assert result == "123 45"

    def test_format_grouped_groups_exactly_available(self) -> None:
        """Test with groups exactly matching available groups."""
        result = format_grouped("123456", group_size=2, groups=3)
        assert result == "12 34 56"

    def test_format_grouped_separator_special_chars(self) -> None:
        """Test with special character separators."""
        result = format_grouped("abcdef", group_size=2, separator="★")
        assert result == "ab★cd★ef"

    def test_format_grouped_different_group_sizes(self) -> None:
        """Test with various group sizes."""
        text = "1234567890"

        # Group size 2
        result = format_grouped(text, group_size=2)
        assert result == "12 34 56 78 90"

        # Group size 5
        result = format_grouped(text, group_size=5)
        assert result == "12345 67890"

    def test_format_grouped_combination_parameters(self) -> None:
        """Test combination of all parameters."""
        result = format_grouped("abcdefghijklmnop", group_size=3, groups=4, separator=" | ")
        assert result == "abc | def | ghi | jkl"

    def test_format_grouped_regex_special_chars(self) -> None:
        """Test with regex special characters."""
        result = format_grouped(".*+?^${}()|[]\\", group_size=4, separator="-")
        assert result == ".*+?-^${}-()|[-]\\"


class TestFormatGroupedEdgeCases:
    """Test edge cases for format_grouped function."""

    def test_format_grouped_none_handling(self) -> None:
        """Test that function works with string inputs only."""
        # The function expects string input, type checking should catch None
        # This tests the actual behavior with string inputs
        result = format_grouped("None", group_size=2)
        assert result == "No ne"

    def test_format_grouped_very_small_groups(self) -> None:
        """Test with very small group size and many groups."""
        result = format_grouped("abcdefghij", group_size=1, groups=5, separator=",")
        assert result == "a,b,c,d,e"

    def test_format_grouped_negative_groups(self) -> None:
        """Test behavior with negative groups parameter."""
        # With negative groups, it should show all groups (treat as 0)
        result = format_grouped("123456", group_size=2, groups=-1)
        # Based on the code, if groups > 0 condition fails, all groups are shown
        assert result == "12 34 56"

    def test_format_grouped_large_group_size_edge(self) -> None:
        """Test with extremely large group size."""
        result = format_grouped("abc", group_size=1000)
        assert result == "abc"

    def test_format_grouped_zero_groups_explicit(self) -> None:
        """Test explicit zero groups parameter."""
        result = format_grouped("abcdef", group_size=2, groups=0)
        assert result == "ab cd ef"


class TestModuleIntegration:
    """Test module-level integration scenarios."""

    def test_all_functions_importable(self) -> None:
        """Test that all public functions are importable."""
        from provide.foundation.formatting.grouping import format_grouped

        assert callable(format_grouped)

    def test_module_exports(self) -> None:
        """Test that __all__ contains expected exports."""
        from provide.foundation.formatting import grouping

        assert hasattr(grouping, "__all__")
        assert "format_grouped" in grouping.__all__

    def test_function_docstring_examples(self) -> None:
        """Test examples from function docstring."""
        # Example 1: format_grouped("abc123def456", group_size=4, separator="-")
        result = format_grouped("abc123def456", group_size=4, separator="-")
        assert result == "abc1-23de-f456"

        # Example 2: format_grouped("abc123def456", group_size=4, groups=2)
        result = format_grouped("abc123def456", group_size=4, groups=2)
        assert result == "abc1 23de"

        # Example 3: format_grouped("1234567890abcdef", group_size=4)
        result = format_grouped("1234567890abcdef", group_size=4)
        assert result == "1234 5678 90ab cdef"


class TestPerformanceAndMemory:
    """Test performance-related edge cases."""

    def test_format_grouped_performance_long_string(self) -> None:
        """Test with reasonably long string for performance."""
        long_string = "x" * 1000
        result = format_grouped(long_string, group_size=50, groups=5)
        expected_groups = ["x" * 50] * 5
        assert result == " ".join(expected_groups)

    def test_format_grouped_memory_efficiency_large_groups(self) -> None:
        """Test memory efficiency with large group size."""
        text = "abcdefghijklmnopqrstuvwxyz"
        result = format_grouped(text, group_size=100)  # Larger than text
        assert result == text


class TestRealWorldUseCases:
    """Test real-world use cases for format_grouped."""

    def test_format_grouped_hash_values(self) -> None:
        """Test formatting hash values."""
        hash_value = "a1b2c3d4e5f6789012345678"
        result = format_grouped(hash_value, group_size=8, separator=" ")
        assert result == "a1b2c3d4 e5f67890 12345678"

    def test_format_grouped_credit_card_style(self) -> None:
        """Test credit card number style formatting."""
        number = "1234567890123456"
        result = format_grouped(number, group_size=4, separator=" ")
        assert result == "1234 5678 9012 3456"

    def test_format_grouped_uuid_style(self) -> None:
        """Test UUID-style formatting."""
        uuid_like = "1234567890abcdef1234567890abcdef"
        result = format_grouped(uuid_like, group_size=8, groups=4, separator="-")
        assert result == "12345678-90abcdef-12345678-90abcdef"

    def test_format_grouped_truncated_display(self) -> None:
        """Test truncated display for long IDs."""
        long_id = "verylongidentifierthatshouldbetruncat"
        result = format_grouped(long_id, group_size=4, groups=3, separator=" ")
        assert result == "very long iden"  # Shows first 3 groups only


# 🧱🏗️🔚
