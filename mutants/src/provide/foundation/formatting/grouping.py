# provide/foundation/formatting/grouping.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""String grouping utilities.

Provides utilities for formatting strings with grouping separators,
useful for hash values, IDs, and other long strings.
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


def x_format_grouped__mutmut_orig(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_1(
    text: str,
    group_size: int = 9,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_2(
    text: str,
    group_size: int = 8,
    groups: int = 1,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_3(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = "XX XX",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_4(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size < 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_5(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 1:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_6(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = None
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_7(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(None, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_8(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, None, group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_9(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), None):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_10(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_11(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_12(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(
        0,
        len(text),
    ):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_13(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(1, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_14(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(None)
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_15(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i - group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_16(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 or len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_17(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups >= 0 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_18(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 1 and len(formatted_parts) >= groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_19(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) > groups:
            break

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_20(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            return

    return separator.join(formatted_parts)


def x_format_grouped__mutmut_21(
    text: str,
    group_size: int = 8,
    groups: int = 0,
    separator: str = " ",
) -> str:
    """Format a string with grouping separators for display.

    Args:
        text: Text to format
        group_size: Number of characters per group
        groups: Number of groups to show (0 for all)
        separator: Separator between groups

    Returns:
        Formatted string with groups

    Examples:
        >>> format_grouped("abc123def456", group_size=4, separator="-")
        'abc1-23de-f456'
        >>> format_grouped("abc123def456", group_size=4, groups=2)
        'abc1 23de'
        >>> format_grouped("1234567890abcdef", group_size=4)
        '1234 5678 90ab cdef'

    """
    if group_size <= 0:
        return text

    formatted_parts = []
    for i in range(0, len(text), group_size):
        formatted_parts.append(text[i : i + group_size])
        if groups > 0 and len(formatted_parts) >= groups:
            break

    return separator.join(None)


x_format_grouped__mutmut_mutants: ClassVar[MutantDict] = {
    "x_format_grouped__mutmut_1": x_format_grouped__mutmut_1,
    "x_format_grouped__mutmut_2": x_format_grouped__mutmut_2,
    "x_format_grouped__mutmut_3": x_format_grouped__mutmut_3,
    "x_format_grouped__mutmut_4": x_format_grouped__mutmut_4,
    "x_format_grouped__mutmut_5": x_format_grouped__mutmut_5,
    "x_format_grouped__mutmut_6": x_format_grouped__mutmut_6,
    "x_format_grouped__mutmut_7": x_format_grouped__mutmut_7,
    "x_format_grouped__mutmut_8": x_format_grouped__mutmut_8,
    "x_format_grouped__mutmut_9": x_format_grouped__mutmut_9,
    "x_format_grouped__mutmut_10": x_format_grouped__mutmut_10,
    "x_format_grouped__mutmut_11": x_format_grouped__mutmut_11,
    "x_format_grouped__mutmut_12": x_format_grouped__mutmut_12,
    "x_format_grouped__mutmut_13": x_format_grouped__mutmut_13,
    "x_format_grouped__mutmut_14": x_format_grouped__mutmut_14,
    "x_format_grouped__mutmut_15": x_format_grouped__mutmut_15,
    "x_format_grouped__mutmut_16": x_format_grouped__mutmut_16,
    "x_format_grouped__mutmut_17": x_format_grouped__mutmut_17,
    "x_format_grouped__mutmut_18": x_format_grouped__mutmut_18,
    "x_format_grouped__mutmut_19": x_format_grouped__mutmut_19,
    "x_format_grouped__mutmut_20": x_format_grouped__mutmut_20,
    "x_format_grouped__mutmut_21": x_format_grouped__mutmut_21,
}


def format_grouped(*args, **kwargs):
    result = _mutmut_trampoline(x_format_grouped__mutmut_orig, x_format_grouped__mutmut_mutants, args, kwargs)
    return result


format_grouped.__signature__ = _mutmut_signature(x_format_grouped__mutmut_orig)
x_format_grouped__mutmut_orig.__name__ = "x_format_grouped"


__all__ = [
    "format_grouped",
]


# <3 🧱🤝🎨🪄
