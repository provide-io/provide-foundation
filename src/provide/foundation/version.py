#
# version.py
#
"""
Version handling for provide-foundation.
Integrates VERSION logic from flavorpack with robust fallback mechanisms.
"""

from pathlib import Path


def get_version() -> str:
    """Get the current provide-foundation version.

    Reads from VERSION file if it exists, otherwise falls back to package metadata,
    then to default development version.
    
    Returns:
        str: The current version string
    """
    # Try VERSION file first (single source of truth)
    version_file = Path(__file__).parent.parent.parent.parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    
    # Fallback to package metadata
    try:
        from importlib.metadata import PackageNotFoundError, version
        return version("provide-foundation")
    except PackageNotFoundError:
        pass
    
    # Final fallback
    return "0.0.0-dev"


__version__ = get_version()