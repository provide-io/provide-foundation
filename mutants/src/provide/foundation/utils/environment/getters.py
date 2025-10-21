# provide/foundation/utils/environment/getters.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, TypeVar, get_origin

from provide.foundation.errors.config import ValidationError
from provide.foundation.logger import get_logger
from provide.foundation.parsers import parse_bool, parse_dict, parse_list, parse_set, parse_tuple

"""Basic environment variable getters with type coercion.

Provides safe functions for reading and parsing environment variables
with automatic type detection and validation.
"""

T = TypeVar("T")
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


def x__get_logger__mutmut_orig() -> Any:
    """Get logger instance lazily to avoid circular imports."""

    return get_logger(__name__)


def x__get_logger__mutmut_1() -> Any:
    """Get logger instance lazily to avoid circular imports."""

    return get_logger(None)

x__get_logger__mutmut_mutants : ClassVar[MutantDict] = {
'x__get_logger__mutmut_1': x__get_logger__mutmut_1
}

def _get_logger(*args, **kwargs):
    result = _mutmut_trampoline(x__get_logger__mutmut_orig, x__get_logger__mutmut_mutants, args, kwargs)
    return result 

_get_logger.__signature__ = _mutmut_signature(x__get_logger__mutmut_orig)
x__get_logger__mutmut_orig.__name__ = 'x__get_logger'


def x_get_bool__mutmut_orig(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_1(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = None
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_2(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(None)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_3(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is not None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_4(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_5(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = None
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_6(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(None)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_7(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            None
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_8(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(None)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_9(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            None,
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_10(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=None,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_11(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=None,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_12(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule=None,
        ) from e


def x_get_bool__mutmut_13(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            field=name,
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_14(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            value=value,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_15(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            rule="boolean",
        ) from e


def x_get_bool__mutmut_16(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            ) from e


def x_get_bool__mutmut_17(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="XXbooleanXX",
        ) from e


def x_get_bool__mutmut_18(name: str, default: bool | None = None) -> bool | None:
    """Get boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Boolean value, None (if set but empty), or default (if unset)

    Note:
        Empty string is treated as ambiguous and returns None with a warning.
        Unset variable returns the default value.

    Examples:
        >>> os.environ['DEBUG'] = 'true'
        >>> get_bool('DEBUG')
        True
        >>> get_bool('MISSING', False)
        False

    """
    from provide.foundation.logger import get_logger

    value = os.environ.get(name)
    if value is None:
        return default

    # Handle empty/whitespace-only strings as ambiguous
    if not value.strip():
        logger = get_logger(__name__)
        logger.warning(
            f"Environment variable {name} is set but empty - treating as None. "
            f"Either provide a value or unset the variable to use default."
        )
        return None

    try:
        return parse_bool(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid boolean value for {name}: {value}",
            field=name,
            value=value,
            rule="BOOLEAN",
        ) from e

x_get_bool__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_bool__mutmut_1': x_get_bool__mutmut_1, 
    'x_get_bool__mutmut_2': x_get_bool__mutmut_2, 
    'x_get_bool__mutmut_3': x_get_bool__mutmut_3, 
    'x_get_bool__mutmut_4': x_get_bool__mutmut_4, 
    'x_get_bool__mutmut_5': x_get_bool__mutmut_5, 
    'x_get_bool__mutmut_6': x_get_bool__mutmut_6, 
    'x_get_bool__mutmut_7': x_get_bool__mutmut_7, 
    'x_get_bool__mutmut_8': x_get_bool__mutmut_8, 
    'x_get_bool__mutmut_9': x_get_bool__mutmut_9, 
    'x_get_bool__mutmut_10': x_get_bool__mutmut_10, 
    'x_get_bool__mutmut_11': x_get_bool__mutmut_11, 
    'x_get_bool__mutmut_12': x_get_bool__mutmut_12, 
    'x_get_bool__mutmut_13': x_get_bool__mutmut_13, 
    'x_get_bool__mutmut_14': x_get_bool__mutmut_14, 
    'x_get_bool__mutmut_15': x_get_bool__mutmut_15, 
    'x_get_bool__mutmut_16': x_get_bool__mutmut_16, 
    'x_get_bool__mutmut_17': x_get_bool__mutmut_17, 
    'x_get_bool__mutmut_18': x_get_bool__mutmut_18
}

def get_bool(*args, **kwargs):
    result = _mutmut_trampoline(x_get_bool__mutmut_orig, x_get_bool__mutmut_mutants, args, kwargs)
    return result 

get_bool.__signature__ = _mutmut_signature(x_get_bool__mutmut_orig)
x_get_bool__mutmut_orig.__name__ = 'x_get_bool'


def x_get_int__mutmut_orig(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_1(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = None
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_2(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(None)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_3(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is not None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_4(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(None)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_5(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            None,
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_6(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=None,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_7(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=None,
            rule="integer",
        ) from e


def x_get_int__mutmut_8(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule=None,
        ) from e


def x_get_int__mutmut_9(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            field=name,
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_10(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            value=value,
            rule="integer",
        ) from e


def x_get_int__mutmut_11(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            rule="integer",
        ) from e


def x_get_int__mutmut_12(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            ) from e


def x_get_int__mutmut_13(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="XXintegerXX",
        ) from e


def x_get_int__mutmut_14(name: str, default: int | None = None) -> int | None:
    """Get integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Integer value or default

    Raises:
        ValidationError: If value cannot be parsed as integer

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid integer value for {name}: {value}",
            field=name,
            value=value,
            rule="INTEGER",
        ) from e

x_get_int__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_int__mutmut_1': x_get_int__mutmut_1, 
    'x_get_int__mutmut_2': x_get_int__mutmut_2, 
    'x_get_int__mutmut_3': x_get_int__mutmut_3, 
    'x_get_int__mutmut_4': x_get_int__mutmut_4, 
    'x_get_int__mutmut_5': x_get_int__mutmut_5, 
    'x_get_int__mutmut_6': x_get_int__mutmut_6, 
    'x_get_int__mutmut_7': x_get_int__mutmut_7, 
    'x_get_int__mutmut_8': x_get_int__mutmut_8, 
    'x_get_int__mutmut_9': x_get_int__mutmut_9, 
    'x_get_int__mutmut_10': x_get_int__mutmut_10, 
    'x_get_int__mutmut_11': x_get_int__mutmut_11, 
    'x_get_int__mutmut_12': x_get_int__mutmut_12, 
    'x_get_int__mutmut_13': x_get_int__mutmut_13, 
    'x_get_int__mutmut_14': x_get_int__mutmut_14
}

def get_int(*args, **kwargs):
    result = _mutmut_trampoline(x_get_int__mutmut_orig, x_get_int__mutmut_mutants, args, kwargs)
    return result 

get_int.__signature__ = _mutmut_signature(x_get_int__mutmut_orig)
x_get_int__mutmut_orig.__name__ = 'x_get_int'


def x_get_float__mutmut_orig(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_1(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = None
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_2(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(None)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_3(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is not None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_4(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(None)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_5(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            None,
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_6(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=None,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_7(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=None,
            rule="float",
        ) from e


def x_get_float__mutmut_8(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule=None,
        ) from e


def x_get_float__mutmut_9(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            field=name,
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_10(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            value=value,
            rule="float",
        ) from e


def x_get_float__mutmut_11(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            rule="float",
        ) from e


def x_get_float__mutmut_12(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            ) from e


def x_get_float__mutmut_13(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="XXfloatXX",
        ) from e


def x_get_float__mutmut_14(name: str, default: float | None = None) -> float | None:
    """Get float environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        Float value or default

    Raises:
        ValidationError: If value cannot be parsed as float

    """
    value = os.environ.get(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError as e:
        raise ValidationError(
            f"Invalid float value for {name}: {value}",
            field=name,
            value=value,
            rule="FLOAT",
        ) from e

x_get_float__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_float__mutmut_1': x_get_float__mutmut_1, 
    'x_get_float__mutmut_2': x_get_float__mutmut_2, 
    'x_get_float__mutmut_3': x_get_float__mutmut_3, 
    'x_get_float__mutmut_4': x_get_float__mutmut_4, 
    'x_get_float__mutmut_5': x_get_float__mutmut_5, 
    'x_get_float__mutmut_6': x_get_float__mutmut_6, 
    'x_get_float__mutmut_7': x_get_float__mutmut_7, 
    'x_get_float__mutmut_8': x_get_float__mutmut_8, 
    'x_get_float__mutmut_9': x_get_float__mutmut_9, 
    'x_get_float__mutmut_10': x_get_float__mutmut_10, 
    'x_get_float__mutmut_11': x_get_float__mutmut_11, 
    'x_get_float__mutmut_12': x_get_float__mutmut_12, 
    'x_get_float__mutmut_13': x_get_float__mutmut_13, 
    'x_get_float__mutmut_14': x_get_float__mutmut_14
}

def get_float(*args, **kwargs):
    result = _mutmut_trampoline(x_get_float__mutmut_orig, x_get_float__mutmut_mutants, args, kwargs)
    return result 

get_float.__signature__ = _mutmut_signature(x_get_float__mutmut_orig)
x_get_float__mutmut_orig.__name__ = 'x_get_float'


def x_get_str__mutmut_orig(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(name, default)


def x_get_str__mutmut_1(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(None, default)


def x_get_str__mutmut_2(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(name, None)


def x_get_str__mutmut_3(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(default)


def x_get_str__mutmut_4(name: str, default: str | None = None) -> str | None:
    """Get string environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        String value or default

    """
    return os.environ.get(name, )

x_get_str__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_str__mutmut_1': x_get_str__mutmut_1, 
    'x_get_str__mutmut_2': x_get_str__mutmut_2, 
    'x_get_str__mutmut_3': x_get_str__mutmut_3, 
    'x_get_str__mutmut_4': x_get_str__mutmut_4
}

def get_str(*args, **kwargs):
    result = _mutmut_trampoline(x_get_str__mutmut_orig, x_get_str__mutmut_mutants, args, kwargs)
    return result 

get_str.__signature__ = _mutmut_signature(x_get_str__mutmut_orig)
x_get_str__mutmut_orig.__name__ = 'x_get_str'


def x_get_path__mutmut_orig(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_1(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = None
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_2(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(None)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_3(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is not None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_4(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is not None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_5(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(None) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_6(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(expanded).expanduser()


def x_get_path__mutmut_7(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = None
    return Path(expanded).expanduser()


def x_get_path__mutmut_8(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(None)
    return Path(expanded).expanduser()


def x_get_path__mutmut_9(name: str, default: Path | str | None = None) -> Path | None:
    """Get path environment variable.

    Args:
        name: Environment variable name
        default: Default path if not set

    Returns:
        Path object or None

    """
    value = os.environ.get(name)
    if value is None:
        if default is None:
            return None
        return Path(default) if not isinstance(default, Path) else default

    # Expand user and environment variables
    expanded = os.path.expandvars(value)
    return Path(None).expanduser()

x_get_path__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_path__mutmut_1': x_get_path__mutmut_1, 
    'x_get_path__mutmut_2': x_get_path__mutmut_2, 
    'x_get_path__mutmut_3': x_get_path__mutmut_3, 
    'x_get_path__mutmut_4': x_get_path__mutmut_4, 
    'x_get_path__mutmut_5': x_get_path__mutmut_5, 
    'x_get_path__mutmut_6': x_get_path__mutmut_6, 
    'x_get_path__mutmut_7': x_get_path__mutmut_7, 
    'x_get_path__mutmut_8': x_get_path__mutmut_8, 
    'x_get_path__mutmut_9': x_get_path__mutmut_9
}

def get_path(*args, **kwargs):
    result = _mutmut_trampoline(x_get_path__mutmut_orig, x_get_path__mutmut_mutants, args, kwargs)
    return result 

get_path.__signature__ = _mutmut_signature(x_get_path__mutmut_orig)
x_get_path__mutmut_orig.__name__ = 'x_get_path'


def x_get_list__mutmut_orig(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_1(name: str, default: list[str] | None = None, separator: str = "XX,XX") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_2(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = None
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_3(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(None)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_4(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is not None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_5(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default and []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_6(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = None
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_7(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(None, separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_8(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=None, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_9(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=None)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_10(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(separator=separator, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_11(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, strip=True)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_12(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, )
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]


def x_get_list__mutmut_13(name: str, default: list[str] | None = None, separator: str = ",") -> list[str]:
    """Get list from environment variable.

    Args:
        name: Environment variable name
        default: Default list if not set
        separator: String separator (default: comma)

    Returns:
        List of strings

    Examples:
        >>> os.environ['ITEMS'] = 'a,b,c'
        >>> get_list('ITEMS')
        ['a', 'b', 'c']

    """
    value = os.environ.get(name)
    if value is None:
        return default or []

    # Use existing parse_list which handles empty strings and stripping
    items = parse_list(value, separator=separator, strip=False)
    # Filter empty strings (parse_list doesn't do this by default)
    return [item for item in items if item]

x_get_list__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_list__mutmut_1': x_get_list__mutmut_1, 
    'x_get_list__mutmut_2': x_get_list__mutmut_2, 
    'x_get_list__mutmut_3': x_get_list__mutmut_3, 
    'x_get_list__mutmut_4': x_get_list__mutmut_4, 
    'x_get_list__mutmut_5': x_get_list__mutmut_5, 
    'x_get_list__mutmut_6': x_get_list__mutmut_6, 
    'x_get_list__mutmut_7': x_get_list__mutmut_7, 
    'x_get_list__mutmut_8': x_get_list__mutmut_8, 
    'x_get_list__mutmut_9': x_get_list__mutmut_9, 
    'x_get_list__mutmut_10': x_get_list__mutmut_10, 
    'x_get_list__mutmut_11': x_get_list__mutmut_11, 
    'x_get_list__mutmut_12': x_get_list__mutmut_12, 
    'x_get_list__mutmut_13': x_get_list__mutmut_13
}

def get_list(*args, **kwargs):
    result = _mutmut_trampoline(x_get_list__mutmut_orig, x_get_list__mutmut_mutants, args, kwargs)
    return result 

get_list.__signature__ = _mutmut_signature(x_get_list__mutmut_orig)
x_get_list__mutmut_orig.__name__ = 'x_get_list'


def x_get_tuple__mutmut_orig(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_1(name: str, default: tuple[str, ...] | None = None, separator: str = "XX,XX") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_2(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = None
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_3(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(None)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_4(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is not None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_5(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default and ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_6(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = None
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_7(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(None, separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_8(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=None, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_9(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=None)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_10(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(separator=separator, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_11(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, strip=True)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_12(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, )
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_13(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=False)
    return tuple(item for item in items if item)


def x_get_tuple__mutmut_14(name: str, default: tuple[str, ...] | None = None, separator: str = ",") -> tuple[str, ...]:
    """Get tuple from environment variable.

    Args:
        name: Environment variable name
        default: Default tuple if not set
        separator: String separator (default: comma)

    Returns:
        Tuple of strings

    Examples:
        >>> os.environ['COORDINATES'] = '1.0,2.0,3.0'
        >>> get_tuple('COORDINATES')
        ('1.0', '2.0', '3.0')

    """
    value = os.environ.get(name)
    if value is None:
        return default or ()

    items = parse_tuple(value, separator=separator, strip=True)
    return tuple(None)

x_get_tuple__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_tuple__mutmut_1': x_get_tuple__mutmut_1, 
    'x_get_tuple__mutmut_2': x_get_tuple__mutmut_2, 
    'x_get_tuple__mutmut_3': x_get_tuple__mutmut_3, 
    'x_get_tuple__mutmut_4': x_get_tuple__mutmut_4, 
    'x_get_tuple__mutmut_5': x_get_tuple__mutmut_5, 
    'x_get_tuple__mutmut_6': x_get_tuple__mutmut_6, 
    'x_get_tuple__mutmut_7': x_get_tuple__mutmut_7, 
    'x_get_tuple__mutmut_8': x_get_tuple__mutmut_8, 
    'x_get_tuple__mutmut_9': x_get_tuple__mutmut_9, 
    'x_get_tuple__mutmut_10': x_get_tuple__mutmut_10, 
    'x_get_tuple__mutmut_11': x_get_tuple__mutmut_11, 
    'x_get_tuple__mutmut_12': x_get_tuple__mutmut_12, 
    'x_get_tuple__mutmut_13': x_get_tuple__mutmut_13, 
    'x_get_tuple__mutmut_14': x_get_tuple__mutmut_14
}

def get_tuple(*args, **kwargs):
    result = _mutmut_trampoline(x_get_tuple__mutmut_orig, x_get_tuple__mutmut_mutants, args, kwargs)
    return result 

get_tuple.__signature__ = _mutmut_signature(x_get_tuple__mutmut_orig)
x_get_tuple__mutmut_orig.__name__ = 'x_get_tuple'


def x_get_set__mutmut_orig(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_1(name: str, default: set[str] | None = None, separator: str = "XX,XX") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_2(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = None
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_3(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(None)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_4(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is not None:
        return default or set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_5(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default and set()

    items = parse_set(value, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_6(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = None
    return {item for item in items if item}


def x_get_set__mutmut_7(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(None, separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_8(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=None, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_9(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=None)
    return {item for item in items if item}


def x_get_set__mutmut_10(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(separator=separator, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_11(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, strip=True)
    return {item for item in items if item}


def x_get_set__mutmut_12(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, )
    return {item for item in items if item}


def x_get_set__mutmut_13(name: str, default: set[str] | None = None, separator: str = ",") -> set[str]:
    """Get set from environment variable (duplicates removed).

    Args:
        name: Environment variable name
        default: Default set if not set
        separator: String separator (default: comma)

    Returns:
        Set of strings

    Examples:
        >>> os.environ['TAGS'] = 'dev,test,dev,prod'
        >>> get_set('TAGS')
        {'dev', 'test', 'prod'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or set()

    items = parse_set(value, separator=separator, strip=False)
    return {item for item in items if item}

x_get_set__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_set__mutmut_1': x_get_set__mutmut_1, 
    'x_get_set__mutmut_2': x_get_set__mutmut_2, 
    'x_get_set__mutmut_3': x_get_set__mutmut_3, 
    'x_get_set__mutmut_4': x_get_set__mutmut_4, 
    'x_get_set__mutmut_5': x_get_set__mutmut_5, 
    'x_get_set__mutmut_6': x_get_set__mutmut_6, 
    'x_get_set__mutmut_7': x_get_set__mutmut_7, 
    'x_get_set__mutmut_8': x_get_set__mutmut_8, 
    'x_get_set__mutmut_9': x_get_set__mutmut_9, 
    'x_get_set__mutmut_10': x_get_set__mutmut_10, 
    'x_get_set__mutmut_11': x_get_set__mutmut_11, 
    'x_get_set__mutmut_12': x_get_set__mutmut_12, 
    'x_get_set__mutmut_13': x_get_set__mutmut_13
}

def get_set(*args, **kwargs):
    result = _mutmut_trampoline(x_get_set__mutmut_orig, x_get_set__mutmut_mutants, args, kwargs)
    return result 

get_set.__signature__ = _mutmut_signature(x_get_set__mutmut_orig)
x_get_set__mutmut_orig.__name__ = 'x_get_set'


def x_get_dict__mutmut_orig(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_1(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = "XX,XX",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_2(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "XX=XX",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_3(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = None
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_4(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(None)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_5(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is not None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_6(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default and {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_7(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            None,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_8(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=None,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_9(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=None,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_10(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=None,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_11(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_12(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_13(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_14(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_15(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=False,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_16(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            None,
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_17(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=None,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_18(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=None,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_19(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=None,
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_20(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_21(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_22(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_23(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_24(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "XXInvalid dictionary format in environment variableXX",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_25(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_26(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "INVALID DICTIONARY FORMAT IN ENVIRONMENT VARIABLE",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_27(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(None),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_28(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = None
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_29(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = None
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_30(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(None)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_31(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = None
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_32(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_33(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                break
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_34(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_35(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                break
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_36(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = None
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_37(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(None, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_38(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, None)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_39(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_40(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, )
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_41(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.rsplit(key_value_separator, 1)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_42(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 2)
            result[key.strip()] = val.strip()
        return result


def x_get_dict__mutmut_43(
    name: str,
    default: dict[str, str] | None = None,
    item_separator: str = ",",
    key_value_separator: str = "=",
) -> dict[str, str]:
    """Get dictionary from environment variable.

    Args:
        name: Environment variable name
        default: Default dict if not set
        item_separator: Separator between items
        key_value_separator: Separator between key and value

    Returns:
        Dictionary of string key-value pairs

    Examples:
        >>> os.environ['CONFIG'] = 'key1=val1,key2=val2'
        >>> get_dict('CONFIG')
        {'key1': 'val1', 'key2': 'val2'}

    """
    value = os.environ.get(name)
    if value is None:
        return default or {}

    try:
        return parse_dict(
            value,
            item_separator=item_separator,
            key_separator=key_value_separator,
            strip=True,
        )
    except ValueError as e:
        # parse_dict raises on invalid format, log warning and return partial result
        _get_logger().warning(
            "Invalid dictionary format in environment variable",
            var=name,
            value=value,
            error=str(e),
        )
        # Try to parse what we can, skipping invalid items
        result = {}
        items = value.split(item_separator)
        for item in items:
            item = item.strip()
            if not item:
                continue
            if key_value_separator not in item:
                continue
            key, val = item.split(key_value_separator, 1)
            result[key.strip()] = None
        return result

x_get_dict__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_dict__mutmut_1': x_get_dict__mutmut_1, 
    'x_get_dict__mutmut_2': x_get_dict__mutmut_2, 
    'x_get_dict__mutmut_3': x_get_dict__mutmut_3, 
    'x_get_dict__mutmut_4': x_get_dict__mutmut_4, 
    'x_get_dict__mutmut_5': x_get_dict__mutmut_5, 
    'x_get_dict__mutmut_6': x_get_dict__mutmut_6, 
    'x_get_dict__mutmut_7': x_get_dict__mutmut_7, 
    'x_get_dict__mutmut_8': x_get_dict__mutmut_8, 
    'x_get_dict__mutmut_9': x_get_dict__mutmut_9, 
    'x_get_dict__mutmut_10': x_get_dict__mutmut_10, 
    'x_get_dict__mutmut_11': x_get_dict__mutmut_11, 
    'x_get_dict__mutmut_12': x_get_dict__mutmut_12, 
    'x_get_dict__mutmut_13': x_get_dict__mutmut_13, 
    'x_get_dict__mutmut_14': x_get_dict__mutmut_14, 
    'x_get_dict__mutmut_15': x_get_dict__mutmut_15, 
    'x_get_dict__mutmut_16': x_get_dict__mutmut_16, 
    'x_get_dict__mutmut_17': x_get_dict__mutmut_17, 
    'x_get_dict__mutmut_18': x_get_dict__mutmut_18, 
    'x_get_dict__mutmut_19': x_get_dict__mutmut_19, 
    'x_get_dict__mutmut_20': x_get_dict__mutmut_20, 
    'x_get_dict__mutmut_21': x_get_dict__mutmut_21, 
    'x_get_dict__mutmut_22': x_get_dict__mutmut_22, 
    'x_get_dict__mutmut_23': x_get_dict__mutmut_23, 
    'x_get_dict__mutmut_24': x_get_dict__mutmut_24, 
    'x_get_dict__mutmut_25': x_get_dict__mutmut_25, 
    'x_get_dict__mutmut_26': x_get_dict__mutmut_26, 
    'x_get_dict__mutmut_27': x_get_dict__mutmut_27, 
    'x_get_dict__mutmut_28': x_get_dict__mutmut_28, 
    'x_get_dict__mutmut_29': x_get_dict__mutmut_29, 
    'x_get_dict__mutmut_30': x_get_dict__mutmut_30, 
    'x_get_dict__mutmut_31': x_get_dict__mutmut_31, 
    'x_get_dict__mutmut_32': x_get_dict__mutmut_32, 
    'x_get_dict__mutmut_33': x_get_dict__mutmut_33, 
    'x_get_dict__mutmut_34': x_get_dict__mutmut_34, 
    'x_get_dict__mutmut_35': x_get_dict__mutmut_35, 
    'x_get_dict__mutmut_36': x_get_dict__mutmut_36, 
    'x_get_dict__mutmut_37': x_get_dict__mutmut_37, 
    'x_get_dict__mutmut_38': x_get_dict__mutmut_38, 
    'x_get_dict__mutmut_39': x_get_dict__mutmut_39, 
    'x_get_dict__mutmut_40': x_get_dict__mutmut_40, 
    'x_get_dict__mutmut_41': x_get_dict__mutmut_41, 
    'x_get_dict__mutmut_42': x_get_dict__mutmut_42, 
    'x_get_dict__mutmut_43': x_get_dict__mutmut_43
}

def get_dict(*args, **kwargs):
    result = _mutmut_trampoline(x_get_dict__mutmut_orig, x_get_dict__mutmut_mutants, args, kwargs)
    return result 

get_dict.__signature__ = _mutmut_signature(x_get_dict__mutmut_orig)
x_get_dict__mutmut_orig.__name__ = 'x_get_dict'


def x__parse_simple_type__mutmut_orig(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_1(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is not bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_2(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(None)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_3(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is not int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_4(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(None)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_5(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is not float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_6(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(None)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_7(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is not str:
        return get_str(name)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_8(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(None)
    if type_hint is Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_9(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is not Path:
        return get_path(name)
    # Fallback to string for unknown simple types
    return os.environ[name]


def x__parse_simple_type__mutmut_10(name: str, type_hint: type) -> Any:
    """Parse environment variable for simple types."""
    if type_hint is bool:
        return get_bool(name)
    if type_hint is int:
        return get_int(name)
    if type_hint is float:
        return get_float(name)
    if type_hint is str:
        return get_str(name)
    if type_hint is Path:
        return get_path(None)
    # Fallback to string for unknown simple types
    return os.environ[name]

x__parse_simple_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_simple_type__mutmut_1': x__parse_simple_type__mutmut_1, 
    'x__parse_simple_type__mutmut_2': x__parse_simple_type__mutmut_2, 
    'x__parse_simple_type__mutmut_3': x__parse_simple_type__mutmut_3, 
    'x__parse_simple_type__mutmut_4': x__parse_simple_type__mutmut_4, 
    'x__parse_simple_type__mutmut_5': x__parse_simple_type__mutmut_5, 
    'x__parse_simple_type__mutmut_6': x__parse_simple_type__mutmut_6, 
    'x__parse_simple_type__mutmut_7': x__parse_simple_type__mutmut_7, 
    'x__parse_simple_type__mutmut_8': x__parse_simple_type__mutmut_8, 
    'x__parse_simple_type__mutmut_9': x__parse_simple_type__mutmut_9, 
    'x__parse_simple_type__mutmut_10': x__parse_simple_type__mutmut_10
}

def _parse_simple_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_simple_type__mutmut_orig, x__parse_simple_type__mutmut_mutants, args, kwargs)
    return result 

_parse_simple_type.__signature__ = _mutmut_signature(x__parse_simple_type__mutmut_orig)
x__parse_simple_type__mutmut_orig.__name__ = 'x__parse_simple_type'


def x__parse_complex_type__mutmut_orig(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_1(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is not list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_2(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(None)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_3(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is not tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_4(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(None)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_5(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is not set:
        return get_set(name)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_6(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(None)
    if origin is dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_7(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is not dict:
        return get_dict(name)
    # Fallback to string for unknown complex types
    return os.environ[name]


def x__parse_complex_type__mutmut_8(name: str, origin: type) -> Any:
    """Parse environment variable for complex types."""
    if origin is list:
        return get_list(name)
    if origin is tuple:
        return get_tuple(name)
    if origin is set:
        return get_set(name)
    if origin is dict:
        return get_dict(None)
    # Fallback to string for unknown complex types
    return os.environ[name]

x__parse_complex_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_complex_type__mutmut_1': x__parse_complex_type__mutmut_1, 
    'x__parse_complex_type__mutmut_2': x__parse_complex_type__mutmut_2, 
    'x__parse_complex_type__mutmut_3': x__parse_complex_type__mutmut_3, 
    'x__parse_complex_type__mutmut_4': x__parse_complex_type__mutmut_4, 
    'x__parse_complex_type__mutmut_5': x__parse_complex_type__mutmut_5, 
    'x__parse_complex_type__mutmut_6': x__parse_complex_type__mutmut_6, 
    'x__parse_complex_type__mutmut_7': x__parse_complex_type__mutmut_7, 
    'x__parse_complex_type__mutmut_8': x__parse_complex_type__mutmut_8
}

def _parse_complex_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_complex_type__mutmut_orig, x__parse_complex_type__mutmut_mutants, args, kwargs)
    return result 

_parse_complex_type.__signature__ = _mutmut_signature(x__parse_complex_type__mutmut_orig)
x__parse_complex_type__mutmut_orig.__name__ = 'x__parse_complex_type'


def x_require__mutmut_orig(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_1(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_2(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            None,
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_3(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=None,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_4(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule=None,
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_5(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_6(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_7(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_8(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="XXrequiredXX",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_9(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="REQUIRED",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_10(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is not None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_11(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = None
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_12(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(None)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_13(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is not None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_14(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(None, type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_15(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, None)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_16(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(type_hint)
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_17(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, )
    else:
        return _parse_complex_type(name, origin)


def x_require__mutmut_18(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(None, origin)


def x_require__mutmut_19(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, None)


def x_require__mutmut_20(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(origin)


def x_require__mutmut_21(name: str, type_hint: type[T] | None = None) -> Any:
    """Require an environment variable to be set.

    Args:
        name: Environment variable name
        type_hint: Optional type hint for parsing

    Returns:
        Parsed value

    Raises:
        ValidationError: If variable is not set

    """
    if name not in os.environ:
        raise ValidationError(
            f"Required environment variable not set: {name}",
            field=name,
            rule="required",
        )

    if type_hint is None:
        return os.environ[name]

    # Parse based on type hint
    origin = get_origin(type_hint)
    if origin is None:
        return _parse_simple_type(name, type_hint)
    else:
        return _parse_complex_type(name, )

x_require__mutmut_mutants : ClassVar[MutantDict] = {
'x_require__mutmut_1': x_require__mutmut_1, 
    'x_require__mutmut_2': x_require__mutmut_2, 
    'x_require__mutmut_3': x_require__mutmut_3, 
    'x_require__mutmut_4': x_require__mutmut_4, 
    'x_require__mutmut_5': x_require__mutmut_5, 
    'x_require__mutmut_6': x_require__mutmut_6, 
    'x_require__mutmut_7': x_require__mutmut_7, 
    'x_require__mutmut_8': x_require__mutmut_8, 
    'x_require__mutmut_9': x_require__mutmut_9, 
    'x_require__mutmut_10': x_require__mutmut_10, 
    'x_require__mutmut_11': x_require__mutmut_11, 
    'x_require__mutmut_12': x_require__mutmut_12, 
    'x_require__mutmut_13': x_require__mutmut_13, 
    'x_require__mutmut_14': x_require__mutmut_14, 
    'x_require__mutmut_15': x_require__mutmut_15, 
    'x_require__mutmut_16': x_require__mutmut_16, 
    'x_require__mutmut_17': x_require__mutmut_17, 
    'x_require__mutmut_18': x_require__mutmut_18, 
    'x_require__mutmut_19': x_require__mutmut_19, 
    'x_require__mutmut_20': x_require__mutmut_20, 
    'x_require__mutmut_21': x_require__mutmut_21
}

def require(*args, **kwargs):
    result = _mutmut_trampoline(x_require__mutmut_orig, x_require__mutmut_mutants, args, kwargs)
    return result 

require.__signature__ = _mutmut_signature(x_require__mutmut_orig)
x_require__mutmut_orig.__name__ = 'x_require'


# <3 🧱🤝🧰🪄
