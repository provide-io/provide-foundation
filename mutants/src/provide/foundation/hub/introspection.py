# provide/foundation/hub/introspection.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Framework-agnostic parameter introspection.

This module provides utilities to extract parameter information from
function signatures in a framework-agnostic way, supporting modern
Python type hints including typing.Annotated for CLI rendering hints.
"""

from __future__ import annotations

from collections.abc import Callable
import inspect
from typing import Annotated, Any, get_args, get_origin

from attrs import define, field

from provide.foundation.cli.errors import InvalidCLIHintError
from provide.foundation.parsers import extract_concrete_type

__all__ = ["ParameterInfo", "extract_cli_hint", "introspect_parameters"]
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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


def x_extract_cli_hint__mutmut_orig(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_1(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith(None):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_2(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("XXAnnotated[XX"):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_3(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_4(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("ANNOTATED["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_5(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = None
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_6(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(None, annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_7(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", None)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_8(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_9(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", )
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_10(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"XX['\"](\w+)['\"]XX", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_11(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_12(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_13(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = None
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_14(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(None)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_15(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(2)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_16(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint not in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_17(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("XXargumentXX", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_18(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("ARGUMENT", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_19(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "XXoptionXX"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_20(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "OPTION"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_21(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(None, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_22(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, None)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_23(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_24(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, )

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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


def x_extract_cli_hint__mutmut_25(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(None) is Annotated:
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


def x_extract_cli_hint__mutmut_26(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is not Annotated:
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


def x_extract_cli_hint__mutmut_27(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = None
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


def x_extract_cli_hint__mutmut_28(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(None)
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


def x_extract_cli_hint__mutmut_29(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = None
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


def x_extract_cli_hint__mutmut_30(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[1]
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


def x_extract_cli_hint__mutmut_31(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = None

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


def x_extract_cli_hint__mutmut_32(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[2:] if len(args) > 1 else ()

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


def x_extract_cli_hint__mutmut_33(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) >= 1 else ()

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


def x_extract_cli_hint__mutmut_34(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 2 else ()

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


def x_extract_cli_hint__mutmut_35(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item not in ("argument", "option"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_36(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item in ("XXargumentXX", "option"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_37(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item in ("ARGUMENT", "option"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_38(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item in ("argument", "XXoptionXX"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_39(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
    if get_origin(annotation) is Annotated:
        args = get_args(annotation)
        base_type = args[0]
        metadata = args[1:] if len(args) > 1 else ()

        # Look for CLI hint in metadata
        for item in metadata:
            if isinstance(item, str):
                if item in ("argument", "OPTION"):
                    return base_type, item
                else:
                    # Invalid hint - raise Foundation error with clear message
                    raise InvalidCLIHintError(item, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_40(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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
                    raise InvalidCLIHintError(None, param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_41(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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
                    raise InvalidCLIHintError(item, None)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_42(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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
                    raise InvalidCLIHintError(param_name)

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None


def x_extract_cli_hint__mutmut_43(annotation: Any, param_name: str) -> tuple[Any, str | None]:
    """Extract CLI rendering hint from Annotated type.

    Supports typing.Annotated with string metadata to explicitly control
    whether a parameter becomes a CLI argument or option.

    Handles both runtime Annotated types and string annotations from
    `from __future__ import annotations`.

    Args:
        annotation: Type annotation (may be Annotated[type, 'hint'] or string)
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
    # Handle string annotations from __future__ import annotations
    if isinstance(annotation, str):
        # Check if it's an Annotated string pattern
        if annotation.startswith("Annotated["):
            # Extract hint from string: "Annotated[str, 'option']" -> 'option'
            # Simple regex pattern for CLI hints
            import re

            hint_match = re.search(r"['\"](\w+)['\"]", annotation)
            if hint_match:
                hint = hint_match.group(1)
                if hint in ("argument", "option"):
                    # Return the full annotation string as base_type for now
                    # extract_concrete_type will handle it
                    return annotation, hint
                else:
                    # Invalid hint
                    raise InvalidCLIHintError(hint, param_name)

        # Not Annotated or no hint found
        return annotation, None

    # Check if this is a runtime Annotated type
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
                    raise InvalidCLIHintError(item, )

        # No CLI hint found in metadata
        return base_type, None

    # Not an Annotated type
    return annotation, None

x_extract_cli_hint__mutmut_mutants : ClassVar[MutantDict] = {
'x_extract_cli_hint__mutmut_1': x_extract_cli_hint__mutmut_1, 
    'x_extract_cli_hint__mutmut_2': x_extract_cli_hint__mutmut_2, 
    'x_extract_cli_hint__mutmut_3': x_extract_cli_hint__mutmut_3, 
    'x_extract_cli_hint__mutmut_4': x_extract_cli_hint__mutmut_4, 
    'x_extract_cli_hint__mutmut_5': x_extract_cli_hint__mutmut_5, 
    'x_extract_cli_hint__mutmut_6': x_extract_cli_hint__mutmut_6, 
    'x_extract_cli_hint__mutmut_7': x_extract_cli_hint__mutmut_7, 
    'x_extract_cli_hint__mutmut_8': x_extract_cli_hint__mutmut_8, 
    'x_extract_cli_hint__mutmut_9': x_extract_cli_hint__mutmut_9, 
    'x_extract_cli_hint__mutmut_10': x_extract_cli_hint__mutmut_10, 
    'x_extract_cli_hint__mutmut_11': x_extract_cli_hint__mutmut_11, 
    'x_extract_cli_hint__mutmut_12': x_extract_cli_hint__mutmut_12, 
    'x_extract_cli_hint__mutmut_13': x_extract_cli_hint__mutmut_13, 
    'x_extract_cli_hint__mutmut_14': x_extract_cli_hint__mutmut_14, 
    'x_extract_cli_hint__mutmut_15': x_extract_cli_hint__mutmut_15, 
    'x_extract_cli_hint__mutmut_16': x_extract_cli_hint__mutmut_16, 
    'x_extract_cli_hint__mutmut_17': x_extract_cli_hint__mutmut_17, 
    'x_extract_cli_hint__mutmut_18': x_extract_cli_hint__mutmut_18, 
    'x_extract_cli_hint__mutmut_19': x_extract_cli_hint__mutmut_19, 
    'x_extract_cli_hint__mutmut_20': x_extract_cli_hint__mutmut_20, 
    'x_extract_cli_hint__mutmut_21': x_extract_cli_hint__mutmut_21, 
    'x_extract_cli_hint__mutmut_22': x_extract_cli_hint__mutmut_22, 
    'x_extract_cli_hint__mutmut_23': x_extract_cli_hint__mutmut_23, 
    'x_extract_cli_hint__mutmut_24': x_extract_cli_hint__mutmut_24, 
    'x_extract_cli_hint__mutmut_25': x_extract_cli_hint__mutmut_25, 
    'x_extract_cli_hint__mutmut_26': x_extract_cli_hint__mutmut_26, 
    'x_extract_cli_hint__mutmut_27': x_extract_cli_hint__mutmut_27, 
    'x_extract_cli_hint__mutmut_28': x_extract_cli_hint__mutmut_28, 
    'x_extract_cli_hint__mutmut_29': x_extract_cli_hint__mutmut_29, 
    'x_extract_cli_hint__mutmut_30': x_extract_cli_hint__mutmut_30, 
    'x_extract_cli_hint__mutmut_31': x_extract_cli_hint__mutmut_31, 
    'x_extract_cli_hint__mutmut_32': x_extract_cli_hint__mutmut_32, 
    'x_extract_cli_hint__mutmut_33': x_extract_cli_hint__mutmut_33, 
    'x_extract_cli_hint__mutmut_34': x_extract_cli_hint__mutmut_34, 
    'x_extract_cli_hint__mutmut_35': x_extract_cli_hint__mutmut_35, 
    'x_extract_cli_hint__mutmut_36': x_extract_cli_hint__mutmut_36, 
    'x_extract_cli_hint__mutmut_37': x_extract_cli_hint__mutmut_37, 
    'x_extract_cli_hint__mutmut_38': x_extract_cli_hint__mutmut_38, 
    'x_extract_cli_hint__mutmut_39': x_extract_cli_hint__mutmut_39, 
    'x_extract_cli_hint__mutmut_40': x_extract_cli_hint__mutmut_40, 
    'x_extract_cli_hint__mutmut_41': x_extract_cli_hint__mutmut_41, 
    'x_extract_cli_hint__mutmut_42': x_extract_cli_hint__mutmut_42, 
    'x_extract_cli_hint__mutmut_43': x_extract_cli_hint__mutmut_43
}

def extract_cli_hint(*args, **kwargs):
    result = _mutmut_trampoline(x_extract_cli_hint__mutmut_orig, x_extract_cli_hint__mutmut_mutants, args, kwargs)
    return result 

extract_cli_hint.__signature__ = _mutmut_signature(x_extract_cli_hint__mutmut_orig)
x_extract_cli_hint__mutmut_orig.__name__ = 'x_extract_cli_hint'


def x_introspect_parameters__mutmut_orig(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_1(func: Callable[..., Any]) -> list[ParameterInfo]:
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
    sig = None
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_2(func: Callable[..., Any]) -> list[ParameterInfo]:
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
    sig = inspect.signature(None)
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_3(func: Callable[..., Any]) -> list[ParameterInfo]:
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
    result = None

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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_4(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name not in ("self", "cls", "ctx"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_5(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("XXselfXX", "cls", "ctx"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_6(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("SELF", "cls", "ctx"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_7(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("self", "XXclsXX", "ctx"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_8(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("self", "CLS", "ctx"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_9(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("self", "cls", "XXctxXX"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_10(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if param_name in ("self", "cls", "CTX"):
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_11(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            break

        # Get annotation and extract CLI hint
        annotation = param.annotation
        if annotation == inspect.Parameter.empty:
            # No annotation - use str as default
            base_type = str
            cli_hint = None
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_12(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        annotation = None
        if annotation == inspect.Parameter.empty:
            # No annotation - use str as default
            base_type = str
            cli_hint = None
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_13(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        if annotation != inspect.Parameter.empty:
            # No annotation - use str as default
            base_type = str
            cli_hint = None
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_14(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type = None
            cli_hint = None
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_15(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            cli_hint = ""
        else:
            base_type, cli_hint = extract_cli_hint(annotation, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_16(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type, cli_hint = None

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_17(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type, cli_hint = extract_cli_hint(None, param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_18(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type, cli_hint = extract_cli_hint(annotation, None)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_19(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type, cli_hint = extract_cli_hint(param_name)

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_20(func: Callable[..., Any]) -> list[ParameterInfo]:
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
            base_type, cli_hint = extract_cli_hint(annotation, )

        # Extract concrete type for framework use
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_21(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = None

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


def x_introspect_parameters__mutmut_22(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type != inspect.Parameter.empty else extract_concrete_type(base_type)

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


def x_introspect_parameters__mutmut_23(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(None)

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


def x_introspect_parameters__mutmut_24(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = None
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


def x_introspect_parameters__mutmut_25(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default == inspect.Parameter.empty
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


def x_introspect_parameters__mutmut_26(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = None

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


def x_introspect_parameters__mutmut_27(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = None

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_28(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=None,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_29(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=None,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_30(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=None,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_31(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=None,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_32(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=None,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_33(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=None,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_34(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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
            cli_hint=None,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_35(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_36(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_37(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            default=default_value,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_38(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            has_default=has_default,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_39(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            is_required=not has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_40(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_41(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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
            )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_42(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

        # Determine default and required status
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default

        param_info = ParameterInfo(
            name=param_name,
            type_annotation=annotation,
            concrete_type=concrete,
            default=default_value,
            has_default=has_default,
            is_required=has_default,
            cli_hint=cli_hint,
        )

        result.append(param_info)

    return result


def x_introspect_parameters__mutmut_43(func: Callable[..., Any]) -> list[ParameterInfo]:
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
        concrete = str if base_type == inspect.Parameter.empty else extract_concrete_type(base_type)

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

        result.append(None)

    return result

x_introspect_parameters__mutmut_mutants : ClassVar[MutantDict] = {
'x_introspect_parameters__mutmut_1': x_introspect_parameters__mutmut_1, 
    'x_introspect_parameters__mutmut_2': x_introspect_parameters__mutmut_2, 
    'x_introspect_parameters__mutmut_3': x_introspect_parameters__mutmut_3, 
    'x_introspect_parameters__mutmut_4': x_introspect_parameters__mutmut_4, 
    'x_introspect_parameters__mutmut_5': x_introspect_parameters__mutmut_5, 
    'x_introspect_parameters__mutmut_6': x_introspect_parameters__mutmut_6, 
    'x_introspect_parameters__mutmut_7': x_introspect_parameters__mutmut_7, 
    'x_introspect_parameters__mutmut_8': x_introspect_parameters__mutmut_8, 
    'x_introspect_parameters__mutmut_9': x_introspect_parameters__mutmut_9, 
    'x_introspect_parameters__mutmut_10': x_introspect_parameters__mutmut_10, 
    'x_introspect_parameters__mutmut_11': x_introspect_parameters__mutmut_11, 
    'x_introspect_parameters__mutmut_12': x_introspect_parameters__mutmut_12, 
    'x_introspect_parameters__mutmut_13': x_introspect_parameters__mutmut_13, 
    'x_introspect_parameters__mutmut_14': x_introspect_parameters__mutmut_14, 
    'x_introspect_parameters__mutmut_15': x_introspect_parameters__mutmut_15, 
    'x_introspect_parameters__mutmut_16': x_introspect_parameters__mutmut_16, 
    'x_introspect_parameters__mutmut_17': x_introspect_parameters__mutmut_17, 
    'x_introspect_parameters__mutmut_18': x_introspect_parameters__mutmut_18, 
    'x_introspect_parameters__mutmut_19': x_introspect_parameters__mutmut_19, 
    'x_introspect_parameters__mutmut_20': x_introspect_parameters__mutmut_20, 
    'x_introspect_parameters__mutmut_21': x_introspect_parameters__mutmut_21, 
    'x_introspect_parameters__mutmut_22': x_introspect_parameters__mutmut_22, 
    'x_introspect_parameters__mutmut_23': x_introspect_parameters__mutmut_23, 
    'x_introspect_parameters__mutmut_24': x_introspect_parameters__mutmut_24, 
    'x_introspect_parameters__mutmut_25': x_introspect_parameters__mutmut_25, 
    'x_introspect_parameters__mutmut_26': x_introspect_parameters__mutmut_26, 
    'x_introspect_parameters__mutmut_27': x_introspect_parameters__mutmut_27, 
    'x_introspect_parameters__mutmut_28': x_introspect_parameters__mutmut_28, 
    'x_introspect_parameters__mutmut_29': x_introspect_parameters__mutmut_29, 
    'x_introspect_parameters__mutmut_30': x_introspect_parameters__mutmut_30, 
    'x_introspect_parameters__mutmut_31': x_introspect_parameters__mutmut_31, 
    'x_introspect_parameters__mutmut_32': x_introspect_parameters__mutmut_32, 
    'x_introspect_parameters__mutmut_33': x_introspect_parameters__mutmut_33, 
    'x_introspect_parameters__mutmut_34': x_introspect_parameters__mutmut_34, 
    'x_introspect_parameters__mutmut_35': x_introspect_parameters__mutmut_35, 
    'x_introspect_parameters__mutmut_36': x_introspect_parameters__mutmut_36, 
    'x_introspect_parameters__mutmut_37': x_introspect_parameters__mutmut_37, 
    'x_introspect_parameters__mutmut_38': x_introspect_parameters__mutmut_38, 
    'x_introspect_parameters__mutmut_39': x_introspect_parameters__mutmut_39, 
    'x_introspect_parameters__mutmut_40': x_introspect_parameters__mutmut_40, 
    'x_introspect_parameters__mutmut_41': x_introspect_parameters__mutmut_41, 
    'x_introspect_parameters__mutmut_42': x_introspect_parameters__mutmut_42, 
    'x_introspect_parameters__mutmut_43': x_introspect_parameters__mutmut_43
}

def introspect_parameters(*args, **kwargs):
    result = _mutmut_trampoline(x_introspect_parameters__mutmut_orig, x_introspect_parameters__mutmut_mutants, args, kwargs)
    return result 

introspect_parameters.__signature__ = _mutmut_signature(x_introspect_parameters__mutmut_orig)
x_introspect_parameters__mutmut_orig.__name__ = 'x_introspect_parameters'


# <3 🧱🤝🌐🪄
