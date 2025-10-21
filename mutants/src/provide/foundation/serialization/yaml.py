# provide/foundation/serialization/yaml.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass
from provide.foundation.serialization.cache import get_cache_enabled, get_cache_key, get_serialization_cache

"""YAML serialization with caching support."""
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


def x_yaml_dumps__mutmut_orig(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_1(
    obj: Any,
    *,
    default_flow_style: bool = True,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_2(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = False,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_3(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = True,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_4(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError(None) from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_5(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("XXPyYAML is required for YAML operationsXX") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_6(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("pyyaml is required for yaml operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_7(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PYYAML IS REQUIRED FOR YAML OPERATIONS") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_8(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            None,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_9(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=None,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_10(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=None,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_11(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=None,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_12(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_13(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_14(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_15(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            )
    except Exception as e:
        raise ValidationError(f"Cannot serialize object to YAML: {e}") from e


def x_yaml_dumps__mutmut_16(
    obj: Any,
    *,
    default_flow_style: bool = False,
    allow_unicode: bool = True,
    sort_keys: bool = False,
) -> str:
    """Serialize object to YAML string.

    Args:
        obj: Object to serialize
        default_flow_style: Use flow style (JSON-like) instead of block style
        allow_unicode: If True, allow unicode characters
        sort_keys: Whether to sort dictionary keys

    Returns:
        YAML string representation

    Raises:
        ValidationError: If object cannot be serialized
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_dumps({"key": "value"})
        'key: value\\n'

    """
    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    from provide.foundation.errors import ValidationError

    try:
        return yaml.dump(
            obj,
            default_flow_style=default_flow_style,
            allow_unicode=allow_unicode,
            sort_keys=sort_keys,
        )
    except Exception as e:
        raise ValidationError(None) from e

x_yaml_dumps__mutmut_mutants : ClassVar[MutantDict] = {
'x_yaml_dumps__mutmut_1': x_yaml_dumps__mutmut_1, 
    'x_yaml_dumps__mutmut_2': x_yaml_dumps__mutmut_2, 
    'x_yaml_dumps__mutmut_3': x_yaml_dumps__mutmut_3, 
    'x_yaml_dumps__mutmut_4': x_yaml_dumps__mutmut_4, 
    'x_yaml_dumps__mutmut_5': x_yaml_dumps__mutmut_5, 
    'x_yaml_dumps__mutmut_6': x_yaml_dumps__mutmut_6, 
    'x_yaml_dumps__mutmut_7': x_yaml_dumps__mutmut_7, 
    'x_yaml_dumps__mutmut_8': x_yaml_dumps__mutmut_8, 
    'x_yaml_dumps__mutmut_9': x_yaml_dumps__mutmut_9, 
    'x_yaml_dumps__mutmut_10': x_yaml_dumps__mutmut_10, 
    'x_yaml_dumps__mutmut_11': x_yaml_dumps__mutmut_11, 
    'x_yaml_dumps__mutmut_12': x_yaml_dumps__mutmut_12, 
    'x_yaml_dumps__mutmut_13': x_yaml_dumps__mutmut_13, 
    'x_yaml_dumps__mutmut_14': x_yaml_dumps__mutmut_14, 
    'x_yaml_dumps__mutmut_15': x_yaml_dumps__mutmut_15, 
    'x_yaml_dumps__mutmut_16': x_yaml_dumps__mutmut_16
}

def yaml_dumps(*args, **kwargs):
    result = _mutmut_trampoline(x_yaml_dumps__mutmut_orig, x_yaml_dumps__mutmut_mutants, args, kwargs)
    return result 

yaml_dumps.__signature__ = _mutmut_signature(x_yaml_dumps__mutmut_orig)
x_yaml_dumps__mutmut_orig.__name__ = 'x_yaml_dumps'


def x_yaml_loads__mutmut_orig(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_1(s: str, *, use_cache: bool = False) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_2(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_3(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError(None)

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_4(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("XXInput must be a stringXX")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_5(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_6(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("INPUT MUST BE A STRING")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_7(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError(None) from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_8(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("XXPyYAML is required for YAML operationsXX") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_9(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("pyyaml is required for yaml operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_10(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PYYAML IS REQUIRED FOR YAML OPERATIONS") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_11(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_12(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = None
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_13(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_14(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_15(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_16(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_17(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXyamlXX")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_18(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "YAML")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_19(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = None
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_20(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(None)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_21(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_22(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = None
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_23(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(None)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_24(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(None) from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_25(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache or get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_26(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = None
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_27(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(None, "yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_28(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, None)
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_29(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key("yaml")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_30(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, )
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_31(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "XXyamlXX")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_32(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "YAML")
        get_serialization_cache().set(cache_key, result)

    return result


def x_yaml_loads__mutmut_33(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(None, result)

    return result


def x_yaml_loads__mutmut_34(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, None)

    return result


def x_yaml_loads__mutmut_35(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(result)

    return result


def x_yaml_loads__mutmut_36(s: str, *, use_cache: bool = True) -> Any:
    """Deserialize YAML string to Python object.

    Args:
        s: YAML string to deserialize
        use_cache: Whether to use caching for this operation

    Returns:
        Deserialized Python object

    Raises:
        ValidationError: If string is not valid YAML
        ImportError: If PyYAML is not installed

    Example:
        >>> yaml_loads('key: value')
        {'key': 'value'}
        >>> yaml_loads('[1, 2, 3]')
        [1, 2, 3]

    """
    from provide.foundation.errors import ValidationError

    if not isinstance(s, str):
        raise ValidationError("Input must be a string")

    try:
        import yaml
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML operations") from e

    # Check cache first if enabled
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        cached = get_serialization_cache().get(cache_key)
        if cached is not None:
            return cached

    try:
        result = yaml.safe_load(s)
    except yaml.YAMLError as e:
        raise ValidationError(f"Invalid YAML string: {e}") from e

    # Cache result
    if use_cache and get_cache_enabled():
        cache_key = get_cache_key(s, "yaml")
        get_serialization_cache().set(cache_key, )

    return result

x_yaml_loads__mutmut_mutants : ClassVar[MutantDict] = {
'x_yaml_loads__mutmut_1': x_yaml_loads__mutmut_1, 
    'x_yaml_loads__mutmut_2': x_yaml_loads__mutmut_2, 
    'x_yaml_loads__mutmut_3': x_yaml_loads__mutmut_3, 
    'x_yaml_loads__mutmut_4': x_yaml_loads__mutmut_4, 
    'x_yaml_loads__mutmut_5': x_yaml_loads__mutmut_5, 
    'x_yaml_loads__mutmut_6': x_yaml_loads__mutmut_6, 
    'x_yaml_loads__mutmut_7': x_yaml_loads__mutmut_7, 
    'x_yaml_loads__mutmut_8': x_yaml_loads__mutmut_8, 
    'x_yaml_loads__mutmut_9': x_yaml_loads__mutmut_9, 
    'x_yaml_loads__mutmut_10': x_yaml_loads__mutmut_10, 
    'x_yaml_loads__mutmut_11': x_yaml_loads__mutmut_11, 
    'x_yaml_loads__mutmut_12': x_yaml_loads__mutmut_12, 
    'x_yaml_loads__mutmut_13': x_yaml_loads__mutmut_13, 
    'x_yaml_loads__mutmut_14': x_yaml_loads__mutmut_14, 
    'x_yaml_loads__mutmut_15': x_yaml_loads__mutmut_15, 
    'x_yaml_loads__mutmut_16': x_yaml_loads__mutmut_16, 
    'x_yaml_loads__mutmut_17': x_yaml_loads__mutmut_17, 
    'x_yaml_loads__mutmut_18': x_yaml_loads__mutmut_18, 
    'x_yaml_loads__mutmut_19': x_yaml_loads__mutmut_19, 
    'x_yaml_loads__mutmut_20': x_yaml_loads__mutmut_20, 
    'x_yaml_loads__mutmut_21': x_yaml_loads__mutmut_21, 
    'x_yaml_loads__mutmut_22': x_yaml_loads__mutmut_22, 
    'x_yaml_loads__mutmut_23': x_yaml_loads__mutmut_23, 
    'x_yaml_loads__mutmut_24': x_yaml_loads__mutmut_24, 
    'x_yaml_loads__mutmut_25': x_yaml_loads__mutmut_25, 
    'x_yaml_loads__mutmut_26': x_yaml_loads__mutmut_26, 
    'x_yaml_loads__mutmut_27': x_yaml_loads__mutmut_27, 
    'x_yaml_loads__mutmut_28': x_yaml_loads__mutmut_28, 
    'x_yaml_loads__mutmut_29': x_yaml_loads__mutmut_29, 
    'x_yaml_loads__mutmut_30': x_yaml_loads__mutmut_30, 
    'x_yaml_loads__mutmut_31': x_yaml_loads__mutmut_31, 
    'x_yaml_loads__mutmut_32': x_yaml_loads__mutmut_32, 
    'x_yaml_loads__mutmut_33': x_yaml_loads__mutmut_33, 
    'x_yaml_loads__mutmut_34': x_yaml_loads__mutmut_34, 
    'x_yaml_loads__mutmut_35': x_yaml_loads__mutmut_35, 
    'x_yaml_loads__mutmut_36': x_yaml_loads__mutmut_36
}

def yaml_loads(*args, **kwargs):
    result = _mutmut_trampoline(x_yaml_loads__mutmut_orig, x_yaml_loads__mutmut_mutants, args, kwargs)
    return result 

yaml_loads.__signature__ = _mutmut_signature(x_yaml_loads__mutmut_orig)
x_yaml_loads__mutmut_orig.__name__ = 'x_yaml_loads'


__all__ = [
    "yaml_dumps",
    "yaml_loads",
]


# <3 🧱🤝📜🪄
