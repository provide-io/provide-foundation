#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the shared versioning utility."""

from __future__ import annotations

from pathlib import Path

import pytest

from provide.foundation.utils.versioning import (
    _find_project_root,
    get_version,
    reset_version_cache,
)


def test_get_version_reads_version_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_version reads from VERSION file when available."""
    # Reset cache before test
    reset_version_cache("test-package")

    # Create a VERSION file
    version_file = tmp_path / "VERSION"
    version_file.write_text("1.2.3\n", encoding="utf-8")

    # Mock _find_project_root to return our tmp_path
    monkeypatch.setattr(
        "provide.foundation.utils.versioning._find_project_root",
        lambda start_path: tmp_path,
    )

    result = get_version("test-package", caller_file=__file__)

    assert result == "1.2.3"


def test_get_version_uses_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_version falls back to package metadata when VERSION file not found."""
    # Reset cache before test
    reset_version_cache("test-package")

    # Mock _find_project_root to return None (no VERSION file)
    monkeypatch.setattr(
        "provide.foundation.utils.versioning._find_project_root",
        lambda start_path: None,
    )

    # Mock importlib.metadata.version to return a specific version
    monkeypatch.setattr("importlib.metadata.version", lambda _: "9.9.9", raising=False)

    result = get_version("test-package", caller_file=__file__)

    assert result == "9.9.9"


def test_get_version_defaults_when_metadata_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_version returns default when both VERSION file and metadata are unavailable."""
    # Reset cache before test
    reset_version_cache("test-package")

    # Mock _find_project_root to return None (no VERSION file)
    monkeypatch.setattr(
        "provide.foundation.utils.versioning._find_project_root",
        lambda start_path: None,
    )

    # Mock importlib.metadata.version to raise PackageNotFoundError
    from importlib import metadata as importlib_metadata

    def raise_package_not_found(_: str) -> str:
        raise importlib_metadata.PackageNotFoundError("missing")

    monkeypatch.setattr("importlib.metadata.version", raise_package_not_found, raising=False)

    result = get_version("test-package", caller_file=__file__)

    assert result == "0.0.0-dev"


def test_find_project_root_finds_version_file(tmp_path: Path) -> None:
    """Test that _find_project_root locates the VERSION file in parent directories."""
    # Create a nested directory structure with VERSION at the root
    root = tmp_path / "project"
    root.mkdir()
    (root / "VERSION").write_text("1.0.0")

    nested = root / "src" / "package"
    nested.mkdir(parents=True)

    # Should find the root with VERSION file
    result = _find_project_root(nested)

    assert result == root


def test_find_project_root_returns_none_when_not_found(tmp_path: Path) -> None:
    """Test that _find_project_root returns None when no VERSION file is found."""
    # Create a directory without VERSION file
    test_dir = tmp_path / "no-version"
    test_dir.mkdir()

    result = _find_project_root(test_dir)

    assert result is None


def test_version_caching() -> None:
    """Test that versions are cached after first call."""
    # Reset cache
    reset_version_cache("provide-foundation")

    # First call - will be cached
    version1 = get_version("provide-foundation", caller_file=__file__)

    # Second call - should return cached value
    version2 = get_version("provide-foundation", caller_file=__file__)

    assert version1 == version2


def test_reset_version_cache_specific_package() -> None:
    """Test that reset_version_cache can reset a specific package."""
    # Get version to cache it
    version1 = get_version("provide-foundation", caller_file=__file__)

    # Reset this specific package
    reset_version_cache("provide-foundation")

    # Next call should re-discover
    version2 = get_version("provide-foundation", caller_file=__file__)

    # Should still be the same value, but was re-discovered
    assert version1 == version2


def test_reset_version_cache_all_packages(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that reset_version_cache with None resets all packages."""
    # Mock _find_project_root to return None (no VERSION file)
    monkeypatch.setattr(
        "provide.foundation.utils.versioning._find_project_root",
        lambda start_path: None,
    )

    # Mock metadata to raise PackageNotFoundError
    from importlib import metadata as importlib_metadata

    def raise_package_not_found(_: str) -> str:
        raise importlib_metadata.PackageNotFoundError("missing")

    monkeypatch.setattr("importlib.metadata.version", raise_package_not_found, raising=False)

    # Get versions to cache them
    get_version("package1", caller_file=__file__)
    get_version("package2", caller_file=__file__)

    # Reset all
    reset_version_cache(None)

    # Both should be re-discovered on next call (won't raise, just re-execute)
    version1 = get_version("package1", caller_file=__file__)
    version2 = get_version("package2", caller_file=__file__)

    assert version1 == "0.0.0-dev"  # Default since packages don't exist
    assert version2 == "0.0.0-dev"


# 🧱🏗️🔚
