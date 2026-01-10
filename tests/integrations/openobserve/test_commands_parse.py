#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for OpenObserve CLI command parsing functionality.

Tests the _parse_filter_to_dict helper function for parsing filter strings."""

from __future__ import annotations

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


# 🧱🏗️🔚
