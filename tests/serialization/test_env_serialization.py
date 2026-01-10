#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.serialization import env


class TestEnvDumps:
    """Test env_dumps serialization."""

    def test_basic_dict(self) -> None:
        """Should serialize basic dictionary."""
        result = env.env_dumps({"KEY": "value"})
        assert result == "KEY=value\n"

    def test_multiple_keys(self) -> None:
        """Should serialize multiple key-value pairs."""
        result = env.env_dumps({"KEY1": "value1", "KEY2": "value2"})
        assert "KEY1=" in result
        assert "KEY2=" in result

    def test_quote_values_true_with_spaces(self) -> None:
        """Should quote values with spaces when quote_values=True."""
        result = env.env_dumps({"KEY": "value with spaces"}, quote_values=True)
        assert result == 'KEY="value with spaces"\n'

    def test_quote_values_true_with_tabs(self) -> None:
        """Should quote values with tabs when quote_values=True."""
        result = env.env_dumps({"KEY": "value\twith\ttabs"}, quote_values=True)
        assert result == 'KEY="value\twith\ttabs"\n'

    def test_quote_values_false(self) -> None:
        """Should not quote values when quote_values=False."""
        result = env.env_dumps({"KEY": "value with spaces"}, quote_values=False)
        assert result == "KEY=value with spaces\n"

    def test_no_spaces_no_quotes(self) -> None:
        """Should not quote values without spaces even when quote_values=True."""
        result = env.env_dumps({"KEY": "valuenospaces"}, quote_values=True)
        assert result == "KEY=valuenospaces\n"

    def test_numeric_values(self) -> None:
        """Should convert numeric values to strings."""
        result = env.env_dumps({"PORT": 8080})
        assert "PORT=8080\n" in result

    def test_boolean_values(self) -> None:
        """Should convert boolean values to strings."""
        result = env.env_dumps({"DEBUG": True})
        assert "DEBUG=True\n" in result

    def test_empty_dict(self) -> None:
        """Should handle empty dictionary."""
        result = env.env_dumps({})
        assert result == "\n"

    def test_invalid_input_not_dict(self) -> None:
        """Should raise ValidationError for non-dict input."""
        with pytest.raises(ValidationError, match="ENV serialization requires a dictionary"):
            env.env_dumps("not a dict")

    def test_invalid_key_empty_string(self) -> None:
        """Should raise ValidationError for empty string key."""
        with pytest.raises(ValidationError, match="Invalid environment variable name"):
            env.env_dumps({"": "value"})

    def test_invalid_key_not_string(self) -> None:
        """Should raise ValidationError for non-string key."""
        with pytest.raises(ValidationError, match="Invalid environment variable name"):
            env.env_dumps({123: "value"})

    def test_exception_handling(self) -> None:
        """Should wrap unexpected exceptions in ValidationError."""
        # This tests the broad except clause
        with pytest.raises(ValidationError, match="Cannot serialize object to ENV format"):
            env.env_dumps({None: "value"})


class TestParseEnvLine:
    """Test _parse_env_line helper function."""

    def test_valid_line(self) -> None:
        """Should parse valid key=value line."""
        result = env._parse_env_line("KEY=value", 1)
        assert result == ("KEY", "value")

    def test_value_with_spaces(self) -> None:
        """Should parse value with spaces."""
        result = env._parse_env_line("KEY=value with spaces", 1)
        assert result == ("KEY", "value with spaces")

    def test_double_quoted_value(self) -> None:
        """Should remove double quotes from value."""
        result = env._parse_env_line('KEY="quoted value"', 1)
        assert result == ("KEY", "quoted value")

    def test_single_quoted_value(self) -> None:
        """Should remove single quotes from value."""
        result = env._parse_env_line("KEY='quoted value'", 1)
        assert result == ("KEY", "quoted value")

    def test_whitespace_around_equals(self) -> None:
        """Should strip whitespace around key and value."""
        result = env._parse_env_line("  KEY  =  value  ", 1)
        assert result == ("KEY", "value")

    def test_empty_line(self) -> None:
        """Should return None for empty line."""
        result = env._parse_env_line("", 1)
        assert result is None

    def test_whitespace_only_line(self) -> None:
        """Should return None for whitespace-only line."""
        result = env._parse_env_line("   ", 1)
        assert result is None

    def test_comment_line(self) -> None:
        """Should return None for comment line."""
        result = env._parse_env_line("# This is a comment", 1)
        assert result is None

    def test_missing_equals(self) -> None:
        """Should raise ValidationError for line without '='."""
        with pytest.raises(ValidationError, match="missing '='"):
            env._parse_env_line("INVALID_LINE", 1)

    def test_empty_key(self) -> None:
        """Should raise ValidationError for empty key."""
        with pytest.raises(ValidationError, match="empty key"):
            env._parse_env_line("=value", 1)

    def test_equals_in_value(self) -> None:
        """Should handle '=' in value."""
        result = env._parse_env_line("KEY=value=with=equals", 1)
        assert result == ("KEY", "value=with=equals")

    def test_empty_value(self) -> None:
        """Should handle empty value."""
        result = env._parse_env_line("KEY=", 1)
        assert result == ("KEY", "")


class TestEnvLoads:
    """Test env_loads deserialization."""

    def test_basic_parsing(self) -> None:
        """Should parse basic env content."""
        result = env.env_loads("KEY=value")
        assert result == {"KEY": "value"}

    def test_multiple_lines(self) -> None:
        """Should parse multiple lines."""
        content = "KEY1=value1\nKEY2=value2"
        result = env.env_loads(content)
        assert result == {"KEY1": "value1", "KEY2": "value2"}

    def test_quoted_values(self) -> None:
        """Should parse quoted values."""
        content = 'KEY="quoted value"'
        result = env.env_loads(content)
        assert result == {"KEY": "quoted value"}

    def test_comments(self) -> None:
        """Should skip comment lines."""
        content = "# Comment\nKEY=value\n# Another comment"
        result = env.env_loads(content)
        assert result == {"KEY": "value"}

    def test_empty_lines(self) -> None:
        """Should skip empty lines."""
        content = "KEY1=value1\n\nKEY2=value2\n"
        result = env.env_loads(content)
        assert result == {"KEY1": "value1", "KEY2": "value2"}

    def test_whitespace_lines(self) -> None:
        """Should skip whitespace-only lines."""
        content = "KEY1=value1\n   \nKEY2=value2"
        result = env.env_loads(content)
        assert result == {"KEY1": "value1", "KEY2": "value2"}

    def test_empty_string(self) -> None:
        """Should return empty dict for empty string."""
        result = env.env_loads("")
        assert result == {}

    def test_caching_enabled(self, mock_env_small_cache) -> None:
        """Should use cache when enabled."""
        content = "KEY=value"

        # First call should cache
        result1 = env.env_loads(content, use_cache=True)

        # Second call should hit cache
        result2 = env.env_loads(content, use_cache=True)

        assert result1 == result2 == {"KEY": "value"}

    def test_caching_disabled(self) -> None:
        """Should not use cache when disabled."""
        content = "KEY=value"
        result = env.env_loads(content, use_cache=False)
        assert result == {"KEY": "value"}

    def test_cache_hit(self, mock_env_small_cache) -> None:
        """Should return cached result on cache hit."""
        from provide.foundation.serialization.cache import get_cache_key, get_serialization_cache

        content = "KEY=value"
        expected = {"KEY": "value"}

        # Manually populate cache
        cache = get_serialization_cache()
        cache_key = get_cache_key(content, "env")
        cache.set(cache_key, expected)

        # Should return cached value
        result = env.env_loads(content, use_cache=True)
        assert result == expected

    def test_invalid_input_not_string(self) -> None:
        """Should raise ValidationError for non-string input."""
        with pytest.raises(ValidationError, match="Input must be a string"):
            env.env_loads(123)

    def test_invalid_format_missing_equals(self) -> None:
        """Should raise ValidationError for invalid format."""
        with pytest.raises(ValidationError, match="missing '='"):
            env.env_loads("INVALID_LINE")

    def test_invalid_format_empty_key(self) -> None:
        """Should raise ValidationError for empty key."""
        with pytest.raises(ValidationError, match="empty key"):
            env.env_loads("=value")

    def test_propagates_validation_error(self) -> None:
        """Should propagate ValidationError from parser."""
        with pytest.raises(ValidationError):
            env.env_loads("INVALID")

    def test_complex_values(self) -> None:
        """Should handle complex value strings."""
        content = "PATH=/usr/bin:/usr/local/bin"
        result = env.env_loads(content)
        assert result == {"PATH": "/usr/bin:/usr/local/bin"}


class TestEnvRoundTrip:
    """Test round-trip serialization."""

    def test_round_trip_basic(self) -> None:
        """Should round-trip basic data."""
        original = {"KEY": "value", "PORT": "8080"}
        serialized = env.env_dumps(original, quote_values=False)
        deserialized = env.env_loads(serialized)
        assert deserialized == original

    def test_round_trip_with_quotes(self) -> None:
        """Should round-trip data with quotes."""
        original = {"KEY": "value with spaces"}
        serialized = env.env_dumps(original, quote_values=True)
        deserialized = env.env_loads(serialized)
        assert deserialized == original

    def test_round_trip_empty(self) -> None:
        """Should round-trip empty dictionary."""
        original = {}
        serialized = env.env_dumps(original)
        deserialized = env.env_loads(serialized)
        assert deserialized == original


class TestModuleExports:
    """Test module exports."""

    def test_all_exports(self) -> None:
        """Module should export expected symbols."""
        assert set(env.__all__) == {"env_dumps", "env_loads"}

    def test_exported_symbols_callable(self) -> None:
        """All exported symbols should be callable."""
        for symbol in env.__all__:
            assert callable(getattr(env, symbol))


# 🧱🏗️🔚
