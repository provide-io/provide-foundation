"""Tests for tool caching system.

Tests the TTL-based caching system for installed tools,
including cache operations, TTL handling, and metadata management.
"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.errors import FoundationError
from provide.foundation.tools.cache import CacheError


class TestCacheError(FoundationTestCase):
    """Test CacheError exception class."""

    def test_inherits_from_foundation_error(self) -> None:
        """Test that CacheError inherits from FoundationError."""
        error = CacheError("test error")
        assert isinstance(error, FoundationError)
        assert str(error) == "test error"

    def test_can_be_raised_and_caught(self) -> None:
        """Test that CacheError can be raised and caught."""
        with pytest.raises(CacheError):
            raise CacheError("cache operation failed")
