# provide/foundation/formatting/numbers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Size, duration, and number formatting utilities.

Provides utilities for human-readable formatting of sizes, durations,
and numeric values.
"""
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


def x_format_size__mutmut_orig(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_1(size_bytes: float, precision: int = 2) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_2(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes != 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_3(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 1:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_4(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "XX0 BXX"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_5(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 b"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_6(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = None
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_7(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes <= 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_8(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 1
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_9(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = None

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_10(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(None)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_11(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = None
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_12(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["XXBXX", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_13(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["b", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_14(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "XXKBXX", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_15(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "kb", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_16(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "XXMBXX", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_17(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "mb", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_18(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "XXGBXX", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_19(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "gb", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_20(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "XXTBXX", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_21(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "tb", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_22(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "XXPBXX", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_23(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "pb", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_24(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "XXEBXX"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_25(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "eb"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_26(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = None

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_27(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 1

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_28(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 or unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_29(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes > 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_30(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1025.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_31(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index <= len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_32(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) + 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_33(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 2:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_34(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes = 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_35(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes *= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_36(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1025.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_37(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index = 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_38(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index -= 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_39(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 2

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_40(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index != 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_41(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 1:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_42(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = None
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_43(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(None)} {units[unit_index]}"
    else:
        formatted = f"{size_bytes:.{precision}f} {units[unit_index]}"

    return f"-{formatted}" if negative else formatted


def x_format_size__mutmut_44(size_bytes: float, precision: int = 1) -> str:
    """Format bytes as human-readable size.

    Args:
        size_bytes: Size in bytes
        precision: Decimal places for display

    Returns:
        Human-readable size string

    Examples:
        >>> format_size(1024)
        '1.0 KB'
        >>> format_size(1536)
        '1.5 KB'
        >>> format_size(1073741824)
        '1.0 GB'
        >>> format_size(0)
        '0 B'

    """
    if size_bytes == 0:
        return "0 B"

    # Handle negative sizes
    negative = size_bytes < 0
    size_bytes = abs(size_bytes)

    units = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
    unit_index = 0

    while size_bytes >= 1024.0 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    # Format with specified precision
    if unit_index == 0:
        # Bytes - no decimal places
        formatted = f"{int(size_bytes)} {units[unit_index]}"
    else:
        formatted = None

    return f"-{formatted}" if negative else formatted


x_format_size__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_size__mutmut_1": x_format_size__mutmut_1,
    "x_format_size__mutmut_2": x_format_size__mutmut_2,
    "x_format_size__mutmut_3": x_format_size__mutmut_3,
    "x_format_size__mutmut_4": x_format_size__mutmut_4,
    "x_format_size__mutmut_5": x_format_size__mutmut_5,
    "x_format_size__mutmut_6": x_format_size__mutmut_6,
    "x_format_size__mutmut_7": x_format_size__mutmut_7,
    "x_format_size__mutmut_8": x_format_size__mutmut_8,
    "x_format_size__mutmut_9": x_format_size__mutmut_9,
    "x_format_size__mutmut_10": x_format_size__mutmut_10,
    "x_format_size__mutmut_11": x_format_size__mutmut_11,
    "x_format_size__mutmut_12": x_format_size__mutmut_12,
    "x_format_size__mutmut_13": x_format_size__mutmut_13,
    "x_format_size__mutmut_14": x_format_size__mutmut_14,
    "x_format_size__mutmut_15": x_format_size__mutmut_15,
    "x_format_size__mutmut_16": x_format_size__mutmut_16,
    "x_format_size__mutmut_17": x_format_size__mutmut_17,
    "x_format_size__mutmut_18": x_format_size__mutmut_18,
    "x_format_size__mutmut_19": x_format_size__mutmut_19,
    "x_format_size__mutmut_20": x_format_size__mutmut_20,
    "x_format_size__mutmut_21": x_format_size__mutmut_21,
    "x_format_size__mutmut_22": x_format_size__mutmut_22,
    "x_format_size__mutmut_23": x_format_size__mutmut_23,
    "x_format_size__mutmut_24": x_format_size__mutmut_24,
    "x_format_size__mutmut_25": x_format_size__mutmut_25,
    "x_format_size__mutmut_26": x_format_size__mutmut_26,
    "x_format_size__mutmut_27": x_format_size__mutmut_27,
    "x_format_size__mutmut_28": x_format_size__mutmut_28,
    "x_format_size__mutmut_29": x_format_size__mutmut_29,
    "x_format_size__mutmut_30": x_format_size__mutmut_30,
    "x_format_size__mutmut_31": x_format_size__mutmut_31,
    "x_format_size__mutmut_32": x_format_size__mutmut_32,
    "x_format_size__mutmut_33": x_format_size__mutmut_33,
    "x_format_size__mutmut_34": x_format_size__mutmut_34,
    "x_format_size__mutmut_35": x_format_size__mutmut_35,
    "x_format_size__mutmut_36": x_format_size__mutmut_36,
    "x_format_size__mutmut_37": x_format_size__mutmut_37,
    "x_format_size__mutmut_38": x_format_size__mutmut_38,
    "x_format_size__mutmut_39": x_format_size__mutmut_39,
    "x_format_size__mutmut_40": x_format_size__mutmut_40,
    "x_format_size__mutmut_41": x_format_size__mutmut_41,
    "x_format_size__mutmut_42": x_format_size__mutmut_42,
    "x_format_size__mutmut_43": x_format_size__mutmut_43,
    "x_format_size__mutmut_44": x_format_size__mutmut_44,
}


def format_size(*args, **kwargs):
    result = _mutmut_trampoline(x_format_size__mutmut_orig, x_format_size__mutmut_mutants, args, kwargs)
    return result


format_size.__signature__ = _mutmut_signature(x_format_size__mutmut_orig)
x_format_size__mutmut_orig.__name__ = "x_format_size"


def _format_duration_components(
    days: int, hours: int, minutes: int, seconds: int
) -> tuple[int, int, int, int]:
    """Extract duration components from seconds."""
    return (
        days,
        hours,
        minutes,
        seconds,
    )


def x__format_duration_short__mutmut_orig(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_1(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = None
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_2(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days >= 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_3(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 1:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_4(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(None)
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_5(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours >= 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_6(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 1:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_7(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(None)
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_8(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes >= 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_9(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 1:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_10(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(None)
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_11(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 and not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_12(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds >= 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_13(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 1 or not parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_14(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or parts:
        parts.append(f"{seconds}s")
    return "".join(parts)


def x__format_duration_short__mutmut_15(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(None)
    return "".join(parts)


def x__format_duration_short__mutmut_16(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "".join(None)


def x__format_duration_short__mutmut_17(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in short format (1h30m)."""
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return "XXXX".join(parts)


x__format_duration_short__mutmut_mutants: ClassVar[MutantDict] = {
    "x__format_duration_short__mutmut_1": x__format_duration_short__mutmut_1,
    "x__format_duration_short__mutmut_2": x__format_duration_short__mutmut_2,
    "x__format_duration_short__mutmut_3": x__format_duration_short__mutmut_3,
    "x__format_duration_short__mutmut_4": x__format_duration_short__mutmut_4,
    "x__format_duration_short__mutmut_5": x__format_duration_short__mutmut_5,
    "x__format_duration_short__mutmut_6": x__format_duration_short__mutmut_6,
    "x__format_duration_short__mutmut_7": x__format_duration_short__mutmut_7,
    "x__format_duration_short__mutmut_8": x__format_duration_short__mutmut_8,
    "x__format_duration_short__mutmut_9": x__format_duration_short__mutmut_9,
    "x__format_duration_short__mutmut_10": x__format_duration_short__mutmut_10,
    "x__format_duration_short__mutmut_11": x__format_duration_short__mutmut_11,
    "x__format_duration_short__mutmut_12": x__format_duration_short__mutmut_12,
    "x__format_duration_short__mutmut_13": x__format_duration_short__mutmut_13,
    "x__format_duration_short__mutmut_14": x__format_duration_short__mutmut_14,
    "x__format_duration_short__mutmut_15": x__format_duration_short__mutmut_15,
    "x__format_duration_short__mutmut_16": x__format_duration_short__mutmut_16,
    "x__format_duration_short__mutmut_17": x__format_duration_short__mutmut_17,
}


def _format_duration_short(*args, **kwargs):
    result = _mutmut_trampoline(
        x__format_duration_short__mutmut_orig, x__format_duration_short__mutmut_mutants, args, kwargs
    )
    return result


_format_duration_short.__signature__ = _mutmut_signature(x__format_duration_short__mutmut_orig)
x__format_duration_short__mutmut_orig.__name__ = "x__format_duration_short"


def x__format_duration_long__mutmut_orig(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_1(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = None
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_2(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days >= 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_3(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 1:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_4(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(None)
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_5(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'XXsXX' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_6(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'S' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_7(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days == 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_8(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 2 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_9(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else 'XXXX'}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_10(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours >= 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_11(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 1:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_12(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(None)
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_13(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'XXsXX' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_14(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'S' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_15(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours == 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_16(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 2 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_17(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else 'XXXX'}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_18(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes >= 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_19(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 1:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_20(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(None)
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_21(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'XXsXX' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_22(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'S' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_23(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes == 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_24(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 2 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_25(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else 'XXXX'}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_26(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 and not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_27(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds >= 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_28(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 1 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_29(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_30(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(None)
    return " ".join(parts)


def x__format_duration_long__mutmut_31(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'XXsXX' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_32(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'S' if seconds != 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_33(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds == 1 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_34(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 2 else ''}")
    return " ".join(parts)


def x__format_duration_long__mutmut_35(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else 'XXXX'}")
    return " ".join(parts)


def x__format_duration_long__mutmut_36(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return " ".join(None)


def x__format_duration_long__mutmut_37(days: int, hours: int, minutes: int, seconds: int) -> str:
    """Format duration in long format (1 hour 30 minutes)."""
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return "XX XX".join(parts)


x__format_duration_long__mutmut_mutants: ClassVar[MutantDict] = {
    "x__format_duration_long__mutmut_1": x__format_duration_long__mutmut_1,
    "x__format_duration_long__mutmut_2": x__format_duration_long__mutmut_2,
    "x__format_duration_long__mutmut_3": x__format_duration_long__mutmut_3,
    "x__format_duration_long__mutmut_4": x__format_duration_long__mutmut_4,
    "x__format_duration_long__mutmut_5": x__format_duration_long__mutmut_5,
    "x__format_duration_long__mutmut_6": x__format_duration_long__mutmut_6,
    "x__format_duration_long__mutmut_7": x__format_duration_long__mutmut_7,
    "x__format_duration_long__mutmut_8": x__format_duration_long__mutmut_8,
    "x__format_duration_long__mutmut_9": x__format_duration_long__mutmut_9,
    "x__format_duration_long__mutmut_10": x__format_duration_long__mutmut_10,
    "x__format_duration_long__mutmut_11": x__format_duration_long__mutmut_11,
    "x__format_duration_long__mutmut_12": x__format_duration_long__mutmut_12,
    "x__format_duration_long__mutmut_13": x__format_duration_long__mutmut_13,
    "x__format_duration_long__mutmut_14": x__format_duration_long__mutmut_14,
    "x__format_duration_long__mutmut_15": x__format_duration_long__mutmut_15,
    "x__format_duration_long__mutmut_16": x__format_duration_long__mutmut_16,
    "x__format_duration_long__mutmut_17": x__format_duration_long__mutmut_17,
    "x__format_duration_long__mutmut_18": x__format_duration_long__mutmut_18,
    "x__format_duration_long__mutmut_19": x__format_duration_long__mutmut_19,
    "x__format_duration_long__mutmut_20": x__format_duration_long__mutmut_20,
    "x__format_duration_long__mutmut_21": x__format_duration_long__mutmut_21,
    "x__format_duration_long__mutmut_22": x__format_duration_long__mutmut_22,
    "x__format_duration_long__mutmut_23": x__format_duration_long__mutmut_23,
    "x__format_duration_long__mutmut_24": x__format_duration_long__mutmut_24,
    "x__format_duration_long__mutmut_25": x__format_duration_long__mutmut_25,
    "x__format_duration_long__mutmut_26": x__format_duration_long__mutmut_26,
    "x__format_duration_long__mutmut_27": x__format_duration_long__mutmut_27,
    "x__format_duration_long__mutmut_28": x__format_duration_long__mutmut_28,
    "x__format_duration_long__mutmut_29": x__format_duration_long__mutmut_29,
    "x__format_duration_long__mutmut_30": x__format_duration_long__mutmut_30,
    "x__format_duration_long__mutmut_31": x__format_duration_long__mutmut_31,
    "x__format_duration_long__mutmut_32": x__format_duration_long__mutmut_32,
    "x__format_duration_long__mutmut_33": x__format_duration_long__mutmut_33,
    "x__format_duration_long__mutmut_34": x__format_duration_long__mutmut_34,
    "x__format_duration_long__mutmut_35": x__format_duration_long__mutmut_35,
    "x__format_duration_long__mutmut_36": x__format_duration_long__mutmut_36,
    "x__format_duration_long__mutmut_37": x__format_duration_long__mutmut_37,
}


def _format_duration_long(*args, **kwargs):
    result = _mutmut_trampoline(
        x__format_duration_long__mutmut_orig, x__format_duration_long__mutmut_mutants, args, kwargs
    )
    return result


_format_duration_long.__signature__ = _mutmut_signature(x__format_duration_long__mutmut_orig)
x__format_duration_long__mutmut_orig.__name__ = "x__format_duration_long"


def x_format_duration__mutmut_orig(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_1(seconds: float, short: bool = True) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_2(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds <= 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_3(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 1:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_4(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(None, short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_5(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), None)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_6(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_7(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds))}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_8(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(None), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_9(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds != 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_10(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 1:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_11(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "XX0sXX" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_12(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0S" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_13(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "XX0 secondsXX"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_14(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 SECONDS"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_15(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = None
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_16(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(None)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_17(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds / 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_18(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86401)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_19(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = None
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_20(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int(None)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_21(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) / 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_22(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds / 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_23(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86401) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_24(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3601)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_25(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = None
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_26(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int(None)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_27(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) / 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_28(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds / 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_29(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3601) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_30(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 61)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_31(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = None

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_32(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(None)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_33(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds / 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_34(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 61)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_35(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(None, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_36(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, None, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_37(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, None, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_38(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, None)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_39(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_40(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, minutes, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_41(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, secs)
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_42(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(
            days,
            hours,
            minutes,
        )
    return _format_duration_long(days, hours, minutes, secs)


def x_format_duration__mutmut_43(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(None, hours, minutes, secs)


def x_format_duration__mutmut_44(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, None, minutes, secs)


def x_format_duration__mutmut_45(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, None, secs)


def x_format_duration__mutmut_46(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, minutes, None)


def x_format_duration__mutmut_47(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(hours, minutes, secs)


def x_format_duration__mutmut_48(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, minutes, secs)


def x_format_duration__mutmut_49(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(days, hours, secs)


def x_format_duration__mutmut_50(seconds: float, short: bool = False) -> str:
    """Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds
        short: Use short format (1h30m vs 1 hour 30 minutes)

    Returns:
        Human-readable duration string

    Examples:
        >>> format_duration(90)
        '1 minute 30 seconds'
        >>> format_duration(90, short=True)
        '1m30s'
        >>> format_duration(3661)
        '1 hour 1 minute 1 second'
        >>> format_duration(3661, short=True)
        '1h1m1s'

    """
    if seconds < 0:
        return f"-{format_duration(abs(seconds), short)}"

    if seconds == 0:
        return "0s" if short else "0 seconds"

    # Calculate components
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if short:
        return _format_duration_short(days, hours, minutes, secs)
    return _format_duration_long(
        days,
        hours,
        minutes,
    )


x_format_duration__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_duration__mutmut_1": x_format_duration__mutmut_1,
    "x_format_duration__mutmut_2": x_format_duration__mutmut_2,
    "x_format_duration__mutmut_3": x_format_duration__mutmut_3,
    "x_format_duration__mutmut_4": x_format_duration__mutmut_4,
    "x_format_duration__mutmut_5": x_format_duration__mutmut_5,
    "x_format_duration__mutmut_6": x_format_duration__mutmut_6,
    "x_format_duration__mutmut_7": x_format_duration__mutmut_7,
    "x_format_duration__mutmut_8": x_format_duration__mutmut_8,
    "x_format_duration__mutmut_9": x_format_duration__mutmut_9,
    "x_format_duration__mutmut_10": x_format_duration__mutmut_10,
    "x_format_duration__mutmut_11": x_format_duration__mutmut_11,
    "x_format_duration__mutmut_12": x_format_duration__mutmut_12,
    "x_format_duration__mutmut_13": x_format_duration__mutmut_13,
    "x_format_duration__mutmut_14": x_format_duration__mutmut_14,
    "x_format_duration__mutmut_15": x_format_duration__mutmut_15,
    "x_format_duration__mutmut_16": x_format_duration__mutmut_16,
    "x_format_duration__mutmut_17": x_format_duration__mutmut_17,
    "x_format_duration__mutmut_18": x_format_duration__mutmut_18,
    "x_format_duration__mutmut_19": x_format_duration__mutmut_19,
    "x_format_duration__mutmut_20": x_format_duration__mutmut_20,
    "x_format_duration__mutmut_21": x_format_duration__mutmut_21,
    "x_format_duration__mutmut_22": x_format_duration__mutmut_22,
    "x_format_duration__mutmut_23": x_format_duration__mutmut_23,
    "x_format_duration__mutmut_24": x_format_duration__mutmut_24,
    "x_format_duration__mutmut_25": x_format_duration__mutmut_25,
    "x_format_duration__mutmut_26": x_format_duration__mutmut_26,
    "x_format_duration__mutmut_27": x_format_duration__mutmut_27,
    "x_format_duration__mutmut_28": x_format_duration__mutmut_28,
    "x_format_duration__mutmut_29": x_format_duration__mutmut_29,
    "x_format_duration__mutmut_30": x_format_duration__mutmut_30,
    "x_format_duration__mutmut_31": x_format_duration__mutmut_31,
    "x_format_duration__mutmut_32": x_format_duration__mutmut_32,
    "x_format_duration__mutmut_33": x_format_duration__mutmut_33,
    "x_format_duration__mutmut_34": x_format_duration__mutmut_34,
    "x_format_duration__mutmut_35": x_format_duration__mutmut_35,
    "x_format_duration__mutmut_36": x_format_duration__mutmut_36,
    "x_format_duration__mutmut_37": x_format_duration__mutmut_37,
    "x_format_duration__mutmut_38": x_format_duration__mutmut_38,
    "x_format_duration__mutmut_39": x_format_duration__mutmut_39,
    "x_format_duration__mutmut_40": x_format_duration__mutmut_40,
    "x_format_duration__mutmut_41": x_format_duration__mutmut_41,
    "x_format_duration__mutmut_42": x_format_duration__mutmut_42,
    "x_format_duration__mutmut_43": x_format_duration__mutmut_43,
    "x_format_duration__mutmut_44": x_format_duration__mutmut_44,
    "x_format_duration__mutmut_45": x_format_duration__mutmut_45,
    "x_format_duration__mutmut_46": x_format_duration__mutmut_46,
    "x_format_duration__mutmut_47": x_format_duration__mutmut_47,
    "x_format_duration__mutmut_48": x_format_duration__mutmut_48,
    "x_format_duration__mutmut_49": x_format_duration__mutmut_49,
    "x_format_duration__mutmut_50": x_format_duration__mutmut_50,
}


def format_duration(*args, **kwargs):
    result = _mutmut_trampoline(
        x_format_duration__mutmut_orig, x_format_duration__mutmut_mutants, args, kwargs
    )
    return result


format_duration.__signature__ = _mutmut_signature(x_format_duration__mutmut_orig)
x_format_duration__mutmut_orig.__name__ = "x_format_duration"


def x_format_number__mutmut_orig(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").rstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_1(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is not None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").rstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_2(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").rstrip(None)
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_3(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").lstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_4(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip(None).rstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_5(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".lstrip("0").rstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_6(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("XX0XX").rstrip(".")
    return f"{num:,.{precision}f}"


def x_format_number__mutmut_7(num: float, precision: int | None = None) -> str:
    """Format number with thousands separators.

    Args:
        num: Number to format
        precision: Decimal places (None for automatic)

    Returns:
        Formatted number string

    Examples:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, precision=2)
        '1,234.57'

    """
    if precision is None:
        if isinstance(num, int):
            return f"{num:,}"
        # Auto precision for floats
        return f"{num:,.6f}".rstrip("0").rstrip("XX.XX")
    return f"{num:,.{precision}f}"


x_format_number__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_number__mutmut_1": x_format_number__mutmut_1,
    "x_format_number__mutmut_2": x_format_number__mutmut_2,
    "x_format_number__mutmut_3": x_format_number__mutmut_3,
    "x_format_number__mutmut_4": x_format_number__mutmut_4,
    "x_format_number__mutmut_5": x_format_number__mutmut_5,
    "x_format_number__mutmut_6": x_format_number__mutmut_6,
    "x_format_number__mutmut_7": x_format_number__mutmut_7,
}


def format_number(*args, **kwargs):
    result = _mutmut_trampoline(x_format_number__mutmut_orig, x_format_number__mutmut_mutants, args, kwargs)
    return result


format_number.__signature__ = _mutmut_signature(x_format_number__mutmut_orig)
x_format_number__mutmut_orig.__name__ = "x_format_number"


def x_format_percentage__mutmut_orig(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_1(value: float, precision: int = 2, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_2(value: float, precision: int = 1, include_sign: bool = True) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_3(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = None
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_4(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value / 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_5(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 101
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_6(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = None

    if include_sign and value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_7(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign or value > 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_8(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value >= 0:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_9(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 1:
        formatted = f"+{formatted}"

    return formatted


def x_format_percentage__mutmut_10(value: float, precision: int = 1, include_sign: bool = False) -> str:
    """Format value as percentage.

    Args:
        value: Value to format (0.5 = 50%)
        precision: Decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(0.5)
        '50.0%'
        >>> format_percentage(0.1234, precision=2)
        '12.34%'
        >>> format_percentage(0.05, include_sign=True)
        '+5.0%'

    """
    percentage = value * 100
    formatted = f"{percentage:.{precision}f}%"

    if include_sign and value > 0:
        formatted = None

    return formatted


x_format_percentage__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_percentage__mutmut_1": x_format_percentage__mutmut_1,
    "x_format_percentage__mutmut_2": x_format_percentage__mutmut_2,
    "x_format_percentage__mutmut_3": x_format_percentage__mutmut_3,
    "x_format_percentage__mutmut_4": x_format_percentage__mutmut_4,
    "x_format_percentage__mutmut_5": x_format_percentage__mutmut_5,
    "x_format_percentage__mutmut_6": x_format_percentage__mutmut_6,
    "x_format_percentage__mutmut_7": x_format_percentage__mutmut_7,
    "x_format_percentage__mutmut_8": x_format_percentage__mutmut_8,
    "x_format_percentage__mutmut_9": x_format_percentage__mutmut_9,
    "x_format_percentage__mutmut_10": x_format_percentage__mutmut_10,
}


def format_percentage(*args, **kwargs):
    result = _mutmut_trampoline(
        x_format_percentage__mutmut_orig, x_format_percentage__mutmut_mutants, args, kwargs
    )
    return result


format_percentage.__signature__ = _mutmut_signature(x_format_percentage__mutmut_orig)
x_format_percentage__mutmut_orig.__name__ = "x_format_percentage"


__all__ = [
    "format_duration",
    "format_number",
    "format_percentage",
    "format_size",
]


# <3 🧱🤝🎨🪄
