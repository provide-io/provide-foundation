# provide/foundation/file/permissions.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""File permission utilities for Unix-like systems.

Provides safe, cross-platform utilities for working with file permissions including
parsing, formatting, and applying permission modes.
"""

from __future__ import annotations

from pathlib import Path

from provide.foundation.logger import get_logger

log = get_logger(__name__)

# Default permission constants
DEFAULT_FILE_PERMS = 0o644  # rw-r--r--
DEFAULT_DIR_PERMS = 0o755  # rwxr-xr-x
DEFAULT_EXECUTABLE_PERMS = 0o755  # rwxr-xr-x
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


def x_parse_permissions__mutmut_orig(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_1(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_2(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = None
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_3(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith(None):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_4(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("XX0oXX"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_5(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0O"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_6(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = None
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_7(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[3:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_8(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") or len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_9(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith(None) and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_10(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("XX0XX") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_11(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) >= 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_12(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 2:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_13(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = None

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_14(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[2:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_15(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(None, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_16(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, None)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_17(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_18(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(
            cleaned,
        )
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_19(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 9)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_20(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            None,
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_21(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=None,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_22(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=None,
        )
        return default


def x_parse_permissions__mutmut_23(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_24(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_25(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
        )
        return default


def x_parse_permissions__mutmut_26(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "XXInvalid permission string, using defaultXX",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_27(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "invalid permission string, using default",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_28(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "INVALID PERMISSION STRING, USING DEFAULT",
            perms_str=perms_str,
            default=oct(default),
        )
        return default


def x_parse_permissions__mutmut_29(perms_str: str | None, default: int = DEFAULT_FILE_PERMS) -> int:
    """Parse permission string to octal integer.

    Accepts various permission string formats:
    - Octal with prefix: "0o755", "0755"
    - Octal without prefix: "755"
    - Integer strings: "493" (decimal for 0o755)

    Args:
        perms_str: Permission string (e.g., "0755", "755", "0o755")
        default: Default permissions if parsing fails

    Returns:
        Permission as integer (e.g., 0o755 = 493)

    Examples:
        >>> parse_permissions("0755")
        493
        >>> parse_permissions("0o755")
        493
        >>> parse_permissions("755")
        493
        >>> parse_permissions(None)
        420
        >>> parse_permissions("invalid")
        420
    """
    if not perms_str:
        return default

    try:
        # Remove leading '0o' or '0' prefix if present
        cleaned = perms_str.strip()
        if cleaned.startswith("0o"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0") and len(cleaned) > 1:
            cleaned = cleaned[1:]

        # Try parsing as octal
        return int(cleaned, 8)
    except (ValueError, TypeError):
        log.warning(
            "Invalid permission string, using default",
            perms_str=perms_str,
            default=oct(None),
        )
        return default


x_parse_permissions__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_permissions__mutmut_1": x_parse_permissions__mutmut_1,
    "x_parse_permissions__mutmut_2": x_parse_permissions__mutmut_2,
    "x_parse_permissions__mutmut_3": x_parse_permissions__mutmut_3,
    "x_parse_permissions__mutmut_4": x_parse_permissions__mutmut_4,
    "x_parse_permissions__mutmut_5": x_parse_permissions__mutmut_5,
    "x_parse_permissions__mutmut_6": x_parse_permissions__mutmut_6,
    "x_parse_permissions__mutmut_7": x_parse_permissions__mutmut_7,
    "x_parse_permissions__mutmut_8": x_parse_permissions__mutmut_8,
    "x_parse_permissions__mutmut_9": x_parse_permissions__mutmut_9,
    "x_parse_permissions__mutmut_10": x_parse_permissions__mutmut_10,
    "x_parse_permissions__mutmut_11": x_parse_permissions__mutmut_11,
    "x_parse_permissions__mutmut_12": x_parse_permissions__mutmut_12,
    "x_parse_permissions__mutmut_13": x_parse_permissions__mutmut_13,
    "x_parse_permissions__mutmut_14": x_parse_permissions__mutmut_14,
    "x_parse_permissions__mutmut_15": x_parse_permissions__mutmut_15,
    "x_parse_permissions__mutmut_16": x_parse_permissions__mutmut_16,
    "x_parse_permissions__mutmut_17": x_parse_permissions__mutmut_17,
    "x_parse_permissions__mutmut_18": x_parse_permissions__mutmut_18,
    "x_parse_permissions__mutmut_19": x_parse_permissions__mutmut_19,
    "x_parse_permissions__mutmut_20": x_parse_permissions__mutmut_20,
    "x_parse_permissions__mutmut_21": x_parse_permissions__mutmut_21,
    "x_parse_permissions__mutmut_22": x_parse_permissions__mutmut_22,
    "x_parse_permissions__mutmut_23": x_parse_permissions__mutmut_23,
    "x_parse_permissions__mutmut_24": x_parse_permissions__mutmut_24,
    "x_parse_permissions__mutmut_25": x_parse_permissions__mutmut_25,
    "x_parse_permissions__mutmut_26": x_parse_permissions__mutmut_26,
    "x_parse_permissions__mutmut_27": x_parse_permissions__mutmut_27,
    "x_parse_permissions__mutmut_28": x_parse_permissions__mutmut_28,
    "x_parse_permissions__mutmut_29": x_parse_permissions__mutmut_29,
}


def parse_permissions(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_permissions__mutmut_orig, x_parse_permissions__mutmut_mutants, args, kwargs
    )
    return result


parse_permissions.__signature__ = _mutmut_signature(x_parse_permissions__mutmut_orig)
x_parse_permissions__mutmut_orig.__name__ = "x_parse_permissions"


def x_format_permissions__mutmut_orig(mode: int) -> str:
    """Format permission bits as octal string.

    Args:
        mode: Permission bits (can include file type bits)

    Returns:
        Formatted string like "0755" (last 3 octal digits only)

    Examples:
        >>> format_permissions(0o755)
        '0755'
        >>> format_permissions(0o644)
        '0644'
        >>> format_permissions(493)  # 0o755 in decimal
        '0755'
    """
    # Mask to only permission bits (last 9 bits = 3 octal digits)
    perms_only = mode & 0o777
    return f"0{perms_only:03o}"


def x_format_permissions__mutmut_1(mode: int) -> str:
    """Format permission bits as octal string.

    Args:
        mode: Permission bits (can include file type bits)

    Returns:
        Formatted string like "0755" (last 3 octal digits only)

    Examples:
        >>> format_permissions(0o755)
        '0755'
        >>> format_permissions(0o644)
        '0644'
        >>> format_permissions(493)  # 0o755 in decimal
        '0755'
    """
    # Mask to only permission bits (last 9 bits = 3 octal digits)
    perms_only = None
    return f"0{perms_only:03o}"


def x_format_permissions__mutmut_2(mode: int) -> str:
    """Format permission bits as octal string.

    Args:
        mode: Permission bits (can include file type bits)

    Returns:
        Formatted string like "0755" (last 3 octal digits only)

    Examples:
        >>> format_permissions(0o755)
        '0755'
        >>> format_permissions(0o644)
        '0644'
        >>> format_permissions(493)  # 0o755 in decimal
        '0755'
    """
    # Mask to only permission bits (last 9 bits = 3 octal digits)
    perms_only = mode | 0o777
    return f"0{perms_only:03o}"


def x_format_permissions__mutmut_3(mode: int) -> str:
    """Format permission bits as octal string.

    Args:
        mode: Permission bits (can include file type bits)

    Returns:
        Formatted string like "0755" (last 3 octal digits only)

    Examples:
        >>> format_permissions(0o755)
        '0755'
        >>> format_permissions(0o644)
        '0644'
        >>> format_permissions(493)  # 0o755 in decimal
        '0755'
    """
    # Mask to only permission bits (last 9 bits = 3 octal digits)
    perms_only = mode & 512
    return f"0{perms_only:03o}"


x_format_permissions__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_permissions__mutmut_1": x_format_permissions__mutmut_1,
    "x_format_permissions__mutmut_2": x_format_permissions__mutmut_2,
    "x_format_permissions__mutmut_3": x_format_permissions__mutmut_3,
}


def format_permissions(*args, **kwargs):
    result = _mutmut_trampoline(
        x_format_permissions__mutmut_orig, x_format_permissions__mutmut_mutants, args, kwargs
    )
    return result


format_permissions.__signature__ = _mutmut_signature(x_format_permissions__mutmut_orig)
x_format_permissions__mutmut_orig.__name__ = "x_format_permissions"


def x_set_file_permissions__mutmut_orig(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_1(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(None)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_2(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(None).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_3(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            None,
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_4(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=None,
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_5(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=None,
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_6(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_7(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_8(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_9(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "XXSet file permissionsXX",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_10(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_11(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "SET FILE PERMISSIONS",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_12(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(None),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_13(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(None),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_14(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            None,
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_15(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=None,
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_16(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=None,
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_17(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=None,
        )
        raise


def x_set_file_permissions__mutmut_18(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_19(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_20(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_21(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
        raise


def x_set_file_permissions__mutmut_22(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "XXCould not set permissionsXX",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_23(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_24(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "COULD NOT SET PERMISSIONS",
            path=str(path),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_25(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(None),
            mode=format_permissions(mode),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_26(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(None),
            error=str(e),
        )
        raise


def x_set_file_permissions__mutmut_27(path: Path, mode: int) -> None:
    """Set file permissions safely with error handling.

    Args:
        path: File or directory path
        mode: Unix permission mode (e.g., 0o755)

    Raises:
        OSError: If setting permissions fails on the underlying filesystem

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> set_file_permissions(p, 0o644)
    """
    try:
        Path(path).chmod(mode)
        log.trace(
            "Set file permissions",
            path=str(path),
            mode=format_permissions(mode),
        )
    except OSError as e:
        log.warning(
            "Could not set permissions",
            path=str(path),
            mode=format_permissions(mode),
            error=str(None),
        )
        raise


x_set_file_permissions__mutmut_mutants: ClassVar[MutantDict] = {
    "x_set_file_permissions__mutmut_1": x_set_file_permissions__mutmut_1,
    "x_set_file_permissions__mutmut_2": x_set_file_permissions__mutmut_2,
    "x_set_file_permissions__mutmut_3": x_set_file_permissions__mutmut_3,
    "x_set_file_permissions__mutmut_4": x_set_file_permissions__mutmut_4,
    "x_set_file_permissions__mutmut_5": x_set_file_permissions__mutmut_5,
    "x_set_file_permissions__mutmut_6": x_set_file_permissions__mutmut_6,
    "x_set_file_permissions__mutmut_7": x_set_file_permissions__mutmut_7,
    "x_set_file_permissions__mutmut_8": x_set_file_permissions__mutmut_8,
    "x_set_file_permissions__mutmut_9": x_set_file_permissions__mutmut_9,
    "x_set_file_permissions__mutmut_10": x_set_file_permissions__mutmut_10,
    "x_set_file_permissions__mutmut_11": x_set_file_permissions__mutmut_11,
    "x_set_file_permissions__mutmut_12": x_set_file_permissions__mutmut_12,
    "x_set_file_permissions__mutmut_13": x_set_file_permissions__mutmut_13,
    "x_set_file_permissions__mutmut_14": x_set_file_permissions__mutmut_14,
    "x_set_file_permissions__mutmut_15": x_set_file_permissions__mutmut_15,
    "x_set_file_permissions__mutmut_16": x_set_file_permissions__mutmut_16,
    "x_set_file_permissions__mutmut_17": x_set_file_permissions__mutmut_17,
    "x_set_file_permissions__mutmut_18": x_set_file_permissions__mutmut_18,
    "x_set_file_permissions__mutmut_19": x_set_file_permissions__mutmut_19,
    "x_set_file_permissions__mutmut_20": x_set_file_permissions__mutmut_20,
    "x_set_file_permissions__mutmut_21": x_set_file_permissions__mutmut_21,
    "x_set_file_permissions__mutmut_22": x_set_file_permissions__mutmut_22,
    "x_set_file_permissions__mutmut_23": x_set_file_permissions__mutmut_23,
    "x_set_file_permissions__mutmut_24": x_set_file_permissions__mutmut_24,
    "x_set_file_permissions__mutmut_25": x_set_file_permissions__mutmut_25,
    "x_set_file_permissions__mutmut_26": x_set_file_permissions__mutmut_26,
    "x_set_file_permissions__mutmut_27": x_set_file_permissions__mutmut_27,
}


def set_file_permissions(*args, **kwargs):
    result = _mutmut_trampoline(
        x_set_file_permissions__mutmut_orig, x_set_file_permissions__mutmut_mutants, args, kwargs
    )
    return result


set_file_permissions.__signature__ = _mutmut_signature(x_set_file_permissions__mutmut_orig)
x_set_file_permissions__mutmut_orig.__name__ = "x_set_file_permissions"


def x_get_permissions__mutmut_orig(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_1(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode | 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_2(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 512
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_3(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            None,
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_4(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=None,
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_5(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=None,
        )
        return 0


def x_get_permissions__mutmut_6(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_7(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_8(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
        )
        return 0


def x_get_permissions__mutmut_9(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "XXCould not read permissionsXX",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_10(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_11(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "COULD NOT READ PERMISSIONS",
            path=str(path),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_12(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(None),
            error=str(e),
        )
        return 0


def x_get_permissions__mutmut_13(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(None),
        )
        return 0


def x_get_permissions__mutmut_14(path: Path) -> int:
    """Get current file permissions.

    Args:
        path: File or directory path

    Returns:
        Permission bits as integer (0 if file doesn't exist or error)

    Examples:
        >>> from pathlib import Path
        >>> p = Path("/tmp/test.txt")
        >>> p.touch()
        >>> p.chmod(0o644)
        >>> get_permissions(p)
        420
        >>> format_permissions(get_permissions(p))
        '0644'
    """
    try:
        return path.stat().st_mode & 0o777
    except OSError as e:
        log.debug(
            "Could not read permissions",
            path=str(path),
            error=str(e),
        )
        return 1


x_get_permissions__mutmut_mutants: ClassVar[MutantDict] = {
    "x_get_permissions__mutmut_1": x_get_permissions__mutmut_1,
    "x_get_permissions__mutmut_2": x_get_permissions__mutmut_2,
    "x_get_permissions__mutmut_3": x_get_permissions__mutmut_3,
    "x_get_permissions__mutmut_4": x_get_permissions__mutmut_4,
    "x_get_permissions__mutmut_5": x_get_permissions__mutmut_5,
    "x_get_permissions__mutmut_6": x_get_permissions__mutmut_6,
    "x_get_permissions__mutmut_7": x_get_permissions__mutmut_7,
    "x_get_permissions__mutmut_8": x_get_permissions__mutmut_8,
    "x_get_permissions__mutmut_9": x_get_permissions__mutmut_9,
    "x_get_permissions__mutmut_10": x_get_permissions__mutmut_10,
    "x_get_permissions__mutmut_11": x_get_permissions__mutmut_11,
    "x_get_permissions__mutmut_12": x_get_permissions__mutmut_12,
    "x_get_permissions__mutmut_13": x_get_permissions__mutmut_13,
    "x_get_permissions__mutmut_14": x_get_permissions__mutmut_14,
}


def get_permissions(*args, **kwargs):
    result = _mutmut_trampoline(
        x_get_permissions__mutmut_orig, x_get_permissions__mutmut_mutants, args, kwargs
    )
    return result


get_permissions.__signature__ = _mutmut_signature(x_get_permissions__mutmut_orig)
x_get_permissions__mutmut_orig.__name__ = "x_get_permissions"


def x_ensure_secure_permissions__mutmut_orig(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_1(
    path: Path,
    is_executable: bool = True,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_2(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = None
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_3(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = None
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_4(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = None

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_5(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(None, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_6(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, None)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_7(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_8(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(
        path,
    )
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_9(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        None,
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_10(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=None,
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_11(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=None,
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_12(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=None,
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_13(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=None,
    )


def x_ensure_secure_permissions__mutmut_14(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_15(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_16(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_17(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_18(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
    )


def x_ensure_secure_permissions__mutmut_19(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "XXApplied secure permissionsXX",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_20(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "applied secure permissions",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_21(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "APPLIED SECURE PERMISSIONS",
        path=str(path),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_22(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(None),
        mode=format_permissions(mode),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


def x_ensure_secure_permissions__mutmut_23(
    path: Path,
    is_executable: bool = False,
    file_mode: int = DEFAULT_FILE_PERMS,
    dir_mode: int = DEFAULT_DIR_PERMS,
    executable_mode: int = DEFAULT_EXECUTABLE_PERMS,
) -> None:
    """Apply secure default permissions to a file or directory.

    Automatically determines the appropriate permission mode based on whether
    the path is a file, directory, or executable.

    Args:
        path: Path to file or directory
        is_executable: Whether file should be executable (ignored for directories)
        file_mode: Permission mode for regular files
        dir_mode: Permission mode for directories
        executable_mode: Permission mode for executable files

    Examples:
        >>> from pathlib import Path
        >>> # Regular file gets 0o644
        >>> p = Path("/tmp/file.txt")
        >>> p.touch()
        >>> ensure_secure_permissions(p)

        >>> # Executable gets 0o755
        >>> p2 = Path("/tmp/script.sh")
        >>> p2.touch()
        >>> ensure_secure_permissions(p2, is_executable=True)

        >>> # Directory gets 0o755
        >>> d = Path("/tmp/mydir")
        >>> d.mkdir(exist_ok=True)
        >>> ensure_secure_permissions(d)
    """
    if path.is_dir():
        mode = dir_mode
    elif is_executable:
        mode = executable_mode
    else:
        mode = file_mode

    set_file_permissions(path, mode)
    log.trace(
        "Applied secure permissions",
        path=str(path),
        mode=format_permissions(None),
        is_dir=path.is_dir(),
        is_executable=is_executable,
    )


x_ensure_secure_permissions__mutmut_mutants: ClassVar[MutantDict] = {
    "x_ensure_secure_permissions__mutmut_1": x_ensure_secure_permissions__mutmut_1,
    "x_ensure_secure_permissions__mutmut_2": x_ensure_secure_permissions__mutmut_2,
    "x_ensure_secure_permissions__mutmut_3": x_ensure_secure_permissions__mutmut_3,
    "x_ensure_secure_permissions__mutmut_4": x_ensure_secure_permissions__mutmut_4,
    "x_ensure_secure_permissions__mutmut_5": x_ensure_secure_permissions__mutmut_5,
    "x_ensure_secure_permissions__mutmut_6": x_ensure_secure_permissions__mutmut_6,
    "x_ensure_secure_permissions__mutmut_7": x_ensure_secure_permissions__mutmut_7,
    "x_ensure_secure_permissions__mutmut_8": x_ensure_secure_permissions__mutmut_8,
    "x_ensure_secure_permissions__mutmut_9": x_ensure_secure_permissions__mutmut_9,
    "x_ensure_secure_permissions__mutmut_10": x_ensure_secure_permissions__mutmut_10,
    "x_ensure_secure_permissions__mutmut_11": x_ensure_secure_permissions__mutmut_11,
    "x_ensure_secure_permissions__mutmut_12": x_ensure_secure_permissions__mutmut_12,
    "x_ensure_secure_permissions__mutmut_13": x_ensure_secure_permissions__mutmut_13,
    "x_ensure_secure_permissions__mutmut_14": x_ensure_secure_permissions__mutmut_14,
    "x_ensure_secure_permissions__mutmut_15": x_ensure_secure_permissions__mutmut_15,
    "x_ensure_secure_permissions__mutmut_16": x_ensure_secure_permissions__mutmut_16,
    "x_ensure_secure_permissions__mutmut_17": x_ensure_secure_permissions__mutmut_17,
    "x_ensure_secure_permissions__mutmut_18": x_ensure_secure_permissions__mutmut_18,
    "x_ensure_secure_permissions__mutmut_19": x_ensure_secure_permissions__mutmut_19,
    "x_ensure_secure_permissions__mutmut_20": x_ensure_secure_permissions__mutmut_20,
    "x_ensure_secure_permissions__mutmut_21": x_ensure_secure_permissions__mutmut_21,
    "x_ensure_secure_permissions__mutmut_22": x_ensure_secure_permissions__mutmut_22,
    "x_ensure_secure_permissions__mutmut_23": x_ensure_secure_permissions__mutmut_23,
}


def ensure_secure_permissions(*args, **kwargs):
    result = _mutmut_trampoline(
        x_ensure_secure_permissions__mutmut_orig, x_ensure_secure_permissions__mutmut_mutants, args, kwargs
    )
    return result


ensure_secure_permissions.__signature__ = _mutmut_signature(x_ensure_secure_permissions__mutmut_orig)
x_ensure_secure_permissions__mutmut_orig.__name__ = "x_ensure_secure_permissions"


__all__ = [
    "DEFAULT_DIR_PERMS",
    "DEFAULT_EXECUTABLE_PERMS",
    "DEFAULT_FILE_PERMS",
    "ensure_secure_permissions",
    "format_permissions",
    "get_permissions",
    "parse_permissions",
    "set_file_permissions",
]


# <3 🧱🤝📄🪄
