#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import re

"""Text manipulation and formatting utilities.

Provides utilities for text truncation, indentation, and other common
text operations.
"""

# Compiled regex patterns for performance
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


def truncate(text: str, max_length: int, suffix: str = "...", whole_words: bool = True) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to append when truncated
        whole_words: Truncate at word boundaries

    Returns:
        Truncated text

    Examples:
        >>> truncate("Hello world", 8)
        'Hello...'
        >>> truncate("Hello world", 8, whole_words=False)
        'Hello...'

    """
    if len(text) <= max_length:
        return text

    if max_length <= len(suffix):
        return suffix[:max_length]

    truncate_at = max_length - len(suffix)

    if whole_words:
        # Find last space before truncate point
        space_pos = text.rfind(" ", 0, truncate_at)
        if space_pos > 0:
            truncate_at = space_pos

    return text[:truncate_at] + suffix


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """Get singular or plural form based on count.

    Args:
        count: Item count
        singular: Singular form
        plural: Plural form (default: singular + 's')

    Returns:
        Appropriate singular/plural form with count

    Examples:
        >>> pluralize(1, "file")
        '1 file'
        >>> pluralize(5, "file")
        '5 files'
        >>> pluralize(2, "child", "children")
        '2 children'

    """
    if plural is None:
        plural = f"{singular}s"

    word = singular if count == 1 else plural
    return f"{count} {word}"


def indent(text: str, spaces: int = 2, first_line: bool = True) -> str:
    """Indent text lines.

    Args:
        text: Text to indent
        spaces: Number of spaces to indent
        first_line: Whether to indent the first line

    Returns:
        Indented text

    Examples:
        >>> indent("line1\\nline2", 4)
        '    line1\\n    line2'

    """
    indent_str = " " * spaces
    lines = text.splitlines()

    if not lines:
        return text

    result = []
    for i, line in enumerate(lines):
        if i == 0 and not first_line:
            result.append(line)
        else:
            result.append(indent_str + line if line else "")

    return "\n".join(result)


def wrap_text(text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0) -> str:
    """Wrap text to specified width.

    Args:
        text: Text to wrap
        width: Maximum line width
        indent_first: Spaces to indent first line
        indent_rest: Spaces to indent remaining lines

    Returns:
        Wrapped text

    """
    import textwrap

    wrapper = textwrap.TextWrapper(
        width=width,
        initial_indent=" " * indent_first,
        subsequent_indent=" " * indent_rest,
        break_long_words=False,
        break_on_hyphens=False,
    )

    return wrapper.fill(text)


def strip_ansi(text: str) -> str:
    """Strip ANSI color codes from text.

    Args:
        text: Text with potential ANSI codes

    Returns:
        Text without ANSI codes

    """
    return ANSI_PATTERN.sub("", text)


__all__ = [
    "indent",
    "pluralize",
    "strip_ansi",
    "truncate",
    "wrap_text",
]

# 🧱🏗️🔚
