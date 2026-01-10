#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for ToolCache initialization and metadata operations."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.tools.cache import ToolCache


class TestToolCacheInit(FoundationTestCase):
    """Test ToolCache initialization and metadata operations."""

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
        with patch("pathlib.Path.home") as mock_home, patch("pathlib.Path.mkdir") as mock_mkdir:
            mock_home.return_value = Path("/mock/home")

            cache = ToolCache()
            expected_dir = Path("/mock/home") / ".provide-foundation" / "cache"
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


# 🧱🏗️🔚
