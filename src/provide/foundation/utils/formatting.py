"""String formatting and text utilities.

Provides utilities for human-readable formatting of sizes, durations,
and other common string operations.
"""

from typing import Any


def format_size(size_bytes: int | float, precision: int = 1) -> str:
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


def format_duration(seconds: int | float, short: bool = False) -> str:
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

    parts = []

    if short:
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        return "".join(parts)
    else:
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if secs > 0 or not parts:
            parts.append(f"{secs} second{'s' if secs != 1 else ''}")
        return " ".join(parts)


def format_number(num: int | float, precision: int | None = None) -> str:
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
        else:
            # Auto precision for floats
            return f"{num:,.6f}".rstrip("0").rstrip(".")
    else:
        return f"{num:,.{precision}f}"


def format_percentage(
    value: float, precision: int = 1, include_sign: bool = False
) -> str:
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


def truncate(
    text: str, max_length: int, suffix: str = "...", whole_words: bool = True
) -> str:
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


def wrap_text(
    text: str, width: int = 80, indent_first: int = 0, indent_rest: int = 0
) -> str:
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


def format_table(
    headers: list[str], rows: list[list[Any]], alignment: list[str] | None = None
) -> str:
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
    widths = [len(h) for h in str_headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))

    # Default alignment
    if alignment is None:
        alignment = ["l"] * len(headers)

    # Format header
    header_parts = []
    separator_parts = []

    for i, (header, width) in enumerate(zip(str_headers, widths, strict=False)):
        align = alignment[i] if i < len(alignment) else "l"

        if align == "r":
            header_parts.append(header.rjust(width))
        elif align == "c":
            header_parts.append(header.center(width))
        else:
            header_parts.append(header.ljust(width))

        separator_parts.append("-" * width)

    lines = [" | ".join(header_parts), "-|-".join(separator_parts)]

    # Format rows
    for row in str_rows:
        row_parts = []
        for i, cell in enumerate(row):
            if i < len(widths):
                width = widths[i]
                align = alignment[i] if i < len(alignment) else "l"

                if align == "r":
                    row_parts.append(cell.rjust(width))
                elif align == "c":
                    row_parts.append(cell.center(width))
                else:
                    row_parts.append(cell.ljust(width))

        lines.append(" | ".join(row_parts))

    return "\n".join(lines)


__all__ = [
    "format_duration",
    "format_number",
    "format_percentage",
    "format_size",
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
