# provide/foundation/serialization/json.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""JSON serialization with caching support."""
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


def x_json_dumps__mutmut_orig(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_1(
    obj: Any,
    *,
    ensure_ascii: bool = True,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_2(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = True,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_3(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(None, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_4(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=None, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_5(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=None, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_6(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=None, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_7(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=None)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_8(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_9(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_10(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_11(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_12(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, )
    except (TypeError, ValueError) as e:
        raise ValidationError(f"Cannot serialize object to JSON: {e}") from e


def x_json_dumps__mutmut_13(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    indent: int | None = None,
    sort_keys: bool = False,
    default: Any = None,
) -> str:
    """Serialize object to JSON string with Foundation tracking.

    Args:
        obj: Object to serialize
        ensure_ascii: If True, non-ASCII characters are escaped
        indent: Number of spaces for indentation (None for compact)
        sort_keys: Whether to sort dictionary keys
        default: Function called for objects that can't be serialized

    Returns:
        JSON string representation

    Raises:
        ValidationError: If object cannot be serialized

    Example:
        >>> json_dumps({"key": "value"})
        '{"key": "value"}'
        >>> json_dumps({"b": 1, "a": 2}, sort_keys=True, indent=2)
        '{\\n  "a": 2,\\n  "b": 1\\n}'

    """
    from provide.foundation.errors import ValidationError

    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys, default=default)
    except (TypeError, ValueError) as e:
        raise ValidationError(None) from e

x_json_dumps__mutmut_mutants : ClassVar[MutantDict] = {
'x_json_dumps__mutmut_1': x_json_dumps__mutmut_1, 
    'x_json_dumps__mutmut_2': x_json_dumps__mutmut_2, 
    'x_json_dumps__mutmut_3': x_json_dumps__mutmut_3, 
    'x_json_dumps__mutmut_4': x_json_dumps__mutmut_4, 
    'x_json_dumps__mutmut_5': x_json_dumps__mutmut_5, 
    'x_json_dumps__mutmut_6': x_json_dumps__mutmut_6, 
    'x_json_dumps__mutmut_7': x_json_dumps__mutmut_7, 
    'x_json_dumps__mutmut_8': x_json_dumps__mutmut_8, 
    'x_json_dumps__mutmut_9': x_json_dumps__mutmut_9, 
    'x_json_dumps__mutmut_10': x_json_dumps__mutmut_10, 
    'x_json_dumps__mutmut_11': x_json_dumps__mutmut_11, 
    'x_json_dumps__mutmut_12': x_json_dumps__mutmut_12, 
    'x_json_dumps__mutmut_13': x_json_dumps__mutmut_13
}

def json_dumps(*args, **kwargs):
    result = _mutmut_trampoline(x_json_dumps__mutmut_orig, x_json_dumps__mutmut_mutants, args, kwargs)
    return result 

json_dumps.__signature__ = _mutmut_signature(x_json_dumps__mutmut_orig)
x_json_dumps__mutmut_orig.__name__ = 'x_json_dumps'


def x_json_loads__mutmut_orig(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_1(s: str, *, use_cache: bool = False) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_2(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_3(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError(None)

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_4(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("XXInput must be a stringXX")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_5(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_6(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("INPUT MUST BE A STRING")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_7(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_8(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

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

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_9(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_10(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

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

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_11(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_12(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

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

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_13(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXjsonXX")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_14(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "JSON")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_15(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = None
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_16(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(None)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_17(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_18(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = None
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_19(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(None)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_20(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(None) from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_21(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_22(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = None
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_23(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_24(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_25(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("json")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_26(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_27(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXjsonXX")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_28(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "JSON")
        get_serialization_cache().set(cache_key, result)

    return result


def x_json_loads__mutmut_29(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(None, result)

    return result


def x_json_loads__mutmut_30(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, None)

    return result


def x_json_loads__mutmut_31(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(result)

    return result


def x_json_loads__mutmut_32(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize JSON string to Python object with Foundation tracking.

    Args:
        s: JSON string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid JSON

    Example:
        >>> json_loads('{"key": "value"}')
        {'key': 'value'}
        >>> json_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = json.loads(s)
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "json")
        get_serialization_cache().set(cache_key, )

    return result

x_json_loads__mutmut_mutants : ClassVar[MutantDict] = {
'x_json_loads__mutmut_1': x_json_loads__mutmut_1, 
    'x_json_loads__mutmut_2': x_json_loads__mutmut_2, 
    'x_json_loads__mutmut_3': x_json_loads__mutmut_3, 
    'x_json_loads__mutmut_4': x_json_loads__mutmut_4, 
    'x_json_loads__mutmut_5': x_json_loads__mutmut_5, 
    'x_json_loads__mutmut_6': x_json_loads__mutmut_6, 
    'x_json_loads__mutmut_7': x_json_loads__mutmut_7, 
    'x_json_loads__mutmut_8': x_json_loads__mutmut_8, 
    'x_json_loads__mutmut_9': x_json_loads__mutmut_9, 
    'x_json_loads__mutmut_10': x_json_loads__mutmut_10, 
    'x_json_loads__mutmut_11': x_json_loads__mutmut_11, 
    'x_json_loads__mutmut_12': x_json_loads__mutmut_12, 
    'x_json_loads__mutmut_13': x_json_loads__mutmut_13, 
    'x_json_loads__mutmut_14': x_json_loads__mutmut_14, 
    'x_json_loads__mutmut_15': x_json_loads__mutmut_15, 
    'x_json_loads__mutmut_16': x_json_loads__mutmut_16, 
    'x_json_loads__mutmut_17': x_json_loads__mutmut_17, 
    'x_json_loads__mutmut_18': x_json_loads__mutmut_18, 
    'x_json_loads__mutmut_19': x_json_loads__mutmut_19, 
    'x_json_loads__mutmut_20': x_json_loads__mutmut_20, 
    'x_json_loads__mutmut_21': x_json_loads__mutmut_21, 
    'x_json_loads__mutmut_22': x_json_loads__mutmut_22, 
    'x_json_loads__mutmut_23': x_json_loads__mutmut_23, 
    'x_json_loads__mutmut_24': x_json_loads__mutmut_24, 
    'x_json_loads__mutmut_25': x_json_loads__mutmut_25, 
    'x_json_loads__mutmut_26': x_json_loads__mutmut_26, 
    'x_json_loads__mutmut_27': x_json_loads__mutmut_27, 
    'x_json_loads__mutmut_28': x_json_loads__mutmut_28, 
    'x_json_loads__mutmut_29': x_json_loads__mutmut_29, 
    'x_json_loads__mutmut_30': x_json_loads__mutmut_30, 
    'x_json_loads__mutmut_31': x_json_loads__mutmut_31, 
    'x_json_loads__mutmut_32': x_json_loads__mutmut_32
}

def json_loads(*args, **kwargs):
    result = _mutmut_trampoline(x_json_loads__mutmut_orig, x_json_loads__mutmut_mutants, args, kwargs)
    return result 

json_loads.__signature__ = _mutmut_signature(x_json_loads__mutmut_orig)
x_json_loads__mutmut_orig.__name__ = 'x_json_loads'


__all__ = [
    "json_dumps",
    "json_loads",
]


# <3 🧱🤝📜🪄
