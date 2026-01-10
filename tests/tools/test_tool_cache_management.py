#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolCache management operations (clear, list, size, prune)."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.tools.cache import ToolCache


class TestToolCacheManagement(FoundationTestCase):
    """Test ToolCache management operations."""

    @pytest.fixture
    def temp_cache_dir(self) -> Path:
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def cache(self, temp_cache_dir: Path) -> ToolCache:
        """Create ToolCache instance with temporary directory."""
        return ToolCache(cache_dir=temp_cache_dir)

    def test_clear(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test clearing all cache entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Add some entries
        cache.store("tool1", "1.0.0", tool_path)
        cache.store("tool2", "2.0.0", tool_path)

        assert len(cache.metadata) == 2

        cache.clear()

        assert len(cache.metadata) == 0
        assert cache.metadata == {}

    def test_list_cached_empty(self, cache: ToolCache) -> None:
        """Test list_cached with empty cache."""
        result = cache.list_cached()
        assert result == []

    def test_list_cached_with_entries(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test list_cached with cache entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path, ttl_days=7)
        cache.store("tool2", "2.0.0", tool_path, ttl_days=0)  # never expires

        results = cache.list_cached()
        assert len(results) == 2

        # Check that all entries have required fields
        for entry in results:
            assert "key" in entry
            assert "expired" in entry
            assert "days_until_expiry" in entry
            assert "path" in entry
            assert "tool" in entry
            assert "version" in entry

    def test_list_cached_expiry_calculation(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test list_cached expiry calculations."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Store entry that expires in 7 days
        cache.store("tool1", "1.0.0", tool_path, ttl_days=7)

        results = cache.list_cached()
        entry = results[0]

        assert not entry["expired"]
        assert 6 <= entry["days_until_expiry"] <= 7  # Should be close to 7

    def test_list_cached_never_expires(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test list_cached with never-expiring entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path, ttl_days=0)

        results = cache.list_cached()
        entry = results[0]

        assert not entry["expired"]
        assert entry["days_until_expiry"] == -1

    def test_list_cached_expired_entry(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test list_cached with expired entry."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path, ttl_days=1)

        # Manually set to expired
        key = "tool1:1.0.0"
        past_time = (datetime.now() - timedelta(days=2)).isoformat()
        cache.metadata[key]["cached_at"] = past_time

        results = cache.list_cached()
        entry = results[0]

        assert entry["expired"]
        assert entry["days_until_expiry"] == 0

    def test_list_cached_invalid_date(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test list_cached with invalid date in entry."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path)

        # Corrupt the date
        cache.metadata["tool1:1.0.0"]["cached_at"] = "invalid-date"

        results = cache.list_cached()
        entry = results[0]

        assert entry["days_until_expiry"] == 0

    def test_get_size_empty_cache(self, cache: ToolCache) -> None:
        """Test get_size with empty cache."""
        assert cache.get_size() == 0

    def test_get_size_with_files(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test get_size with cached files."""
        # Create test file
        tool_file = temp_cache_dir / "tool1"
        tool_file.write_text("test content")

        cache.store("tool1", "1.0.0", tool_file)

        size = cache.get_size()
        assert size > 0
        assert size == len("test content")

    def test_get_size_with_directories(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test get_size with cached directories."""
        # Create test directory with files
        tool_dir = temp_cache_dir / "tool1"
        tool_dir.mkdir()

        file1 = tool_dir / "file1.txt"
        file1.write_text("content1")

        file2 = tool_dir / "file2.txt"
        file2.write_text("content2")

        cache.store("tool1", "1.0.0", tool_dir)

        size = cache.get_size()
        expected_size = len("content1") + len("content2")
        assert size == expected_size

    def test_get_size_nonexistent_path(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test get_size with non-existent cached path."""
        fake_path = temp_cache_dir / "nonexistent"
        cache.store("tool1", "1.0.0", fake_path)

        # Should not crash and return 0 for missing files
        size = cache.get_size()
        assert size == 0

    def test_get_size_error_handling(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test get_size error handling."""
        tool_file = temp_cache_dir / "tool1"
        tool_file.write_text("test")

        cache.store("tool1", "1.0.0", tool_file)

        # Mock stat to raise an error
        with patch("pathlib.Path.stat", side_effect=OSError("Permission denied")):
            size = cache.get_size()
            assert size == 0  # Should handle error gracefully

    def test_prune_expired_no_expired(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test prune_expired with no expired entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path)

        removed = cache.prune_expired()
        assert removed == 0
        assert "tool1:1.0.0" in cache.metadata

    def test_prune_expired_with_expired(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test prune_expired with expired entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        # Store entries
        cache.store("tool1", "1.0.0", tool_path, ttl_days=1)
        cache.store("tool2", "2.0.0", tool_path, ttl_days=7)

        # Make first entry expired
        key = "tool1:1.0.0"
        past_time = (datetime.now() - timedelta(days=2)).isoformat()
        cache.metadata[key]["cached_at"] = past_time

        with patch("provide.foundation.tools.cache.log") as mock_log:
            removed = cache.prune_expired()
            assert removed == 1
            mock_log.info.assert_called_once()

        assert key not in cache.metadata
        assert "tool2:2.0.0" in cache.metadata

    def test_prune_expired_all_expired(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test prune_expired with all entries expired."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path, ttl_days=1)
        cache.store("tool2", "2.0.0", tool_path, ttl_days=1)

        # Make all entries expired
        past_time = (datetime.now() - timedelta(days=2)).isoformat()
        for key in cache.metadata:
            cache.metadata[key]["cached_at"] = past_time

        removed = cache.prune_expired()
        assert removed == 2
        assert len(cache.metadata) == 0

    def test_debug_logging(self, cache: ToolCache, temp_cache_dir: Path) -> None:
        """Test that debug logging works correctly."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        with patch("provide.foundation.tools.cache.log") as mock_log:
            # Cache miss
            cache.get("nonexistent", "1.0.0")
            mock_log.debug.assert_called_with(
                "Cache miss: nonexistent:1.0.0 not in cache",
            )

            # Cache store
            cache.store("tool1", "1.0.0", tool_path)
            mock_log.debug.assert_called_with(
                "Cached tool1:1.0.0 at " + str(tool_path) + " (TTL: 7 days)",
            )

            # Cache hit
            cache.get("tool1", "1.0.0")
            mock_log.debug.assert_called_with("Cache hit: tool1:1.0.0")

    def test_integration_full_workflow(
        self,
        cache: ToolCache,
        temp_cache_dir: Path,
    ) -> None:
        """Test full cache workflow integration."""
        # Create tool directory
        tool_dir = temp_cache_dir / "mytool" / "1.2.3"
        tool_dir.mkdir(parents=True)

        binary = tool_dir / "mytool"
        binary.write_text("#!/bin/bash\necho 'Hello from mytool'")
        binary.chmod(0o755)

        # Store in cache
        cache.store("mytool", "1.2.3", tool_dir, ttl_days=30)

        # Verify storage
        assert len(cache.metadata) == 1

        # Retrieve from cache
        cached_path = cache.get("mytool", "1.2.3")
        assert cached_path == tool_dir
        assert cached_path.exists()

        # List cached tools
        cached_list = cache.list_cached()
        assert len(cached_list) == 1
        assert cached_list[0]["tool"] == "mytool"
        assert cached_list[0]["version"] == "1.2.3"
        assert not cached_list[0]["expired"]

        # Get cache size
        size = cache.get_size()
        assert size > 0

        # Invalidate
        cache.invalidate("mytool", "1.2.3")
        assert len(cache.metadata) == 0

        # Verify cache miss after invalidation
        result = cache.get("mytool", "1.2.3")
        assert result is None


# 🧱🏗️🔚
