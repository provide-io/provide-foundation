#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

"""Case conversion utilities.

Provides utilities for converting between different text case formats
like snake_case, kebab-case, and camelCase.
"""


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


__all__ = [
    "to_camel_case",
    "to_kebab_case",
    "to_snake_case",
]

# 🧱🏗️🔚
