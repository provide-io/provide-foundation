#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import pytest

from provide.foundation.errors import ValidationError
from provide.foundation.serialization import ini


class TestIniDumps:
    """Test ini_dumps serialization."""

    def test_basic_section(self) -> None:
        """Should serialize basic INI section."""
        data = {"section": {"key": "value"}}
        result = ini.ini_dumps(data)
        assert "[section]" in result
        assert "key = value" in result

    def test_multiple_sections(self) -> None:
        """Should serialize multiple sections."""
        data = {
            "section1": {"key1": "value1"},
            "section2": {"key2": "value2"},
        }
        result = ini.ini_dumps(data)
        assert "[section1]" in result
        assert "[section2]" in result

    def test_multiple_keys(self) -> None:
        """Should serialize multiple keys in section."""
        data = {"section": {"key1": "val1", "key2": "val2"}}
        result = ini.ini_dumps(data)
        assert "key1 = val1" in result
        assert "key2 = val2" in result

    def test_numeric_values(self) -> None:
        """Should convert numeric values to strings."""
        data = {"section": {"port": 8080}}
        result = ini.ini_dumps(data)
        assert "port = 8080" in result

    def test_invalid_input_not_dict(self) -> None:
        """Should raise ValidationError for non-dict input."""
        with pytest.raises(ValidationError, match="INI serialization requires a dictionary"):
            ini.ini_dumps("not a dict")

    def test_invalid_section_not_dict(self) -> None:
        """Should raise ValidationError if section is not dict."""
        with pytest.raises(ValidationError, match="must be a dictionary"):
            ini.ini_dumps({"section": "not a dict"})


class TestIniLoads:
    """Test ini_loads deserialization."""

    def test_basic_parsing(self) -> None:
        """Should parse basic INI."""
        content = "[section]\nkey = value"
        result = ini.ini_loads(content)
        assert result == {"section": {"key": "value"}}

    def test_multiple_sections(self) -> None:
        """Should parse multiple sections."""
        content = "[section1]\nkey1 = value1\n\n[section2]\nkey2 = value2"
        result = ini.ini_loads(content)
        assert "section1" in result
        assert "section2" in result

    def test_comments(self) -> None:
        """Should handle comments."""
        content = "; Comment\n[section]\nkey = value  # inline"
        result = ini.ini_loads(content)
        assert result["section"]["key"] == "value  # inline"  # ConfigParser doesn't strip inline comments

    def test_empty_string(self) -> None:
        """Should handle empty string."""
        result = ini.ini_loads("")
        assert result == {}

    def test_caching_enabled(self, mock_env_small_cache) -> None:
        """Should use cache when enabled."""
        content = "[section]\nkey = value"
        result1 = ini.ini_loads(content, use_cache=True)
        result2 = ini.ini_loads(content, use_cache=True)
        assert result1 == result2

    def test_invalid_input_not_string(self) -> None:
        """Should raise ValidationError for non-string input."""
        with pytest.raises(ValidationError, match="Input must be a string"):
            ini.ini_loads(123)


class TestIniRoundTrip:
    """Test round-trip serialization."""

    def test_round_trip(self) -> None:
        """Should round-trip INI data."""
        original = {"section": {"key": "value"}}
        serialized = ini.ini_dumps(original)
        deserialized = ini.ini_loads(serialized)
        assert deserialized == original


class TestModuleExports:
    """Test module exports."""

    def test_all_exports(self) -> None:
        """Module should export expected symbols."""
        assert set(ini.__all__) == {"ini_dumps", "ini_loads"}


# 🧱🏗️🔚
