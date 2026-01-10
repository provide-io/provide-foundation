#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for collection environment getter functions.

Tests get_list, get_dict, get_tuple, get_set and related edge cases."""

from __future__ import annotations

from collections.abc import Generator
import os
from typing import Any

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.utils.environment.getters import (
    get_dict,
    get_list,
    get_set,
    get_tuple,
)


@pytest.fixture
def clean_env() -> Generator[None, None, None]:
    """Fixture to clean up environment variables after each test."""
    original_env = os.environ.copy()
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


class TestGetList(FoundationTestCase):
    """Test get_list function edge cases."""

    def test_get_list_empty_items_filtered(self, clean_env: Any) -> None:
        """Test get_list filters empty items."""
        os.environ["TEST_LIST"] = "a,,b,,"
        result = get_list("TEST_LIST")
        assert result == ["a", "b"]

    def test_get_list_only_separators(self, clean_env: Any) -> None:
        """Test get_list with only separators."""
        os.environ["TEST_LIST"] = ",,,"
        result = get_list("TEST_LIST")
        assert result == []

    def test_get_list_custom_separator(self, clean_env: Any) -> None:
        """Test get_list with custom separator."""
        os.environ["TEST_LIST"] = "a|b|c"
        result = get_list("TEST_LIST", separator="|")
        assert result == ["a", "b", "c"]

    def test_get_list_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_list whitespace handling."""
        os.environ["TEST_LIST"] = " a , b , c "
        result = get_list("TEST_LIST")
        assert result == ["a", "b", "c"]

    def test_get_list_single_item(self, clean_env: Any) -> None:
        """Test get_list with single item."""
        os.environ["TEST_LIST"] = "single"
        result = get_list("TEST_LIST")
        assert result == ["single"]


class TestGetDict(FoundationTestCase):
    """Test get_dict function edge cases."""

    def test_get_dict_invalid_format_warning(self, clean_env: Any) -> None:
        """Test get_dict logs warning for invalid format and returns partial result."""
        os.environ["TEST_DICT"] = "key1=val1,invalid_item,key2=val2"

        with patch("provide.foundation.utils.environment.getters._get_logger") as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger

            result = get_dict("TEST_DICT")

            # Should return valid items and skip invalid ones
            assert result == {"key1": "val1", "key2": "val2"}

            # Should log warning about invalid format
            mock_logger.warning.assert_called_once()
            call_args = mock_logger.warning.call_args
            assert "Invalid dictionary format" in call_args[0][0]

    def test_get_dict_custom_separators(self, clean_env: Any) -> None:
        """Test get_dict with custom separators."""
        os.environ["TEST_DICT"] = "key1:val1;key2:val2"
        result = get_dict("TEST_DICT", item_separator=";", key_value_separator=":")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_empty_items_skipped(self, clean_env: Any) -> None:
        """Test get_dict skips empty items."""
        os.environ["TEST_DICT"] = "key1=val1,,key2=val2,"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_dict handles whitespace correctly."""
        os.environ["TEST_DICT"] = " key1 = val1 , key2 = val2 "
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_no_separator_items_skipped(self, clean_env: Any) -> None:
        """Test get_dict skips items without key-value separator."""
        os.environ["TEST_DICT"] = "key1=val1,invalid_item,key2=val2"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_multiple_separators(self, clean_env: Any) -> None:
        """Test get_dict with multiple separators in value."""
        os.environ["TEST_DICT"] = "key1=val=with=equals,key2=val2"
        result = get_dict("TEST_DICT")
        assert result == {"key1": "val=with=equals", "key2": "val2"}


class TestGetDictEdgeCases(FoundationTestCase):
    """Test additional get_dict edge cases for coverage."""

    def test_get_dict_items_without_separator_skipped(self, clean_env: Any) -> None:
        """Test get_dict skips items without key=value separator."""
        os.environ["TEST_DICT"] = "key1=val1,no_separator,key2=val2"
        result = get_dict("TEST_DICT")
        # Should skip 'no_separator' and only include key1 and key2
        assert result == {"key1": "val1", "key2": "val2"}

    def test_get_dict_mixed_invalid_items(self, clean_env: Any) -> None:
        """Test get_dict handles mix of valid and invalid items."""
        os.environ["TEST_DICT"] = "valid=1,no_eq,another=2,also_no_eq,final=3"
        result = get_dict("TEST_DICT")
        # Should only include items with '=' separator
        assert result == {"valid": "1", "another": "2", "final": "3"}


class TestGetTuple(FoundationTestCase):
    """Test get_tuple function edge cases."""

    def test_get_tuple_missing_with_default(self, clean_env: Any) -> None:
        """Test get_tuple returns default when env var missing."""
        result = get_tuple("MISSING", ("default", "tuple"))
        assert result == ("default", "tuple")

    def test_get_tuple_missing_no_default(self, clean_env: Any) -> None:
        """Test get_tuple returns empty tuple when no default."""
        result = get_tuple("MISSING")
        assert result == ()

    def test_get_tuple_empty_items_filtered(self, clean_env: Any) -> None:
        """Test get_tuple filters empty items."""
        os.environ["TEST"] = "a,,b,,"
        assert get_tuple("TEST") == ("a", "b")

    def test_get_tuple_custom_separator(self, clean_env: Any) -> None:
        """Test get_tuple with custom separator."""
        os.environ["TEST"] = "a|b|c"
        result = get_tuple("TEST", separator="|")
        assert result == ("a", "b", "c")

    def test_get_tuple_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_tuple whitespace handling."""
        os.environ["TEST"] = " a , b , c "
        result = get_tuple("TEST")
        assert result == ("a", "b", "c")

    def test_get_tuple_single_item(self, clean_env: Any) -> None:
        """Test get_tuple with single item."""
        os.environ["TEST"] = "single"
        result = get_tuple("TEST")
        assert result == ("single",)


class TestGetSet(FoundationTestCase):
    """Test get_set function edge cases."""

    def test_get_set_missing_with_default(self, clean_env: Any) -> None:
        """Test get_set returns default when env var missing."""
        result = get_set("MISSING", {"default", "set"})
        assert result == {"default", "set"}

    def test_get_set_missing_no_default(self, clean_env: Any) -> None:
        """Test get_set returns empty set when no default."""
        result = get_set("MISSING")
        assert result == set()

    def test_get_set_duplicates_removed(self, clean_env: Any) -> None:
        """Test get_set removes duplicates."""
        os.environ["TEST"] = "a,b,a,c,b"
        result = get_set("TEST")
        assert result == {"a", "b", "c"}

    def test_get_set_empty_items_filtered(self, clean_env: Any) -> None:
        """Test get_set filters empty items."""
        os.environ["TEST"] = "a,,b,,"
        result = get_set("TEST")
        assert result == {"a", "b"}

    def test_get_set_custom_separator(self, clean_env: Any) -> None:
        """Test get_set with custom separator."""
        os.environ["TEST"] = "a|b|c"
        result = get_set("TEST", separator="|")
        assert result == {"a", "b", "c"}

    def test_get_set_whitespace_handling(self, clean_env: Any) -> None:
        """Test get_set whitespace handling."""
        os.environ["TEST"] = " a , b , c "
        result = get_set("TEST")
        assert result == {"a", "b", "c"}


# 🧱🏗️🔚
