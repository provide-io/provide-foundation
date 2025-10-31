#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

import types
import typing
from typing import Any, get_args, get_origin

from provide.foundation.parsers.collections import parse_dict, parse_list, parse_set, parse_tuple
from provide.foundation.parsers.primitives import parse_bool

"""Type-aware parsing utilities for converting strings to typed values.

Provides utilities for converting string values to proper Python types based on
type hints, including support for generics and parameterized types.
"""


def _parse_basic_type(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def _parse_list_type(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def _parse_tuple_type(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def _parse_set_type(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def _parse_generic_type(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def extract_concrete_type(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def parse_typed_value(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

    Handles basic types (int, float, bool, str) and generic types (list, dict).
    For attrs fields, pass field.type as target_type.

    Args:
        value: String value to parse
        target_type: Target type to convert to

    Returns:
        Parsed value of the target type

    Examples:
        >>> parse_typed_value("42", int)
        42
        >>> parse_typed_value("true", bool)
        True
        >>> parse_typed_value("a,b,c", list)
        ['a', 'b', 'c']

    """
    if value is None:
        return None

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


__all__ = [
    "_parse_basic_type",
    "_parse_generic_type",
    "_parse_list_type",
    "_parse_set_type",
    "_parse_tuple_type",
    "extract_concrete_type",
    "parse_typed_value",
]

# 🧱🏗️🔚
