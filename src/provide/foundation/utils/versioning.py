#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

from pathlib import Path
import threading

"""Shared version discovery logic for provide-io packages.

This module provides thread-safe version discovery with caching,
supporting VERSION files, package metadata, and development fallbacks.
"""

# Thread-safe lazy initialization state
_version_lock = threading.Lock()
_cached_versions: dict[str, str] = {}


def reset_version_cache(package_name: str | None = None) -> None:
    """Reset the cached version for testing.

    Args:
        package_name: Specific package to reset, or None to reset all

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_versions
    with _version_lock:
        if package_name is None:
            _cached_versions.clear()
        else:
            _cached_versions.pop(package_name, None)


def _is_environment_root(path: Path) -> bool:
    """Whether `path` is the root of an installed environment rather than a project.

    An installed package lives under site-packages, which lives inside an
    environment, which very often lives inside some *other* project's checkout --
    `.venv/` at the top of the repo that created it. Every dependency installed
    there sits a few levels below that repo's own VERSION file.
    """
    return path.name in ("site-packages", "dist-packages") or (path / "pyvenv.cfg").is_file()


def _find_project_root(start_path: Path) -> Path | None:
    """Find the project root directory by looking for VERSION file.

    The search stops at an environment root. A VERSION file above that point
    belongs to whichever project happens to host the environment, and reporting
    it would give every installed package that project's version.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to project root if found, None otherwise
    """
    current = start_path

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        if _is_environment_root(current):
            return None
        current = current.parent

    return None


def get_version(package_name: str, caller_file: str | Path | None = None) -> str:
    """Get the version for a package.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches results after the first call per package.

    Args:
        package_name: The package name as it appears in PyPI (e.g., "provide-foundation")
        caller_file: Path to the calling module's __file__, used to find VERSION file.
                    If None, uses the calling context.

    Returns:
        The current version string
    """
    global _cached_versions

    # Fast path: return cached version if available
    if package_name in _cached_versions:
        return _cached_versions[package_name]

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if package_name in _cached_versions:
            return _cached_versions[package_name]

        # Determine start path for searching
        if caller_file is not None:
            start_path = Path(caller_file).parent
        else:
            # Try to infer from the call stack
            import inspect

            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                start_path = Path(caller_frame.f_code.co_filename).parent
            else:
                start_path = Path.cwd()

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root(start_path)
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    version_str = version_file.read_text().strip()
                    _cached_versions[package_name] = version_str
                    return version_str
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version as get_metadata_version

            version_str = get_metadata_version(package_name)
            _cached_versions[package_name] = version_str
            return version_str
        except PackageNotFoundError:
            pass

        # Final fallback
        version_str = "0.0.0-dev"
        _cached_versions[package_name] = version_str
        return version_str


__all__ = [
    "_find_project_root",
    "_is_environment_root",
    "get_version",
    "reset_version_cache",
]

# 🧱🏗️🔚
