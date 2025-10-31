#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

from provide.foundation.formatting.case import (
    to_camel_case,
    to_kebab_case,
    to_snake_case,
)
from provide.foundation.formatting.grouping import format_grouped
from provide.foundation.formatting.numbers import (
    format_duration,
    format_number,
    format_percentage,
    format_size,
)
from provide.foundation.formatting.tables import format_table
from provide.foundation.formatting.text import (
    indent,
    pluralize,
    strip_ansi,
    truncate,
    wrap_text,
)

"""Formatting utilities for provide.foundation.

Comprehensive text, numeric, and data formatting utilities for consistent
output across applications.
"""

__all__ = [
    # Numeric formatting
    "format_duration",
    # String grouping
    "format_grouped",
    "format_number",
    "format_percentage",
    "format_size",
    # Table formatting
    "format_table",
    # Text manipulation
    "indent",
    "pluralize",
    "strip_ansi",
    # Case conversion
    "to_camel_case",
    "to_kebab_case",
    "to_snake_case",
    "truncate",
    "wrap_text",
]

# 🧱🏗️🔚
