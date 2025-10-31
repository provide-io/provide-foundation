#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Archive extraction security utilities.

Provides path validation to prevent common archive extraction vulnerabilities."""

from __future__ import annotations

from pathlib import Path

__all__ = ["is_safe_path"]


def is_safe_path(base_dir: Path, target_path: str) -> bool:
    """Validate that a path is safe for extraction.

    Prevents:
    - Path traversal attacks (..)
    - Absolute paths
    - Symlinks that point outside base directory

    Uses modern Path.is_relative_to() for robust path containment checks,
    avoiding string manipulation vulnerabilities.

    Args:
        base_dir: Base extraction directory
        target_path: Path to validate

    Returns:
        True if path is safe, False otherwise

    Examples:
        >>> base = Path("/tmp/extract")
        >>> is_safe_path(base, "file.txt")  # Safe
        True
        >>> is_safe_path(base, "../etc/passwd")  # Path traversal
        False
        >>> is_safe_path(base, "/etc/passwd")  # Absolute path
        False
    """
    # Check for absolute paths
    if Path(target_path).is_absolute():
        return False

    # Check for path traversal patterns
    if ".." in Path(target_path).parts:
        return False

    # Normalize and resolve the full path
    try:
        full_path = (base_dir / target_path).resolve()
        base_resolved = base_dir.resolve()

        # Use modern is_relative_to() for robust containment check
        # This catches symlinks and other tricks without string manipulation
        return full_path.is_relative_to(base_resolved)
    except (ValueError, OSError):
        return False


# 🧱🏗️🔚
