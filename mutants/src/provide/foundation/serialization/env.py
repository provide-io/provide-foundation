# provide/foundation/serialization/env.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

""".env file format serialization with caching support."""
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


def x_env_dumps__mutmut_orig(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_1(obj: dict[str, str], *, quote_values: bool = False) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_2(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_3(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError(None)

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_4(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("XXENV serialization requires a dictionaryXX")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_5(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("env serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_6(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV SERIALIZATION REQUIRES A DICTIONARY")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_7(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = None

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_8(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) and not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_9(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_10(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_11(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(None)

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_12(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = None

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_13(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(None)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_14(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values or (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_15(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str and "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_16(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and ("XX XX" in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_17(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " not in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_18(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "XX\tXX" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_19(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" not in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_20(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = None

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_21(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(None)

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_22(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) - "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_23(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(None) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_24(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "XX\nXX".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_25(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "XX\nXX"
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to ENV format: {e}") from e


def x_env_dumps__mutmut_26(obj: dict[str, str], *, quote_values: bool = True) -> str:
    """Serialize dictionary to .env file format string.

    Args:
        obj: Dictionary of environment variables
        quote_values: Whether to quote string values

    Returns:
        .env format string

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> env_dumps({"KEY": "value"})
        'KEY="value"\\n'
        >>> env_dumps({"KEY": "value"}, quote_values=False)
        'KEY=value\\n'

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(obj, dict):
        raise ValidationError("ENV serialization requires a dictionary")

    lines: list[str] = []

    try:
        for key, value in obj.items():
            # Ensure key is valid
            if not isinstance(key, str) or not key:
                raise ValidationError(f"Invalid environment variable name: {key}")

            value_str = str(value)

            # Quote if requested and contains spaces
            if quote_values and (" " in value_str or "\t" in value_str):
                value_str = f'"{value_str}"'

            lines.append(f"{key}={value_str}")

        return "\n".join(lines) + "\n"
    except Exception as e:
        raise ValidationError(None) from e

x_env_dumps__mutmut_mutants : ClassVar[MutantDict] = {
'x_env_dumps__mutmut_1': x_env_dumps__mutmut_1, 
    'x_env_dumps__mutmut_2': x_env_dumps__mutmut_2, 
    'x_env_dumps__mutmut_3': x_env_dumps__mutmut_3, 
    'x_env_dumps__mutmut_4': x_env_dumps__mutmut_4, 
    'x_env_dumps__mutmut_5': x_env_dumps__mutmut_5, 
    'x_env_dumps__mutmut_6': x_env_dumps__mutmut_6, 
    'x_env_dumps__mutmut_7': x_env_dumps__mutmut_7, 
    'x_env_dumps__mutmut_8': x_env_dumps__mutmut_8, 
    'x_env_dumps__mutmut_9': x_env_dumps__mutmut_9, 
    'x_env_dumps__mutmut_10': x_env_dumps__mutmut_10, 
    'x_env_dumps__mutmut_11': x_env_dumps__mutmut_11, 
    'x_env_dumps__mutmut_12': x_env_dumps__mutmut_12, 
    'x_env_dumps__mutmut_13': x_env_dumps__mutmut_13, 
    'x_env_dumps__mutmut_14': x_env_dumps__mutmut_14, 
    'x_env_dumps__mutmut_15': x_env_dumps__mutmut_15, 
    'x_env_dumps__mutmut_16': x_env_dumps__mutmut_16, 
    'x_env_dumps__mutmut_17': x_env_dumps__mutmut_17, 
    'x_env_dumps__mutmut_18': x_env_dumps__mutmut_18, 
    'x_env_dumps__mutmut_19': x_env_dumps__mutmut_19, 
    'x_env_dumps__mutmut_20': x_env_dumps__mutmut_20, 
    'x_env_dumps__mutmut_21': x_env_dumps__mutmut_21, 
    'x_env_dumps__mutmut_22': x_env_dumps__mutmut_22, 
    'x_env_dumps__mutmut_23': x_env_dumps__mutmut_23, 
    'x_env_dumps__mutmut_24': x_env_dumps__mutmut_24, 
    'x_env_dumps__mutmut_25': x_env_dumps__mutmut_25, 
    'x_env_dumps__mutmut_26': x_env_dumps__mutmut_26
}

def env_dumps(*args, **kwargs):
    result = _mutmut_trampoline(x_env_dumps__mutmut_orig, x_env_dumps__mutmut_mutants, args, kwargs)
    return result 

env_dumps.__signature__ = _mutmut_signature(x_env_dumps__mutmut_orig)
x_env_dumps__mutmut_orig.__name__ = 'x_env_dumps'


def x__parse_env_line__mutmut_orig(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_1(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = None

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_2(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line and line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_3(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_4(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith(None):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_5(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("XX#XX"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_6(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "XX=XX" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_7(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_8(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(None)

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_9(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = None
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_10(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split(None, 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_11(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", None)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_12(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split(1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_13(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", )
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_14(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.rsplit("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_15(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("XX=XX", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_16(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 2)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_17(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = None
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_18(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = None

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_19(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_20(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(None)

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_21(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) and (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_22(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') or value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_23(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith(None) and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_24(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('XX"XX') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_25(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith(None)) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_26(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('XX"XX')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_27(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") or value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_28(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith(None) and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_29(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("XX'XX") and value.endswith("'")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_30(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith(None)):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_31(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("XX'XX")):
        value = value[1:-1]

    return (key, value)


def x__parse_env_line__mutmut_32(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = None

    return (key, value)


def x__parse_env_line__mutmut_33(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[2:-1]

    return (key, value)


def x__parse_env_line__mutmut_34(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:+1]

    return (key, value)


def x__parse_env_line__mutmut_35(line: str, line_num: int) -> tuple[str, str] | None:
    """Parse a single line from .env format.

    Args:
        line: Line to parse
        line_num: Line number for error messages

    Returns:
        (key, value) tuple or None if line should be skipped

    Raises:
        ValidationError: If line is invalid

    """
    from provide.foundation.errors import ValidationError

    line = line.strip()

    # Skip comments and empty lines
    if not line or line.startswith("#"):
        return None

    # Parse key=value
    if "=" not in line:
        raise ValidationError(f"Invalid .env format at line {line_num}: missing '='")

    key, value = line.split("=", 1)
    key = key.strip()
    value = value.strip()

    # Validate key
    if not key:
        raise ValidationError(f"Invalid .env format at line {line_num}: empty key")

    # Remove quotes if present
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-2]

    return (key, value)

x__parse_env_line__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_env_line__mutmut_1': x__parse_env_line__mutmut_1, 
    'x__parse_env_line__mutmut_2': x__parse_env_line__mutmut_2, 
    'x__parse_env_line__mutmut_3': x__parse_env_line__mutmut_3, 
    'x__parse_env_line__mutmut_4': x__parse_env_line__mutmut_4, 
    'x__parse_env_line__mutmut_5': x__parse_env_line__mutmut_5, 
    'x__parse_env_line__mutmut_6': x__parse_env_line__mutmut_6, 
    'x__parse_env_line__mutmut_7': x__parse_env_line__mutmut_7, 
    'x__parse_env_line__mutmut_8': x__parse_env_line__mutmut_8, 
    'x__parse_env_line__mutmut_9': x__parse_env_line__mutmut_9, 
    'x__parse_env_line__mutmut_10': x__parse_env_line__mutmut_10, 
    'x__parse_env_line__mutmut_11': x__parse_env_line__mutmut_11, 
    'x__parse_env_line__mutmut_12': x__parse_env_line__mutmut_12, 
    'x__parse_env_line__mutmut_13': x__parse_env_line__mutmut_13, 
    'x__parse_env_line__mutmut_14': x__parse_env_line__mutmut_14, 
    'x__parse_env_line__mutmut_15': x__parse_env_line__mutmut_15, 
    'x__parse_env_line__mutmut_16': x__parse_env_line__mutmut_16, 
    'x__parse_env_line__mutmut_17': x__parse_env_line__mutmut_17, 
    'x__parse_env_line__mutmut_18': x__parse_env_line__mutmut_18, 
    'x__parse_env_line__mutmut_19': x__parse_env_line__mutmut_19, 
    'x__parse_env_line__mutmut_20': x__parse_env_line__mutmut_20, 
    'x__parse_env_line__mutmut_21': x__parse_env_line__mutmut_21, 
    'x__parse_env_line__mutmut_22': x__parse_env_line__mutmut_22, 
    'x__parse_env_line__mutmut_23': x__parse_env_line__mutmut_23, 
    'x__parse_env_line__mutmut_24': x__parse_env_line__mutmut_24, 
    'x__parse_env_line__mutmut_25': x__parse_env_line__mutmut_25, 
    'x__parse_env_line__mutmut_26': x__parse_env_line__mutmut_26, 
    'x__parse_env_line__mutmut_27': x__parse_env_line__mutmut_27, 
    'x__parse_env_line__mutmut_28': x__parse_env_line__mutmut_28, 
    'x__parse_env_line__mutmut_29': x__parse_env_line__mutmut_29, 
    'x__parse_env_line__mutmut_30': x__parse_env_line__mutmut_30, 
    'x__parse_env_line__mutmut_31': x__parse_env_line__mutmut_31, 
    'x__parse_env_line__mutmut_32': x__parse_env_line__mutmut_32, 
    'x__parse_env_line__mutmut_33': x__parse_env_line__mutmut_33, 
    'x__parse_env_line__mutmut_34': x__parse_env_line__mutmut_34, 
    'x__parse_env_line__mutmut_35': x__parse_env_line__mutmut_35
}

def _parse_env_line(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_env_line__mutmut_orig, x__parse_env_line__mutmut_mutants, args, kwargs)
    return result 

_parse_env_line.__signature__ = _mutmut_signature(x__parse_env_line__mutmut_orig)
x__parse_env_line__mutmut_orig.__name__ = 'x__parse_env_line'


def x_env_loads__mutmut_orig(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_1(s: str, *, use_cache: bool = False) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_2(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_3(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError(None)

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_4(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("XXInput must be a stringXX")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_5(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_6(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("INPUT MUST BE A STRING")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_7(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_8(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = None
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_9(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_10(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_11(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_12(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_13(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXenvXX")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_14(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ENV")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_15(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = None
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_16(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(None)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_17(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_18(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = None

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_19(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(None, 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_20(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), None):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_21(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_22(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), ):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_23(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 2):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_24(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = None
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_25(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(None, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_26(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, None)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_27(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_28(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, )
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_29(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_30(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = None
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_31(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = None
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_32(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(None) from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_33(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_34(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = None
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_35(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_36(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_37(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("env")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_38(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_39(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXenvXX")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_40(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "ENV")
        get_serialization_cache().set(cache_key, result)

    return result


def x_env_loads__mutmut_41(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(None, result)

    return result


def x_env_loads__mutmut_42(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, None)

    return result


def x_env_loads__mutmut_43(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(result)

    return result


def x_env_loads__mutmut_44(s: str, *, use_cache: bool = True) -> dict[str, str]:
    """Deserialize .env file format string to dictionary.

    Args:
        s: .env format string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Dictionary of environment variables

    Raises:
        ValidationError: If string is not valid .env format

    Example:
        >>> env_loads('KEY=value')
        {'KEY': 'value'}
        >>> env_loads('KEY="value"')
        {'KEY': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    result: dict[str, str] = {}

    try:
        for line_num, line in enumerate(s.splitlines(), 1):
            parsed = _parse_env_line(line, line_num)
            if parsed is not None:
                key, value = parsed
                result[key] = value
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Invalid .env format string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "env")
        get_serialization_cache().set(cache_key, )

    return result

x_env_loads__mutmut_mutants : ClassVar[MutantDict] = {
'x_env_loads__mutmut_1': x_env_loads__mutmut_1, 
    'x_env_loads__mutmut_2': x_env_loads__mutmut_2, 
    'x_env_loads__mutmut_3': x_env_loads__mutmut_3, 
    'x_env_loads__mutmut_4': x_env_loads__mutmut_4, 
    'x_env_loads__mutmut_5': x_env_loads__mutmut_5, 
    'x_env_loads__mutmut_6': x_env_loads__mutmut_6, 
    'x_env_loads__mutmut_7': x_env_loads__mutmut_7, 
    'x_env_loads__mutmut_8': x_env_loads__mutmut_8, 
    'x_env_loads__mutmut_9': x_env_loads__mutmut_9, 
    'x_env_loads__mutmut_10': x_env_loads__mutmut_10, 
    'x_env_loads__mutmut_11': x_env_loads__mutmut_11, 
    'x_env_loads__mutmut_12': x_env_loads__mutmut_12, 
    'x_env_loads__mutmut_13': x_env_loads__mutmut_13, 
    'x_env_loads__mutmut_14': x_env_loads__mutmut_14, 
    'x_env_loads__mutmut_15': x_env_loads__mutmut_15, 
    'x_env_loads__mutmut_16': x_env_loads__mutmut_16, 
    'x_env_loads__mutmut_17': x_env_loads__mutmut_17, 
    'x_env_loads__mutmut_18': x_env_loads__mutmut_18, 
    'x_env_loads__mutmut_19': x_env_loads__mutmut_19, 
    'x_env_loads__mutmut_20': x_env_loads__mutmut_20, 
    'x_env_loads__mutmut_21': x_env_loads__mutmut_21, 
    'x_env_loads__mutmut_22': x_env_loads__mutmut_22, 
    'x_env_loads__mutmut_23': x_env_loads__mutmut_23, 
    'x_env_loads__mutmut_24': x_env_loads__mutmut_24, 
    'x_env_loads__mutmut_25': x_env_loads__mutmut_25, 
    'x_env_loads__mutmut_26': x_env_loads__mutmut_26, 
    'x_env_loads__mutmut_27': x_env_loads__mutmut_27, 
    'x_env_loads__mutmut_28': x_env_loads__mutmut_28, 
    'x_env_loads__mutmut_29': x_env_loads__mutmut_29, 
    'x_env_loads__mutmut_30': x_env_loads__mutmut_30, 
    'x_env_loads__mutmut_31': x_env_loads__mutmut_31, 
    'x_env_loads__mutmut_32': x_env_loads__mutmut_32, 
    'x_env_loads__mutmut_33': x_env_loads__mutmut_33, 
    'x_env_loads__mutmut_34': x_env_loads__mutmut_34, 
    'x_env_loads__mutmut_35': x_env_loads__mutmut_35, 
    'x_env_loads__mutmut_36': x_env_loads__mutmut_36, 
    'x_env_loads__mutmut_37': x_env_loads__mutmut_37, 
    'x_env_loads__mutmut_38': x_env_loads__mutmut_38, 
    'x_env_loads__mutmut_39': x_env_loads__mutmut_39, 
    'x_env_loads__mutmut_40': x_env_loads__mutmut_40, 
    'x_env_loads__mutmut_41': x_env_loads__mutmut_41, 
    'x_env_loads__mutmut_42': x_env_loads__mutmut_42, 
    'x_env_loads__mutmut_43': x_env_loads__mutmut_43, 
    'x_env_loads__mutmut_44': x_env_loads__mutmut_44
}

def env_loads(*args, **kwargs):
    result = _mutmut_trampoline(x_env_loads__mutmut_orig, x_env_loads__mutmut_mutants, args, kwargs)
    return result 

env_loads.__signature__ = _mutmut_signature(x_env_loads__mutmut_orig)
x_env_loads__mutmut_orig.__name__ = 'x_env_loads'


__all__ = [
    "env_dumps",
    "env_loads",
]


# <3 🧱🤝📜🪄
