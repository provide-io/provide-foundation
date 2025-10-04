"""Framework-agnostic parameter introspection.

This module provides utilities to extract parameter information from
function signatures in a framework-agnostic way, supporting modern
Python type hints including typing.Annotated for CLI rendering hints.
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Annotated, Any, get_args, get_origin

from attrs import define, field

from provide.foundation.cli.errors import InvalidCLIHintError
from provide.foundation.utils.parsing import extract_concrete_type

__all__ = ["ParameterInfo", "extract_cli_hint", "introspect_parameters"]


@define(frozen=True, slots=True)
class ParameterInfo:
    """Framework-agnostic parameter information.

    Attributes:
        name: Parameter name
        type_annotation: Original type annotation (may be Annotated)
        concrete_type: Extracted concrete type (for Click/other frameworks)
        default: Default value (inspect.Parameter.empty if required)
        has_default: Whether parameter has a default value
        is_required: Whether parameter is required (inverse of has_default)
        cli_hint: Explicit CLI rendering hint ('argument', 'option', or None)

    """

    name: str
    type_annotation: Any
    concrete_type: type
    default: Any
    has_default: bool
    is_required: bool
    cli_hint: str | None = field(default=None)


def extract_cli_hint(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'])
        param_name: Parameter name (for error messages)

    Returns:
        (base_type, hint) where hint is 'argument', 'option', or None

    Raises:
        InvalidCLIHintError: If hint is not 'argument' or 'option'

    Examples:
        >>> extract_cli_hint(Annotated[str, 'option'], 'user')
        (str, 'option')

        >>> extract_cli_hint(Annotated[str, 'argument'], 'name')
        (str, 'argument')

        >>> extract_cli_hint(str, 'user')
        (str, None)

        >>> extract_cli_hint(str | None, 'user')
        (str | None, None)

        >>> # Raises InvalidCLIHintError
        >>> extract_cli_hint(Annotated[str, 'invalid'], 'user')

    """
    # Check if this is an Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item in ("argument", "option"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def introspect_parameters(func: Callable[..., Any]) -> list[ParameterInfo]:
    """Extract parameter information from function signature.

    Introspects a function's parameters and returns framework-agnostic
    metadata that can be used by different CLI adapters.

    Args:
        func: Function to introspect

    Returns:
        List of ParameterInfo objects (excludes 'self', 'cls', 'ctx')

    Examples:
        >>> def greet(name: str, greeting: str = "Hello"):
        ...     pass
        >>> params = introspect_parameters(greet)
        >>> len(params)
        2
        >>> params[0].name
        'name'
        >>> params[0].is_required
        True
        >>> params[1].has_default
        True

    """
    sig = inspect.signature(func)
    result = []

    for param_name, param in sig.parameters.items():
        # Skip special parameters
        if param_name in ("self", "cls", "ctx"):
            continue

        # Get annotation and extract CLI hint
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            # No annotation - use str as default
            base_type = str
            cli_hint = None
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        if base_type == inspect.Parameter.empty:
            concrete = str
        else:
            concrete = extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result
