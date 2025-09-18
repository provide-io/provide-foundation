from __future__ import annotations

from typing import Any

"""Text manipulation and formatting utilities.

Provides utilities for text truncation, case conversion, table formatting,
and other common text operations.
"""


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
    import re

    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_pattern.sub("", text)


def to_snake_case(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def to_camel_case(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


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
    "indent",
    "pluralize",
    "strip_ansi",
    "to_camel_case",
    "to_kebab_case",
    "to_snake_case",
    "truncate",
    "wrap_text",
]
