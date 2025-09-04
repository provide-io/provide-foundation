"""Type system and Click type mapping utilities."""

import types
import typing
from typing import Any, get_args, get_origin


def extract_click_type(annotation: Any) -> type:
    """
    Extract a Click-compatible type from a Python type annotation.

    Handles:
    - Union types (str | None, Union[str, None])
    - Optional types (Optional[str])
    - Regular types (str, int, bool)

    Args:
        annotation: Type annotation from function signature

    Returns:
        A type that Click can understand
    """
    # Handle None type
    if annotation is type(None):
        return str

    # Get the origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (
        hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)
    ):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            # Could be enhanced to handle Union[str, int] etc.
            return non_none_types[0]
        else:
            # If only None, default to str
            return str

    # For non-generic types, return as-is
    return annotation


__all__ = ["extract_click_type"]
