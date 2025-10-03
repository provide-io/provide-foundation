from __future__ import annotations

from pathlib import Path
import threading

#
# version.py
#
"""Version handling for provide-foundation.
Integrates VERSION logic from flavorpack with robust fallback mechanisms.

This module uses lazy initialization to avoid blocking I/O at import time,
making it safe to import in async contexts.
"""

# Thread-safe lazy initialization state
_version_lock = threading.Lock()
_cached_version: str | None = None


def reset_version_cache() -> None:
    """Reset the cached version (for testing).

    This function clears the cached version so that get_version() will
    re-evaluate the version on the next call.

    Warning:
        This should only be called from test code or test fixtures.
    """
    global _cached_version
    with _version_lock:
        _cached_version = None


def _find_project_root() -> Path | None:
    """Find the project root directory by looking for VERSION file."""
    current = Path(__file__).parent

    # Walk up the directory tree looking for VERSION file
    while current != current.parent:  # Stop at filesystem root
        version_file = current / "VERSION"
        if version_file.exists():
            return current
        current = current.parent

    return None


def get_version() -> str:
    """Get the current provide-foundation version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.

    This function is thread-safe and caches the result after first call.

    Returns:
        str: The current version string

    """
    global _cached_version

    # Fast path: return cached version if available
    if _cached_version is not None:
        return _cached_version

    # Slow path: load version with thread-safe locking
    with _version_lock:
        # Double-check after acquiring lock
        if _cached_version is not None:
            return _cached_version

        # Try VERSION file first (single source of truth)
        project_root = _find_project_root()
        if project_root:
            version_file = project_root / "VERSION"
            if version_file.exists():
                try:
                    _cached_version = version_file.read_text().strip()
                    return _cached_version
                except OSError:
                    # Fall back to metadata if VERSION file can't be read
                    pass

        # Fallback to package metadata
        try:
            from importlib.metadata import PackageNotFoundError, version

            _cached_version = version("provide-foundation")
            return _cached_version
        except PackageNotFoundError:
            pass

        # Final fallback
        _cached_version = "0.0.0-dev"
        return _cached_version


def __getattr__(name: str) -> str:
    """Lazy loading support for __version__.

    This allows __version__ to be loaded on first access rather than at
    import time, making this module safe to import in async contexts.
    """
    if name == "__version__":
        return get_version()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
