#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolCache operations (get, store, invalidate, expiry)."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.tools.cache import ToolCache


class TestToolCacheOperations(FoundationTestCase):
    """Test ToolCache cache operations."""

    @pytest.fixture
    def temp_cache_dir(self) -> Path:
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def cache(self, temp_cache_dir: Path) -> ToolCache:
        """Create ToolCache instance with temporary directory."""
        return ToolCache(cache_dir=temp_cache_dir)

    def test_get_cache_miss_not_in_cache(self, cache: ToolCache) -> None:
        """Test get with cache miss - tool not in cache."""
        result = cache.get("nonexistent", "1.0.0")
        assert result is None

    def test_get_cache_miss_path_not_exists(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test get with cache miss - path doesn't exist."""
        # Store entry with non-existent path
        fake_path = temp_cache_dir / "nonexistent"
        cache.store("tool1", "1.0.0", fake_path)

        # Should return None and invalidate entry
        result = cache.get("tool1", "1.0.0")
        assert result is None
        assert "tool1:1.0.0" not in cache.metadata

    def test_get_cache_miss_expired(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test get with cache miss - entry expired."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Store with very short TTL
        cache.store("tool1", "1.0.0", tool_path, ttl_days=1)

        # Manually set cached_at to past
        key = "tool1:1.0.0"
        past_time = (datetime.now() - timedelta(days=2)).isoformat()
        cache.metadata[key]["cached_at"] = past_time

        # Should return None and invalidate entry
        result = cache.get("tool1", "1.0.0")
        assert result is None
        assert key not in cache.metadata

    def test_get_cache_hit(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test get with cache hit - valid entry."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path)

        result = cache.get("tool1", "1.0.0")
        assert result == tool_path

    def test_store_basic(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test basic store operation."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path)

        key = "tool1:1.0.0"
        assert key in cache.metadata

        entry = cache.metadata[key]
        assert entry["path"] == str(tool_path)
        assert entry["tool"] == "tool1"
        assert entry["version"] == "1.0.0"
        assert entry["ttl_days"] == 7  # default
        assert "cached_at" in entry

    def test_store_custom_ttl(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test store with custom TTL."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path, ttl_days=14)

        entry = cache.metadata["tool1:1.0.0"]
        assert entry["ttl_days"] == 14

    def test_store_overwrites_existing(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test that store overwrites existing entries."""
        tool_path1 = temp_cache_dir / "tool1_old"
        tool_path1.mkdir()
        tool_path2 = temp_cache_dir / "tool1_new"
        tool_path2.mkdir()

        # Store first version
        cache.store("tool1", "1.0.0", tool_path1, ttl_days=7)

        # Store second version (should overwrite)
        cache.store("tool1", "1.0.0", tool_path2, ttl_days=14)

        entry = cache.metadata["tool1:1.0.0"]
        assert entry["path"] == str(tool_path2)
        assert entry["ttl_days"] == 14

    def test_invalidate_specific_version(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test invalidating specific version."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Store two versions
        cache.store("tool1", "1.0.0", tool_path)
        cache.store("tool1", "2.0.0", tool_path)

        # Invalidate specific version
        cache.invalidate("tool1", "1.0.0")

        assert "tool1:1.0.0" not in cache.metadata
        assert "tool1:2.0.0" in cache.metadata

    def test_invalidate_all_versions(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test invalidating all versions of a tool."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Store multiple versions and different tool
        cache.store("tool1", "1.0.0", tool_path)
        cache.store("tool1", "2.0.0", tool_path)
        cache.store("tool2", "1.0.0", tool_path)

        # Invalidate all versions of tool1
        cache.invalidate("tool1")

        assert "tool1:1.0.0" not in cache.metadata
        assert "tool1:2.0.0" not in cache.metadata
        assert "tool2:1.0.0" in cache.metadata

    def test_invalidate_nonexistent_tool(self, cache: ToolCache) -> None:
        """Test invalidating non-existent tool."""
        # Should not raise error
        cache.invalidate("nonexistent", "1.0.0")
        cache.invalidate("nonexistent")

    def test_is_expired_not_expired(self, cache: ToolCache) -> None:
        """Test _is_expired with non-expired entry."""
        entry = {"cached_at": datetime.now().isoformat(), "ttl_days": 7}

        assert not cache._is_expired(entry)

    def test_is_expired_expired(self, cache: ToolCache) -> None:
        """Test _is_expired with expired entry."""
        past_time = datetime.now() - timedelta(days=10)
        entry = {"cached_at": past_time.isoformat(), "ttl_days": 7}

        assert cache._is_expired(entry)

    def test_is_expired_never_expires(self, cache: ToolCache) -> None:
        """Test _is_expired with TTL of 0 (never expires)."""
        past_time = datetime.now() - timedelta(days=100)
        entry = {"cached_at": past_time.isoformat(), "ttl_days": 0}

        assert not cache._is_expired(entry)

    def test_is_expired_negative_ttl(self, cache: ToolCache) -> None:
        """Test _is_expired with negative TTL (never expires)."""
        past_time = datetime.now() - timedelta(days=100)
        entry = {"cached_at": past_time.isoformat(), "ttl_days": -1}

        assert not cache._is_expired(entry)

    def test_is_expired_invalid_date(self, cache: ToolCache) -> None:
        """Test _is_expired with invalid date format."""
        entry = {"cached_at": "invalid-date-format", "ttl_days": 7}

        # Should return True (treat as expired)
        assert cache._is_expired(entry)

    def test_is_expired_missing_ttl(self, cache: ToolCache) -> None:
        """Test _is_expired with missing ttl_days (defaults to 7)."""
        past_time = datetime.now() - timedelta(days=10)
        entry = {"cached_at": past_time.isoformat()}

        assert cache._is_expired(entry)


# 🧱🏗️🔚
