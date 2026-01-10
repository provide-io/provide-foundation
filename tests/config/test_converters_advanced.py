#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for advanced config converters."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.config.validators import (
    validate_log_level,
    validate_non_negative,
    validate_overflow_policy,
    validate_port,
    validate_positive,
    validate_sample_rate,
)
from provide.foundation.errors.config import ValidationError
from provide.foundation.parsers.collections import parse_comma_list
from provide.foundation.parsers.primitives import (
    parse_json_dict,
    parse_json_list,
    parse_sample_rate,
)
from provide.foundation.parsers.structured import parse_headers


class TestSampleRateParsing(FoundationTestCase):
    """Test sample rate parsing."""

    def test_parse_sample_rate_valid(self) -> None:
        """Test parsing valid sample rates."""
        assert parse_sample_rate("0.0") == 0.0
        assert parse_sample_rate("0.5") == 0.5
        assert parse_sample_rate("1.0") == 1.0

    def test_parse_sample_rate_invalid_range(self) -> None:
        """Test parsing sample rates outside 0-1 range."""
        with pytest.raises(ValueError, match=r"must be >= 0.0"):
            parse_sample_rate("-0.1")

        with pytest.raises(ValueError, match=r"must be <= 1.0"):
            parse_sample_rate("1.1")


class TestHeadersParsing(FoundationTestCase):
    """Test HTTP headers parsing."""

    def test_parse_headers_valid(self) -> None:
        """Test parsing valid header pairs."""
        result = parse_headers("Authorization=Bearer token,Content-Type=application/json")
        assert result == {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }

    def test_parse_headers_empty(self) -> None:
        """Test parsing empty string returns empty dict."""
        assert parse_headers("") == {}
        assert parse_headers("   ") == {}

    def test_parse_headers_invalid_format(self) -> None:
        """Test invalid formats are skipped."""
        result = parse_headers("Valid=value,InvalidNoEquals,Another=one")
        assert result == {
            "Valid": "value",
            "Another": "one",
        }

    def test_parse_headers_whitespace(self) -> None:
        """Test whitespace handling."""
        result = parse_headers(" Key1 = Value1 , Key2 = Value2 ")
        assert result == {
            "Key1": "Value1",
            "Key2": "Value2",
        }


class TestCommaListParsing(FoundationTestCase):
    """Test comma-separated list parsing."""

    def test_parse_comma_list_valid(self) -> None:
        """Test parsing comma-separated strings."""
        assert parse_comma_list("a,b,c") == ["a", "b", "c"]
        assert parse_comma_list(" a , b , c ") == ["a", "b", "c"]

    def test_parse_comma_list_empty(self) -> None:
        """Test parsing empty string returns empty list."""
        assert parse_comma_list("") == []
        assert parse_comma_list("   ") == []

    def test_parse_comma_list_single(self) -> None:
        """Test parsing single item."""
        assert parse_comma_list("single") == ["single"]


class TestJsonParsing(FoundationTestCase):
    """Test JSON parsing functions."""

    def test_parse_json_dict_valid(self) -> None:
        """Test parsing valid JSON objects."""
        result = parse_json_dict('{"key": "value", "number": 42}')
        assert result == {"key": "value", "number": 42}

    def test_parse_json_dict_empty(self) -> None:
        """Test parsing empty string returns empty dict."""
        assert parse_json_dict("") == {}
        assert parse_json_dict("   ") == {}

    def test_parse_json_dict_invalid(self) -> None:
        """Test parsing invalid JSON raises error."""
        with pytest.raises(ValueError, match="Invalid json_dict"):
            parse_json_dict("not json")

        with pytest.raises(ValueError, match="Invalid json_dict"):
            parse_json_dict('["list", "not", "dict"]')

    def test_parse_json_list_valid(self) -> None:
        """Test parsing valid JSON arrays."""
        result = parse_json_list('["a", "b", "c"]')
        assert result == ["a", "b", "c"]

    def test_parse_json_list_empty(self) -> None:
        """Test parsing empty string returns empty list."""
        assert parse_json_list("") == []
        assert parse_json_list("   ") == []

    def test_parse_json_list_invalid(self) -> None:
        """Test parsing invalid JSON raises error."""
        with pytest.raises(ValueError, match="Invalid json_list"):
            parse_json_list("not json")

        with pytest.raises(ValueError, match="Invalid json_list"):
            parse_json_list('{"key": "value"}')


class TestValidators(FoundationTestCase):
    """Test validator functions."""

    def test_validate_log_level(self) -> None:
        """Test log level validator."""
        # Valid levels should not raise
        validate_log_level(None, type("attr", (), {"name": "test"})(), "DEBUG")
        validate_log_level(None, type("attr", (), {"name": "test"})(), "INFO")

        # Invalid level should raise
        with pytest.raises(ValidationError, match="Invalid test"):
            validate_log_level(None, type("attr", (), {"name": "test"})(), "INVALID")

    def test_validate_sample_rate(self) -> None:
        """Test sample rate validator."""
        # Valid rates should not raise
        validate_sample_rate(None, type("attr", (), {"name": "test"})(), 0.0)
        validate_sample_rate(None, type("attr", (), {"name": "test"})(), 0.5)
        validate_sample_rate(None, type("attr", (), {"name": "test"})(), 1.0)

        # Invalid rates should raise
        with pytest.raises(ValidationError, match="must be between"):
            validate_sample_rate(None, type("attr", (), {"name": "test"})(), -0.1)

        with pytest.raises(ValidationError, match="must be between"):
            validate_sample_rate(None, type("attr", (), {"name": "test"})(), 1.1)

    def test_validate_port(self) -> None:
        """Test port number validator."""
        # Valid ports should not raise
        validate_port(None, type("attr", (), {"name": "test"})(), 1)
        validate_port(None, type("attr", (), {"name": "test"})(), 8080)
        validate_port(None, type("attr", (), {"name": "test"})(), 65535)

        # Invalid ports should raise
        with pytest.raises(ValidationError, match="must be between"):
            validate_port(None, type("attr", (), {"name": "test"})(), 0)

        with pytest.raises(ValidationError, match="must be between"):
            validate_port(None, type("attr", (), {"name": "test"})(), 65536)

    def test_validate_positive(self) -> None:
        """Test positive value validator."""
        # Valid values should not raise
        validate_positive(None, type("attr", (), {"name": "test"})(), 1)
        validate_positive(None, type("attr", (), {"name": "test"})(), 0.1)
        validate_positive(None, type("attr", (), {"name": "test"})(), 100)

        # Invalid values should raise
        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive(None, type("attr", (), {"name": "test"})(), 0)

        with pytest.raises(ValidationError, match="must be positive"):
            validate_positive(None, type("attr", (), {"name": "test"})(), -1)

    def test_validate_non_negative(self) -> None:
        """Test non-negative value validator."""
        # Valid values should not raise
        validate_non_negative(None, type("attr", (), {"name": "test"})(), 0)
        validate_non_negative(None, type("attr", (), {"name": "test"})(), 1)
        validate_non_negative(None, type("attr", (), {"name": "test"})(), 100)

        # Invalid values should raise
        with pytest.raises(ValidationError, match="must be non-negative"):
            validate_non_negative(None, type("attr", (), {"name": "test"})(), -1)

        with pytest.raises(ValidationError, match="must be non-negative"):
            validate_non_negative(None, type("attr", (), {"name": "test"})(), -0.1)

    def test_validate_overflow_policy(self) -> None:
        """Test overflow policy validator."""
        # Valid policies should not raise
        validate_overflow_policy(None, type("attr", (), {"name": "test"})(), "drop_oldest")
        validate_overflow_policy(None, type("attr", (), {"name": "test"})(), "drop_newest")
        validate_overflow_policy(None, type("attr", (), {"name": "test"})(), "block")

        # Invalid policies should raise
        with pytest.raises(ValidationError, match="Invalid test"):
            validate_overflow_policy(None, type("attr", (), {"name": "test"})(), "invalid")

        with pytest.raises(ValidationError, match="Invalid test"):
            validate_overflow_policy(None, type("attr", (), {"name": "test"})(), "")


# 🧱🏗️🔚
