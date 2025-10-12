from __future__ import annotations

from provide.foundation.utils.versioning import (
    _find_project_root,
    get_version,
    reset_version_cache,
)

"""Version handling for provide-foundation.

This module uses the shared versioning utility with lazy initialization
to avoid blocking I/O at import time, making it safe to import in async contexts.
"""

__all__ = ["get_version", "reset_version_cache", "_find_project_root"]


def __getattr__(name: str) -> str:
    """Lazy loading support for __version__.

    This allows __version__ to be loaded on first access rather than at
    import time, making this module safe to import in async contexts.
    """
    if name == "__version__":
        return get_version("provide-foundation", caller_file=__file__)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
