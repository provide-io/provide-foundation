"""Type system and Click type mapping utilities."""

from __future__ import annotations

import types
import typing
from typing import Any, get_args, get_origin


def extract_click_type(annotation: Any) -> type:
    """Extract a Click-compatible type from a Python type annotation.

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
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        # Parse common string type patterns
        annotation = annotation.strip()

        # Handle Union types as strings
        if " | " in annotation:
            # Split on " | " and get the first non-None type
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            annotation = non_none_parts[0] if non_none_parts else "str"

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "Path": str,  # Path objects are handled as strings by Click
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str

    # Get the origin and args for generic types
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
            # Could be enhanced to handle Union[str, int] etc.
            return non_none_types[0]
        # If only None, default to str
        return str

    # For non-generic types, return as-is
    return annotation


__all__ = ["extract_click_type"]
