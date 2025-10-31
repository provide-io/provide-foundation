#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from typing import Any

"""Table formatting utilities.

Provides utilities for formatting data as ASCII tables with proper
alignment and column width calculation.
"""


def _calculate_column_widths(headers: list[str], rows: list[list[str]]) -> list[int]:
    """Calculate optimal column widths for table formatting."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))
    return widths


def _align_cell(text: str, width: int, alignment: str) -> str:
    """Align cell text within the specified width."""
    if alignment == "r":
        return text.rjust(width)
    elif alignment == "c":
        return text.center(width)
    else:
        return text.ljust(width)


def _format_table_header(headers: list[str], widths: list[int], alignment: list[str]) -> tuple[str, str]:
    """Format table header and separator lines."""
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"
        header_parts.append(_align_cell(header, width, align))
        separator_parts.append("-" * width)

    return " | ".join(header_parts), "-|-".join(separator_parts)


def _format_table_row(row: list[str], widths: list[int], alignment: list[str]) -> str:
    """Format a single table row."""
    row_parts = []
    for i, cell in enumerate(row):
        if i < len(widths):
            align = alignment[i] if i < len(alignment) else "l"
            row_parts.append(_align_cell(cell, widths[i], align))
    return " | ".join(row_parts)


def format_table(headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None) -> str:
    """Format data as ASCII table.

    Args:
        headers: Column headers
        rows: Data rows
        alignment: Column alignments ('l', 'r', 'c')

    Returns:
        Formatted table string

    Examples:
        >>> headers = ['Name', 'Age']
        >>> rows = [['Alice', 30], ['Bob', 25]]
        >>> print(format_table(headers, rows))
        Name  | Age
        ------|----
        Alice | 30
        Bob   | 25

    """
    if not headers and not rows:
        return ""

    # Convert all cells to strings
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]

    # Calculate column widths
    widths = _calculate_column_widths(str_headers, str_rows)

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header and separator
    header_line, separator_line = _format_table_header(str_headers, widths, alignment)
    lines = [header_line, separator_line]

    # Format data rows
    for row in str_rows:
        lines.append(_format_table_row(row, widths, alignment))

    return "\n".join(lines)


__all__ = [
    "format_table",
]

# 🧱🏗️🔚
