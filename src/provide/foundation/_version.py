from __future__ import annotations

from pathlib import Path

from provide.foundation.utils.versioning import (
    _find_project_root as _find_project_root_impl,
    get_version as get_version_impl,
    reset_version_cache as reset_version_cache_impl,
)

"""Version handling for provide-foundation.

This module uses the shared versioning utility with lazy initialization
to avoid blocking I/O at import time, making it safe to import in async contexts.
"""

__all__ = ["_find_project_root", "get_version", "reset_version_cache"]


# Compatibility wrappers for provide-foundation's legacy API
def get_version() -> str:
    """Get the version for provide-foundation.

    This is a compatibility wrapper that calls the shared versioning utility
    with provide-foundation's package name.

    Returns:
        The current version string
    """
    return get_version_impl("provide-foundation", caller_file=__file__)


def _find_project_root() -> Path | None:
    """Find the project root directory by looking for VERSION file.

    This is a compatibility wrapper that starts from this module's location.

    Returns:
        Path to project root if found, None otherwise
    """
    return _find_project_root_impl(Path(__file__).parent)


def reset_version_cache() -> None:
    """Reset the cached version for testing.

    This is a compatibility wrapper for provide-foundation's version cache.
    """
    reset_version_cache_impl("provide-foundation")


def __getattr__(name: str) -> str:
    """Lazy loading support for __version__.

    This allows __version__ to be loaded on first access rather than at
    import time, making this module safe to import in async contexts.
    """
    if name == "__version__":
        return get_version()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
