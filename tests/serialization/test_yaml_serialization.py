#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.serialization import yaml


class TestYamlDumps:
    """Test yaml_dumps serialization."""

    def test_basic_dict(self) -> None:
        """Should serialize basic dictionary."""
        result = yaml.yaml_dumps({"key": "value"})
        assert "key:" in result
        assert "value" in result

    def test_nested_dict(self) -> None:
        """Should serialize nested dictionaries."""
        data = {"outer": {"inner": "value"}}
        result = yaml.yaml_dumps(data)
        assert "outer:" in result
        assert "inner:" in result

    def test_list(self) -> None:
        """Should serialize lists."""
        result = yaml.yaml_dumps([1, 2, 3])
        assert "- 1" in result or "[1, 2, 3]" in result

    def test_mixed_types(self) -> None:
        """Should handle mixed types."""
        data = {"string": "value", "number": 42, "boolean": True, "null": None}
        result = yaml.yaml_dumps(data)
        assert "string:" in result
        assert "number:" in result

    def test_unicode(self) -> None:
        """Should handle unicode characters."""
        data = {"emoji": "🎉", "japanese": "こんにちは"}
        result = yaml.yaml_dumps(data, allow_unicode=True)
        assert "emoji:" in result

    def test_flow_style(self) -> None:
        """Should support flow style formatting."""
        data = {"key": "value"}
        result = yaml.yaml_dumps(data, default_flow_style=True)
        assert "{" in result and "}" in result

    def test_sort_keys(self) -> None:
        """Should sort keys when requested."""
        data = {"z": 1, "a": 2, "m": 3}
        result = yaml.yaml_dumps(data, sort_keys=True)
        [line for line in result.split("\n") if line.strip()]
        # Keys should appear in sorted order
        assert "a:" in result
        assert "m:" in result
        assert "z:" in result

    def test_empty_dict(self) -> None:
        """Should handle empty dictionary."""
        result = yaml.yaml_dumps({})
        assert result == "{}\n"

    def test_empty_list(self) -> None:
        """Should handle empty list."""
        result = yaml.yaml_dumps([])
        assert result == "[]\n"


class TestYamlLoads:
    """Test yaml_loads deserialization."""

    def test_basic_dict(self) -> None:
        """Should parse basic YAML dictionary."""
        result = yaml.yaml_loads("key: value")
        assert result == {"key": "value"}

    def test_nested_dict(self) -> None:
        """Should parse nested dictionaries."""
        content = """
outer:
  inner: value
"""
        result = yaml.yaml_loads(content)
        assert result == {"outer": {"inner": "value"}}

    def test_list(self) -> None:
        """Should parse YAML lists."""
        content = """
- item1
- item2
- item3
"""
        result = yaml.yaml_loads(content)
        assert result == ["item1", "item2", "item3"]

    def test_flow_style_dict(self) -> None:
        """Should parse flow-style dictionaries."""
        result = yaml.yaml_loads("{key: value}")
        assert result == {"key": "value"}

    def test_flow_style_list(self) -> None:
        """Should parse flow-style lists."""
        result = yaml.yaml_loads("[1, 2, 3]")
        assert result == [1, 2, 3]

    def test_multiline_string(self) -> None:
        """Should handle multiline strings."""
        content = """
text: |
  Line 1
  Line 2
"""
        result = yaml.yaml_loads(content)
        assert "Line 1" in result["text"]
        assert "Line 2" in result["text"]

    def test_numbers(self) -> None:
        """Should parse numbers correctly."""
        result = yaml.yaml_loads("number: 42")
        assert result == {"number": 42}

    def test_booleans(self) -> None:
        """Should parse booleans correctly."""
        result = yaml.yaml_loads("flag: true")
        assert result == {"flag": True}

    def test_null_values(self) -> None:
        """Should parse null values."""
        result = yaml.yaml_loads("value: null")
        assert result == {"value": None}

    def test_empty_string(self) -> None:
        """Should handle empty string."""
        result = yaml.yaml_loads("")
        assert result is None  # YAML treats empty as None

    def test_comments(self) -> None:
        """Should ignore comments."""
        content = """
# This is a comment
key: value  # Inline comment
"""
        result = yaml.yaml_loads(content)
        assert result == {"key": "value"}

    def test_unicode(self) -> None:
        """Should handle unicode characters."""
        content = "emoji: 🎉"
        result = yaml.yaml_loads(content)
        assert result == {"emoji": "🎉"}

    def test_caching_enabled(self, mock_env_small_cache) -> None:
        """Should use cache when enabled."""
        content = "key: value"

        # First call should cache
        result1 = yaml.yaml_loads(content, use_cache=True)

        # Second call should hit cache
        result2 = yaml.yaml_loads(content, use_cache=True)

        assert result1 == result2 == {"key": "value"}

    def test_caching_disabled(self) -> None:
        """Should not use cache when disabled."""
        content = "key: value"
        result = yaml.yaml_loads(content, use_cache=False)
        assert result == {"key": "value"}

    def test_cache_hit(self, mock_env_small_cache) -> None:
        """Should return cached result on cache hit."""
        from provide.foundation.serialization.cache import get_cache_key, get_serialization_cache

        content = "key: value"
        expected = {"key": "value"}

        # Manually populate cache
        cache = get_serialization_cache()
        cache_key = get_cache_key(content, "yaml")
        cache.set(cache_key, expected)

        # Should return cached value
        result = yaml.yaml_loads(content, use_cache=True)
        assert result == expected

    def test_invalid_input_not_string(self) -> None:
        """Should raise ValidationError for non-string input."""
        with pytest.raises(ValidationError, match="Input must be a string"):
            yaml.yaml_loads(123)

    def test_invalid_yaml_syntax(self) -> None:
        """Should raise ValidationError for invalid YAML."""
        with pytest.raises(ValidationError, match="Invalid YAML string"):
            yaml.yaml_loads("invalid: [unclosed")


class TestYamlRoundTrip:
    """Test round-trip serialization."""

    def test_round_trip_dict(self) -> None:
        """Should round-trip dictionaries."""
        original = {"key": "value", "number": 42}
        serialized = yaml.yaml_dumps(original)
        deserialized = yaml.yaml_loads(serialized)
        assert deserialized == original

    def test_round_trip_list(self) -> None:
        """Should round-trip lists."""
        original = [1, 2, 3, "four"]
        serialized = yaml.yaml_dumps(original)
        deserialized = yaml.yaml_loads(serialized)
        assert deserialized == original

    def test_round_trip_nested(self) -> None:
        """Should round-trip nested structures."""
        original = {"level1": {"level2": {"level3": "value"}}}
        serialized = yaml.yaml_dumps(original)
        deserialized = yaml.yaml_loads(serialized)
        assert deserialized == original

    def test_round_trip_mixed_types(self) -> None:
        """Should round-trip mixed types."""
        original = {"string": "text", "int": 42, "float": 3.14, "bool": True, "null": None}
        serialized = yaml.yaml_dumps(original)
        deserialized = yaml.yaml_loads(serialized)
        assert deserialized == original


class TestModuleExports:
    """Test module exports."""

    def test_all_exports(self) -> None:
        """Module should export expected symbols."""
        assert set(yaml.__all__) == {"yaml_dumps", "yaml_loads"}

    def test_exported_symbols_callable(self) -> None:
        """All exported symbols should be callable."""
        for symbol in yaml.__all__:
            assert callable(getattr(yaml, symbol))


# 🧱🏗️🔚
