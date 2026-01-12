#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.serialization import toml


class TestTomlDumps:
    """Test toml_dumps serialization."""

    def test_basic_dict(self) -> None:
        """Should serialize basic dictionary."""
        result = toml.toml_dumps({"key": "value"})
        assert 'key = "value"' in result

    def test_nested_dict(self) -> None:
        """Should serialize nested dictionaries as TOML tables."""
        data = {"section": {"key": "value"}}
        result = toml.toml_dumps(data)
        assert "[section]" in result

    def test_mixed_types(self) -> None:
        """Should handle mixed types."""
        data = {"string": "value", "number": 42, "boolean": True}
        result = toml.toml_dumps(data)
        assert "string" in result
        assert "42" in result

    def test_lists(self) -> None:
        """Should serialize lists."""
        data = {"items": [1, 2, 3]}
        result = toml.toml_dumps(data)
        assert "items" in result

    def test_dates(self) -> None:
        """Should handle datetime objects."""
        from datetime import datetime

        data = {"timestamp": datetime(2024, 1, 1, 12, 0, 0)}
        result = toml.toml_dumps(data)
        assert "timestamp" in result

    def test_empty_dict(self) -> None:
        """Should handle empty dictionary."""
        result = toml.toml_dumps({})
        assert result == ""

    def test_invalid_input_not_dict(self) -> None:
        """Should raise ValidationError for non-dict input."""
        with pytest.raises(ValidationError, match="TOML serialization requires a dictionary"):
            toml.toml_dumps("not a dict")

    def test_invalid_input_list(self) -> None:
        """Should raise ValidationError for list input."""
        with pytest.raises(ValidationError, match="TOML serialization requires a dictionary"):
            toml.toml_dumps([1, 2, 3])


class TestTomlLoads:
    """Test toml_loads deserialization."""

    def test_basic_dict(self) -> None:
        """Should parse basic TOML."""
        result = toml.toml_loads('key = "value"')
        assert result == {"key": "value"}

    def test_nested_dict(self) -> None:
        """Should parse TOML tables."""
        content = """
[section]
key = "value"
"""
        result = toml.toml_loads(content)
        assert result == {"section": {"key": "value"}}

    def test_numbers(self) -> None:
        """Should parse numbers correctly."""
        result = toml.toml_loads("number = 42")
        assert result == {"number": 42}

    def test_floats(self) -> None:
        """Should parse floats correctly."""
        result = toml.toml_loads("pi = 3.14")
        assert result == {"pi": 3.14}

    def test_booleans(self) -> None:
        """Should parse booleans correctly."""
        result = toml.toml_loads("flag = true")
        assert result == {"flag": True}

    def test_lists(self) -> None:
        """Should parse arrays."""
        result = toml.toml_loads("items = [1, 2, 3]")
        assert result == {"items": [1, 2, 3]}

    def test_comments(self) -> None:
        """Should ignore comments."""
        content = """
# This is a comment
key = "value"  # Inline comment
"""
        result = toml.toml_loads(content)
        assert result == {"key": "value"}

    def test_empty_string(self) -> None:
        """Should handle empty string."""
        result = toml.toml_loads("")
        assert result == {}

    def test_caching_enabled(self, mock_env_small_cache) -> None:
        """Should use cache when enabled."""
        content = 'key = "value"'

        # First call should cache
        result1 = toml.toml_loads(content, use_cache=True)

        # Second call should hit cache
        result2 = toml.toml_loads(content, use_cache=True)

        assert result1 == result2 == {"key": "value"}

    def test_caching_disabled(self) -> None:
        """Should not use cache when disabled."""
        content = 'key = "value"'
        result = toml.toml_loads(content, use_cache=False)
        assert result == {"key": "value"}

    def test_cache_hit(self, mock_env_small_cache) -> None:
        """Should return cached result on cache hit."""
        from provide.foundation.serialization.cache import get_cache_key, get_serialization_cache

        content = 'key = "value"'
        expected = {"key": "value"}

        # Manually populate cache
        cache = get_serialization_cache()
        cache_key = get_cache_key(content, "toml")
        cache.set(cache_key, expected)

        # Should return cached value
        result = toml.toml_loads(content, use_cache=True)
        assert result == expected

    def test_invalid_input_not_string(self) -> None:
        """Should raise ValidationError for non-string input."""
        with pytest.raises(ValidationError, match="Input must be a string"):
            toml.toml_loads(123)

    def test_invalid_toml_syntax(self) -> None:
        """Should raise ValidationError for invalid TOML."""
        with pytest.raises(ValidationError, match="Invalid TOML string"):
            toml.toml_loads("invalid toml [[[")


class TestTomlRoundTrip:
    """Test round-trip serialization."""

    def test_round_trip_dict(self) -> None:
        """Should round-trip dictionaries."""
        original = {"key": "value", "number": 42}
        serialized = toml.toml_dumps(original)
        deserialized = toml.toml_loads(serialized)
        assert deserialized == original

    def test_round_trip_nested(self) -> None:
        """Should round-trip nested structures."""
        original = {"section": {"key": "value", "number": 42}}
        serialized = toml.toml_dumps(original)
        deserialized = toml.toml_loads(serialized)
        assert deserialized == original

    def test_round_trip_mixed_types(self) -> None:
        """Should round-trip mixed types."""
        original = {"string": "text", "int": 42, "float": 3.14, "bool": True}
        serialized = toml.toml_dumps(original)
        deserialized = toml.toml_loads(serialized)
        assert deserialized == original


class TestModuleExports:
    """Test module exports."""

    def test_all_exports(self) -> None:
        """Module should export expected symbols."""
        assert set(toml.__all__) == {"toml_dumps", "toml_loads"}

    def test_exported_symbols_callable(self) -> None:
        """All exported symbols should be callable."""
        for symbol in toml.__all__:
            assert callable(getattr(toml, symbol))


# 🧱🏗️🔚
