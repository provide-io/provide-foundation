"""
Type parsing and conversion utilities.

Provides utilities for converting string values (from environment variables,
config files, CLI args, etc.) to proper Python types based on type hints.
"""

from __future__ import annotations

from typing import Any, TypeVar, get_args, get_origin

T = TypeVar("T")


def parse_bool(value: Any, strict: bool = False) -> bool:
    """
    Parse a boolean value from string or other types.

    Accepts: true/false, yes/no, 1/0, on/off, enabled/disabled (case-insensitive)

    Args:
        value: Value to parse as boolean
        strict: If True, only accept bool or string types (raise TypeError otherwise)

    Returns:
        Boolean value

    Raises:
        TypeError: If strict=True and value is not bool or string
        ValueError: If value cannot be parsed as boolean
    """
    if isinstance(value, bool):
        return value

    if strict and not isinstance(value, str):
        raise TypeError(f"Cannot convert {type(value).__name__} to bool: {value!r}")

    str_value = str(value).lower().strip()

    if str_value in ("true", "yes", "1", "on", "enabled"):
        return True
    elif str_value in ("false", "no", "0", "off", "disabled", ""):
        return False
    else:
        raise ValueError(f"Cannot parse '{value}' as boolean")


def parse_list(
    value: str | list,
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """
    Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings
    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def parse_dict(
    value: str | dict,
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """
    Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid
    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def parse_typed_value(value: str, target_type: type) -> Any:
    """
    Parse a string value to a specific type.

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

    # Handle basic types
    if target_type == bool:
        return parse_bool(value)
    elif target_type == int:
        return int(value)
    elif target_type == float:
        return float(value)
    elif target_type == str:
        return value

    # Handle generic types using typing module
    origin = get_origin(target_type)

    if origin == list:
        # Handle list[T] - convert each item to the specified type
        args = get_args(target_type)
        if args and len(args) > 0:
            item_type = args[0]
            str_list = parse_list(value)
            try:
                # Convert each item to the target type
                return [parse_typed_value(item, item_type) for item in str_list]
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Cannot convert list items to {item_type.__name__}: {e}"
                )
        else:
            # list without type parameter, return as list[str]
            return parse_list(value)
    elif origin == dict:
        return parse_dict(value)
    elif origin is None:
        # Not a generic type, try direct conversion
        if target_type == list:
            return parse_list(value)
        elif target_type == dict:
            return parse_dict(value)

    # Default to string
    return value


def auto_parse(attr: Any, value: str) -> Any:
    """
    Automatically parse value based on an attrs field's type.

    This is a convenience wrapper for parse_typed_value that extracts
    the type from an attrs field.

    Args:
        attr: attrs field (from fields(Class))
        value: String value to parse

    Returns:
        Parsed value based on field type
    """
    # Get type hint from attrs field
    if hasattr(attr, "type") and attr.type is not None:
        field_type = attr.type

        # Handle string type annotations (e.g., 'int', 'str', 'bool')
        # This happens when attrs processes classes defined inside functions
        if isinstance(field_type, str):
            # Map common string type names to actual types
            type_map = {
                "int": int,
                "float": float,
                "str": str,
                "bool": bool,
                "list": list,
                "dict": dict,
            }
            # Try to get the actual type from the map
            field_type = type_map.get(field_type, field_type)

        # If we still have a string, we can't parse it
        if isinstance(field_type, str):
            return value

        return parse_typed_value(value, field_type)

    # No type info, return as string
    return value
