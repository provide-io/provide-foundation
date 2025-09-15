"""Tests for tool caching system.

Tests the TTL-based caching system for installed tools,
including cache operations, TTL handling, and metadata management.
"""

from datetime import datetime, timedelta
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import pytest

from provide.foundation.errors import FoundationError
from provide.foundation.tools.cache import CacheError, ToolCache


class TestCacheError:
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


class TestToolCache:
    """Test ToolCache class."""

    @pytest.fixture
    def temp_cache_dir(self) -> Path:
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def cache(self, temp_cache_dir: Path) -> ToolCache:
        """Create ToolCache instance with temporary directory."""
        return ToolCache(cache_dir=temp_cache_dir)

    def test_init_default_cache_dir(self) -> None:
        """Test initialization with default cache directory."""
        with patch("pathlib.Path.home") as mock_home, \
             patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_home.return_value = Path("/mock/home")

            cache = ToolCache()
            expected_dir = Path("/mock/home") / ".wrknv" / "cache"
            assert cache.cache_dir == expected_dir
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_init_custom_cache_dir(self, temp_cache_dir: Path) -> None:
        """Test initialization with custom cache directory."""
        cache = ToolCache(cache_dir=temp_cache_dir)
        assert cache.cache_dir == temp_cache_dir

    def test_init_creates_cache_dir(self, temp_cache_dir: Path) -> None:
        """Test that initialization creates cache directory."""
        cache_dir = temp_cache_dir / "new_cache"
        assert not cache_dir.exists()

        ToolCache(cache_dir=cache_dir)
        assert cache_dir.exists()
        assert cache_dir.is_dir()

    def test_metadata_file_location(self, cache: ToolCache) -> None:
        """Test metadata file location."""
        expected_path = cache.cache_dir / "metadata.json"
        assert cache.metadata_file == expected_path

    def test_load_metadata_empty_file(self, cache: ToolCache) -> None:
        """Test loading metadata from empty/non-existent file."""
        assert cache.metadata == {}

    def test_load_metadata_valid_json(self, cache: ToolCache) -> None:
        """Test loading metadata from valid JSON file."""
        test_data = {
            "tool1:1.0.0": {
                "path": "/path/to/tool1",
                "tool": "tool1",
                "version": "1.0.0",
            },
        }

        with cache.metadata_file.open("w") as f:
            json.dump(test_data, f)

        # Reload cache to test metadata loading
        new_cache = ToolCache(cache_dir=cache.cache_dir)
        assert new_cache.metadata == test_data

    def test_load_metadata_invalid_json(self, cache: ToolCache) -> None:
        """Test loading metadata from invalid JSON file."""
        with cache.metadata_file.open("w") as f:
            f.write("invalid json content {")

        # read_json handles invalid JSON by returning the default value silently
        new_cache = ToolCache(cache_dir=cache.cache_dir)
        assert new_cache.metadata == {}

    def test_save_metadata(self, cache: ToolCache) -> None:
        """Test saving metadata to disk."""
        test_data = {
            "tool1:1.0.0": {
                "path": "/path/to/tool1",
                "tool": "tool1",
                "version": "1.0.0",
            },
        }

        cache.metadata = test_data
        cache._save_metadata()

        # Verify file was written
        assert cache.metadata_file.exists()

        # Verify content
        with cache.metadata_file.open() as f:
            saved_data = json.load(f)
        assert saved_data == test_data

    def test_save_metadata_error_handling(self, cache: ToolCache) -> None:
        """Test save metadata error handling."""
        # Make the directory read-only to trigger write error
        cache.cache_dir.chmod(0o444)

        with patch("provide.foundation.tools.cache.log") as mock_log:
            with pytest.raises(Exception):  # write_json will raise after logging
                cache._save_metadata()
            mock_log.error.assert_called_once()

        # Restore permissions
        cache.cache_dir.chmod(0o755)

    def test_get_cache_miss_not_in_cache(self, cache: ToolCache) -> None:
        """Test get with cache miss - tool not in cache."""
        result = cache.get("nonexistent", "1.0.0")
        assert result is None

    def test_get_cache_miss_path_not_exists(
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
    ) -> None:
        """Test get_size with non-existent cached path."""
        fake_path = temp_cache_dir / "nonexistent"
        cache.store("tool1", "1.0.0", fake_path)

        # Should not crash and return 0 for missing files
        size = cache.get_size()
        assert size == 0

    def test_get_size_error_handling(
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
    ) -> None:
        """Test prune_expired with no expired entries."""
        tool_path = temp_cache_dir / "tool1"
        tool_path.mkdir()

        cache.store("tool1", "1.0.0", tool_path)

        removed = cache.prune_expired()
        assert removed == 0
        assert "tool1:1.0.0" in cache.metadata

    def test_prune_expired_with_expired(
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
        self, cache: ToolCache, temp_cache_dir: Path,
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
