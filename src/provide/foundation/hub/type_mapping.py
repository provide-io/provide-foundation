#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Type system and Click type mapping utilities."""

from __future__ import annotations

from typing import Any

from provide.foundation.parsers import extract_concrete_type


def extract_click_type(annotation: Any) -> type:
    """Extract a Click-compatible type from a Python type annotation.

    This is a wrapper around extract_concrete_type() that ensures
    compatibility with Click's type system.

    Handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)

    Args:
        annotation: Type annotation from function signature

    Returns:
        A type that Click can understand

    """
    return extract_concrete_type(annotation)


__all__ = ["extract_click_type"]

# 🧱🏗️🔚
