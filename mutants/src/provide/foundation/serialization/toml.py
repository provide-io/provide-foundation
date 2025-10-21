# provide/foundation/serialization/toml.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""TOML serialization with caching support."""
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


def x_toml_dumps__mutmut_orig(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_1(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError(None) from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_2(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("XXtomli-w is required for TOML write operationsXX") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_3(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for toml write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_4(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("TOMLI-W IS REQUIRED FOR TOML WRITE OPERATIONS") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_5(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_6(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError(None)

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_7(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("XXTOML serialization requires a dictionary at the top levelXX")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_8(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("toml serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_9(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML SERIALIZATION REQUIRES A DICTIONARY AT THE TOP LEVEL")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_10(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(None)
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to TOML: {e}") from e


def x_toml_dumps__mutmut_11(obj: dict[str, Any]) -> str:
    """Serialize dictionary to TOML string.

    Args:
        obj: Dictionary to serialize (TOML requires dict at top level)

    Returns:
        TOML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If tomli-w is not installed

    Example:
        >>> toml_dumps({"key": "value"})
        'key = "value"\\n'

    """
    from provide.foundation.errors import ValidationError

    try:
        import tomli_w
    except ImportError as e:
        raise ImportError("tomli-w is required for TOML write operations") from e

    if not isinstance(obj, dict):
        raise ValidationError("TOML serialization requires a dictionary at the top level")

    try:
        return tomli_w.dumps(obj)
    except Exception as e:
        raise ValidationError(None) from e

x_toml_dumps__mutmut_mutants : ClassVar[MutantDict] = {
'x_toml_dumps__mutmut_1': x_toml_dumps__mutmut_1, 
    'x_toml_dumps__mutmut_2': x_toml_dumps__mutmut_2, 
    'x_toml_dumps__mutmut_3': x_toml_dumps__mutmut_3, 
    'x_toml_dumps__mutmut_4': x_toml_dumps__mutmut_4, 
    'x_toml_dumps__mutmut_5': x_toml_dumps__mutmut_5, 
    'x_toml_dumps__mutmut_6': x_toml_dumps__mutmut_6, 
    'x_toml_dumps__mutmut_7': x_toml_dumps__mutmut_7, 
    'x_toml_dumps__mutmut_8': x_toml_dumps__mutmut_8, 
    'x_toml_dumps__mutmut_9': x_toml_dumps__mutmut_9, 
    'x_toml_dumps__mutmut_10': x_toml_dumps__mutmut_10, 
    'x_toml_dumps__mutmut_11': x_toml_dumps__mutmut_11
}

def toml_dumps(*args, **kwargs):
    result = _mutmut_trampoline(x_toml_dumps__mutmut_orig, x_toml_dumps__mutmut_mutants, args, kwargs)
    return result 

toml_dumps.__signature__ = _mutmut_signature(x_toml_dumps__mutmut_orig)
x_toml_dumps__mutmut_orig.__name__ = 'x_toml_dumps'


def x_toml_loads__mutmut_orig(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_1(s: str, *, use_cache: bool = False) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_2(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_3(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError(None)

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_4(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("XXInput must be a stringXX")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_5(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_6(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("INPUT MUST BE A STRING")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_7(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_8(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

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
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_9(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_10(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

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
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_11(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_12(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

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
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_13(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXtomlXX")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_14(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "TOML")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_15(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = None
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_16(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(None)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_17(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_18(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = None
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_19(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(None)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_20(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(None) from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_21(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_22(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = None
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_23(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_24(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_25(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("toml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_26(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_27(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXtomlXX")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_28(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "TOML")
        get_serialization_cache().set(cache_key, result)

    return result


def x_toml_loads__mutmut_29(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(None, result)

    return result


def x_toml_loads__mutmut_30(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, None)

    return result


def x_toml_loads__mutmut_31(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(result)

    return result


def x_toml_loads__mutmut_32(s: str, *, use_cache: bool = True) -> dict[str, Any]:
    """Deserialize TOML string to Python dictionary.

    Args:
        s: TOML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python dictionary

    Raises:
        ValidationError: If string is not valid TOML

    Example:
        >>> toml_loads('key = "value"')
        {'key': 'value'}

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = tomllib.loads(s)
    except Exception as e:
        raise ValidationError(f"Invalid TOML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "toml")
        get_serialization_cache().set(cache_key, )

    return result

x_toml_loads__mutmut_mutants : ClassVar[MutantDict] = {
'x_toml_loads__mutmut_1': x_toml_loads__mutmut_1, 
    'x_toml_loads__mutmut_2': x_toml_loads__mutmut_2, 
    'x_toml_loads__mutmut_3': x_toml_loads__mutmut_3, 
    'x_toml_loads__mutmut_4': x_toml_loads__mutmut_4, 
    'x_toml_loads__mutmut_5': x_toml_loads__mutmut_5, 
    'x_toml_loads__mutmut_6': x_toml_loads__mutmut_6, 
    'x_toml_loads__mutmut_7': x_toml_loads__mutmut_7, 
    'x_toml_loads__mutmut_8': x_toml_loads__mutmut_8, 
    'x_toml_loads__mutmut_9': x_toml_loads__mutmut_9, 
    'x_toml_loads__mutmut_10': x_toml_loads__mutmut_10, 
    'x_toml_loads__mutmut_11': x_toml_loads__mutmut_11, 
    'x_toml_loads__mutmut_12': x_toml_loads__mutmut_12, 
    'x_toml_loads__mutmut_13': x_toml_loads__mutmut_13, 
    'x_toml_loads__mutmut_14': x_toml_loads__mutmut_14, 
    'x_toml_loads__mutmut_15': x_toml_loads__mutmut_15, 
    'x_toml_loads__mutmut_16': x_toml_loads__mutmut_16, 
    'x_toml_loads__mutmut_17': x_toml_loads__mutmut_17, 
    'x_toml_loads__mutmut_18': x_toml_loads__mutmut_18, 
    'x_toml_loads__mutmut_19': x_toml_loads__mutmut_19, 
    'x_toml_loads__mutmut_20': x_toml_loads__mutmut_20, 
    'x_toml_loads__mutmut_21': x_toml_loads__mutmut_21, 
    'x_toml_loads__mutmut_22': x_toml_loads__mutmut_22, 
    'x_toml_loads__mutmut_23': x_toml_loads__mutmut_23, 
    'x_toml_loads__mutmut_24': x_toml_loads__mutmut_24, 
    'x_toml_loads__mutmut_25': x_toml_loads__mutmut_25, 
    'x_toml_loads__mutmut_26': x_toml_loads__mutmut_26, 
    'x_toml_loads__mutmut_27': x_toml_loads__mutmut_27, 
    'x_toml_loads__mutmut_28': x_toml_loads__mutmut_28, 
    'x_toml_loads__mutmut_29': x_toml_loads__mutmut_29, 
    'x_toml_loads__mutmut_30': x_toml_loads__mutmut_30, 
    'x_toml_loads__mutmut_31': x_toml_loads__mutmut_31, 
    'x_toml_loads__mutmut_32': x_toml_loads__mutmut_32
}

def toml_loads(*args, **kwargs):
    result = _mutmut_trampoline(x_toml_loads__mutmut_orig, x_toml_loads__mutmut_mutants, args, kwargs)
    return result 

toml_loads.__signature__ = _mutmut_signature(x_toml_loads__mutmut_orig)
x_toml_loads__mutmut_orig.__name__ = 'x_toml_loads'


__all__ = [
    "toml_dumps",
    "toml_loads",
]


# <3 🧱🤝📜🪄
