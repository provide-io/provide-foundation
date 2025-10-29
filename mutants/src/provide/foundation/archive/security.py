# provide/foundation/archive/security.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Archive extraction security utilities.

Provides path validation to prevent common archive extraction vulnerabilities.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["is_safe_path"]
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_is_safe_path__mutmut_orig(base_dir: Path, target_path: str) -> bool:
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


def x_is_safe_path__mutmut_1(base_dir: Path, target_path: str) -> bool:
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
    if Path(None).is_absolute():
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


def x_is_safe_path__mutmut_2(base_dir: Path, target_path: str) -> bool:
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
        return True

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


def x_is_safe_path__mutmut_3(base_dir: Path, target_path: str) -> bool:
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
    if "XX..XX" in Path(target_path).parts:
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


def x_is_safe_path__mutmut_4(base_dir: Path, target_path: str) -> bool:
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
    if ".." not in Path(target_path).parts:
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


def x_is_safe_path__mutmut_5(base_dir: Path, target_path: str) -> bool:
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
    if ".." in Path(None).parts:
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


def x_is_safe_path__mutmut_6(base_dir: Path, target_path: str) -> bool:
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
        return True

    # Normalize and resolve the full path
    try:
        full_path = (base_dir / target_path).resolve()
        base_resolved = base_dir.resolve()

        # Use modern is_relative_to() for robust containment check
        # This catches symlinks and other tricks without string manipulation
        return full_path.is_relative_to(base_resolved)
    except (ValueError, OSError):
        return False


def x_is_safe_path__mutmut_7(base_dir: Path, target_path: str) -> bool:
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
        full_path = None
        base_resolved = base_dir.resolve()

        # Use modern is_relative_to() for robust containment check
        # This catches symlinks and other tricks without string manipulation
        return full_path.is_relative_to(base_resolved)
    except (ValueError, OSError):
        return False


def x_is_safe_path__mutmut_8(base_dir: Path, target_path: str) -> bool:
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
        full_path = (base_dir * target_path).resolve()
        base_resolved = base_dir.resolve()

        # Use modern is_relative_to() for robust containment check
        # This catches symlinks and other tricks without string manipulation
        return full_path.is_relative_to(base_resolved)
    except (ValueError, OSError):
        return False


def x_is_safe_path__mutmut_9(base_dir: Path, target_path: str) -> bool:
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
        base_resolved = None

        # Use modern is_relative_to() for robust containment check
        # This catches symlinks and other tricks without string manipulation
        return full_path.is_relative_to(base_resolved)
    except (ValueError, OSError):
        return False


def x_is_safe_path__mutmut_10(base_dir: Path, target_path: str) -> bool:
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
        return full_path.is_relative_to(None)
    except (ValueError, OSError):
        return False


def x_is_safe_path__mutmut_11(base_dir: Path, target_path: str) -> bool:
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
        return True


x_is_safe_path__mutmut_mutants: ClassVar[MutantDict] = {
    "x_is_safe_path__mutmut_1": x_is_safe_path__mutmut_1,
    "x_is_safe_path__mutmut_2": x_is_safe_path__mutmut_2,
    "x_is_safe_path__mutmut_3": x_is_safe_path__mutmut_3,
    "x_is_safe_path__mutmut_4": x_is_safe_path__mutmut_4,
    "x_is_safe_path__mutmut_5": x_is_safe_path__mutmut_5,
    "x_is_safe_path__mutmut_6": x_is_safe_path__mutmut_6,
    "x_is_safe_path__mutmut_7": x_is_safe_path__mutmut_7,
    "x_is_safe_path__mutmut_8": x_is_safe_path__mutmut_8,
    "x_is_safe_path__mutmut_9": x_is_safe_path__mutmut_9,
    "x_is_safe_path__mutmut_10": x_is_safe_path__mutmut_10,
    "x_is_safe_path__mutmut_11": x_is_safe_path__mutmut_11,
}


def is_safe_path(*args, **kwargs):
    result = _mutmut_trampoline(x_is_safe_path__mutmut_orig, x_is_safe_path__mutmut_mutants, args, kwargs)
    return result


is_safe_path.__signature__ = _mutmut_signature(x_is_safe_path__mutmut_orig)
x_is_safe_path__mutmut_orig.__name__ = "x_is_safe_path"


# <3 🧱🤝📦🪄
