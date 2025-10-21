# provide/foundation/parsers/typed.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import types
import typing
from typing import Any, get_args, get_origin

from provide.foundation.parsers.collections import parse_dict, parse_list, parse_set, parse_tuple
from provide.foundation.parsers.primitives import parse_bool

"""Type-aware parsing utilities for converting strings to typed values.

Provides utilities for converting string values to proper Python types based on
type hints, including support for generics and parameterized types.
"""
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


def x__parse_basic_type__mutmut_orig(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_1(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is not bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_2(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(None)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_3(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is not int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_4(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(None)
    if target_type is float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_5(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is not float:
        return float(value)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_6(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(None)
    if target_type is str:
        return value
    return None  # Not a basic type


def x__parse_basic_type__mutmut_7(value: str, target_type: type) -> Any:
    """Parse basic types (bool, int, float, str)."""
    if target_type is bool:
        return parse_bool(value)
    if target_type is int:
        return int(value)
    if target_type is float:
        return float(value)
    if target_type is not str:
        return value
    return None  # Not a basic type

x__parse_basic_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_basic_type__mutmut_1': x__parse_basic_type__mutmut_1, 
    'x__parse_basic_type__mutmut_2': x__parse_basic_type__mutmut_2, 
    'x__parse_basic_type__mutmut_3': x__parse_basic_type__mutmut_3, 
    'x__parse_basic_type__mutmut_4': x__parse_basic_type__mutmut_4, 
    'x__parse_basic_type__mutmut_5': x__parse_basic_type__mutmut_5, 
    'x__parse_basic_type__mutmut_6': x__parse_basic_type__mutmut_6, 
    'x__parse_basic_type__mutmut_7': x__parse_basic_type__mutmut_7
}

def _parse_basic_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_basic_type__mutmut_orig, x__parse_basic_type__mutmut_mutants, args, kwargs)
    return result 

_parse_basic_type.__signature__ = _mutmut_signature(x__parse_basic_type__mutmut_orig)
x__parse_basic_type__mutmut_orig.__name__ = 'x__parse_basic_type'


def x__parse_list_type__mutmut_orig(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_1(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = None
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_2(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(None)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_3(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args or len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_4(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) >= 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_5(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 1:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_6(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = None
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_7(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[1]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_8(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = None
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_9(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(None)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_10(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(None, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_11(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, None) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_12(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_13(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, ) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_14(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(None) from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(value)


def x__parse_list_type__mutmut_15(value: str, target_type: type) -> list[Any]:
    """Parse list types, including parameterized lists like list[int]."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_list = parse_list(value)
        try:
            # Convert each item to the target type
            return [parse_typed_value(item, item_type) for item in str_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert list items to {item_type.__name__}: {e}") from e
    else:
        # list without type parameter, return as list[str]
        return parse_list(None)

x__parse_list_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_list_type__mutmut_1': x__parse_list_type__mutmut_1, 
    'x__parse_list_type__mutmut_2': x__parse_list_type__mutmut_2, 
    'x__parse_list_type__mutmut_3': x__parse_list_type__mutmut_3, 
    'x__parse_list_type__mutmut_4': x__parse_list_type__mutmut_4, 
    'x__parse_list_type__mutmut_5': x__parse_list_type__mutmut_5, 
    'x__parse_list_type__mutmut_6': x__parse_list_type__mutmut_6, 
    'x__parse_list_type__mutmut_7': x__parse_list_type__mutmut_7, 
    'x__parse_list_type__mutmut_8': x__parse_list_type__mutmut_8, 
    'x__parse_list_type__mutmut_9': x__parse_list_type__mutmut_9, 
    'x__parse_list_type__mutmut_10': x__parse_list_type__mutmut_10, 
    'x__parse_list_type__mutmut_11': x__parse_list_type__mutmut_11, 
    'x__parse_list_type__mutmut_12': x__parse_list_type__mutmut_12, 
    'x__parse_list_type__mutmut_13': x__parse_list_type__mutmut_13, 
    'x__parse_list_type__mutmut_14': x__parse_list_type__mutmut_14, 
    'x__parse_list_type__mutmut_15': x__parse_list_type__mutmut_15
}

def _parse_list_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_list_type__mutmut_orig, x__parse_list_type__mutmut_mutants, args, kwargs)
    return result 

_parse_list_type.__signature__ = _mutmut_signature(x__parse_list_type__mutmut_orig)
x__parse_list_type__mutmut_orig.__name__ = 'x__parse_list_type'


def x__parse_tuple_type__mutmut_orig(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_1(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = None
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_2(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(None)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_3(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args or len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_4(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) >= 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_5(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 1:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_6(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = None
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_7(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[1]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_8(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = None
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_9(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(None)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_10(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(None)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_11(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(None, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_12(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, None) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_13(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_14(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, ) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_15(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(None) from e
    return parse_tuple(value)


def x__parse_tuple_type__mutmut_16(value: str, target_type: type) -> tuple:
    """Parse parameterized tuple types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_tuple = parse_tuple(value)
        try:
            return tuple(parse_typed_value(item, item_type) for item in str_tuple)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert tuple items to {item_type.__name__}: {e}") from e
    return parse_tuple(None)

x__parse_tuple_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_tuple_type__mutmut_1': x__parse_tuple_type__mutmut_1, 
    'x__parse_tuple_type__mutmut_2': x__parse_tuple_type__mutmut_2, 
    'x__parse_tuple_type__mutmut_3': x__parse_tuple_type__mutmut_3, 
    'x__parse_tuple_type__mutmut_4': x__parse_tuple_type__mutmut_4, 
    'x__parse_tuple_type__mutmut_5': x__parse_tuple_type__mutmut_5, 
    'x__parse_tuple_type__mutmut_6': x__parse_tuple_type__mutmut_6, 
    'x__parse_tuple_type__mutmut_7': x__parse_tuple_type__mutmut_7, 
    'x__parse_tuple_type__mutmut_8': x__parse_tuple_type__mutmut_8, 
    'x__parse_tuple_type__mutmut_9': x__parse_tuple_type__mutmut_9, 
    'x__parse_tuple_type__mutmut_10': x__parse_tuple_type__mutmut_10, 
    'x__parse_tuple_type__mutmut_11': x__parse_tuple_type__mutmut_11, 
    'x__parse_tuple_type__mutmut_12': x__parse_tuple_type__mutmut_12, 
    'x__parse_tuple_type__mutmut_13': x__parse_tuple_type__mutmut_13, 
    'x__parse_tuple_type__mutmut_14': x__parse_tuple_type__mutmut_14, 
    'x__parse_tuple_type__mutmut_15': x__parse_tuple_type__mutmut_15, 
    'x__parse_tuple_type__mutmut_16': x__parse_tuple_type__mutmut_16
}

def _parse_tuple_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_tuple_type__mutmut_orig, x__parse_tuple_type__mutmut_mutants, args, kwargs)
    return result 

_parse_tuple_type.__signature__ = _mutmut_signature(x__parse_tuple_type__mutmut_orig)
x__parse_tuple_type__mutmut_orig.__name__ = 'x__parse_tuple_type'


def x__parse_set_type__mutmut_orig(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_1(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = None
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_2(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(None)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_3(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args or len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_4(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) >= 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_5(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 1:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_6(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = None
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_7(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[1]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_8(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = None
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_9(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(None)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_10(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(None, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_11(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, None) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_12(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_13(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, ) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(value)


def x__parse_set_type__mutmut_14(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(None) from e
    return parse_set(value)


def x__parse_set_type__mutmut_15(value: str, target_type: type) -> set:
    """Parse parameterized set types."""
    args = get_args(target_type)
    if args and len(args) > 0:
        item_type = args[0]
        str_set = parse_set(value)
        try:
            return {parse_typed_value(item, item_type) for item in str_set}
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert set items to {item_type.__name__}: {e}") from e
    return parse_set(None)

x__parse_set_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_set_type__mutmut_1': x__parse_set_type__mutmut_1, 
    'x__parse_set_type__mutmut_2': x__parse_set_type__mutmut_2, 
    'x__parse_set_type__mutmut_3': x__parse_set_type__mutmut_3, 
    'x__parse_set_type__mutmut_4': x__parse_set_type__mutmut_4, 
    'x__parse_set_type__mutmut_5': x__parse_set_type__mutmut_5, 
    'x__parse_set_type__mutmut_6': x__parse_set_type__mutmut_6, 
    'x__parse_set_type__mutmut_7': x__parse_set_type__mutmut_7, 
    'x__parse_set_type__mutmut_8': x__parse_set_type__mutmut_8, 
    'x__parse_set_type__mutmut_9': x__parse_set_type__mutmut_9, 
    'x__parse_set_type__mutmut_10': x__parse_set_type__mutmut_10, 
    'x__parse_set_type__mutmut_11': x__parse_set_type__mutmut_11, 
    'x__parse_set_type__mutmut_12': x__parse_set_type__mutmut_12, 
    'x__parse_set_type__mutmut_13': x__parse_set_type__mutmut_13, 
    'x__parse_set_type__mutmut_14': x__parse_set_type__mutmut_14, 
    'x__parse_set_type__mutmut_15': x__parse_set_type__mutmut_15
}

def _parse_set_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_set_type__mutmut_orig, x__parse_set_type__mutmut_mutants, args, kwargs)
    return result 

_parse_set_type.__signature__ = _mutmut_signature(x__parse_set_type__mutmut_orig)
x__parse_set_type__mutmut_orig.__name__ = 'x__parse_set_type'


def x__parse_generic_type__mutmut_orig(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_1(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = None

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_2(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(None)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_3(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is not list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_4(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(None, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_5(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, None)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_6(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_7(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, )
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_8(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is not tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_9(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(None, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_10(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, None)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_11(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_12(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, )
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_13(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is not set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_14(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(None, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_15(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, None)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_16(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_17(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, )
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_18(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is not dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_19(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(None)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_20(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is not None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_21(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is not list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_22(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(None)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_23(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is not tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_24(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(None)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_25(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is not set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_26(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(None)
        if target_type is dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_27(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is not dict:
            return parse_dict(value)

    return None  # Not a recognized generic type


def x__parse_generic_type__mutmut_28(value: str, target_type: type) -> Any:
    """Parse generic types (list, dict, tuple, set, etc.)."""
    origin = get_origin(target_type)

    if origin is list:
        return _parse_list_type(value, target_type)
    if origin is tuple:
        return _parse_tuple_type(value, target_type)
    if origin is set:
        return _parse_set_type(value, target_type)
    if origin is dict:
        return parse_dict(value)
    if origin is None:
        # Not a generic type, try direct conversion
        if target_type is list:
            return parse_list(value)
        if target_type is tuple:
            return parse_tuple(value)
        if target_type is set:
            return parse_set(value)
        if target_type is dict:
            return parse_dict(None)

    return None  # Not a recognized generic type

x__parse_generic_type__mutmut_mutants : ClassVar[MutantDict] = {
'x__parse_generic_type__mutmut_1': x__parse_generic_type__mutmut_1, 
    'x__parse_generic_type__mutmut_2': x__parse_generic_type__mutmut_2, 
    'x__parse_generic_type__mutmut_3': x__parse_generic_type__mutmut_3, 
    'x__parse_generic_type__mutmut_4': x__parse_generic_type__mutmut_4, 
    'x__parse_generic_type__mutmut_5': x__parse_generic_type__mutmut_5, 
    'x__parse_generic_type__mutmut_6': x__parse_generic_type__mutmut_6, 
    'x__parse_generic_type__mutmut_7': x__parse_generic_type__mutmut_7, 
    'x__parse_generic_type__mutmut_8': x__parse_generic_type__mutmut_8, 
    'x__parse_generic_type__mutmut_9': x__parse_generic_type__mutmut_9, 
    'x__parse_generic_type__mutmut_10': x__parse_generic_type__mutmut_10, 
    'x__parse_generic_type__mutmut_11': x__parse_generic_type__mutmut_11, 
    'x__parse_generic_type__mutmut_12': x__parse_generic_type__mutmut_12, 
    'x__parse_generic_type__mutmut_13': x__parse_generic_type__mutmut_13, 
    'x__parse_generic_type__mutmut_14': x__parse_generic_type__mutmut_14, 
    'x__parse_generic_type__mutmut_15': x__parse_generic_type__mutmut_15, 
    'x__parse_generic_type__mutmut_16': x__parse_generic_type__mutmut_16, 
    'x__parse_generic_type__mutmut_17': x__parse_generic_type__mutmut_17, 
    'x__parse_generic_type__mutmut_18': x__parse_generic_type__mutmut_18, 
    'x__parse_generic_type__mutmut_19': x__parse_generic_type__mutmut_19, 
    'x__parse_generic_type__mutmut_20': x__parse_generic_type__mutmut_20, 
    'x__parse_generic_type__mutmut_21': x__parse_generic_type__mutmut_21, 
    'x__parse_generic_type__mutmut_22': x__parse_generic_type__mutmut_22, 
    'x__parse_generic_type__mutmut_23': x__parse_generic_type__mutmut_23, 
    'x__parse_generic_type__mutmut_24': x__parse_generic_type__mutmut_24, 
    'x__parse_generic_type__mutmut_25': x__parse_generic_type__mutmut_25, 
    'x__parse_generic_type__mutmut_26': x__parse_generic_type__mutmut_26, 
    'x__parse_generic_type__mutmut_27': x__parse_generic_type__mutmut_27, 
    'x__parse_generic_type__mutmut_28': x__parse_generic_type__mutmut_28
}

def _parse_generic_type(*args, **kwargs):
    result = _mutmut_trampoline(x__parse_generic_type__mutmut_orig, x__parse_generic_type__mutmut_mutants, args, kwargs)
    return result 

_parse_generic_type.__signature__ = _mutmut_signature(x__parse_generic_type__mutmut_orig)
x__parse_generic_type__mutmut_orig.__name__ = 'x__parse_generic_type'


def x_extract_concrete_type__mutmut_orig(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_1(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = None

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_2(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if "XX | XX" in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_3(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " not in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_4(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = None
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_5(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(None)]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_6(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split("XX | XX")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_7(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = None
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_8(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part == "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_9(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "XXNoneXX"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_10(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "none"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_11(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "NONE"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_12(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = None
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_13(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[1]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_14(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = None

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_15(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "XXstrXX": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_16(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "STR": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_17(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "XXintXX": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_18(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "INT": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_19(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "XXboolXX": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_20(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "BOOL": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_21(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "XXfloatXX": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_22(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "FLOAT": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_23(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "XXlistXX": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_24(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "LIST": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_25(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "XXdictXX": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_26(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "DICT": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_27(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "XXtupleXX": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_28(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "TUPLE": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_29(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "XXsetXX": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_30(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "SET": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_31(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "XXPathXX": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_32(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_33(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "PATH": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_34(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "XXpathlib.PathXX": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_35(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_36(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "PATHLIB.PATH": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_37(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(None, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_38(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, None)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_39(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_40(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, )

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_41(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is not type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_42(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = None
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_43(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(None)
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_44(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = None

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_45(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(None)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_46(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union and (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_47(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is not typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_48(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") or isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_49(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(None, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_50(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, None) and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_51(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr("UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_52(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, ) and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_53(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "XXUnionTypeXX") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_54(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "uniontype") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_55(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UNIONTYPE") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_56(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(None, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_57(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, None):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_58(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr("__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_59(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, ):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_60(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "XX__args__XX"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_61(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__ARGS__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_62(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = None

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is not type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_63(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = None

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_64(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
    origin = get_origin(annotation)
    args = get_args(annotation)

    # Handle Union types (including Optional which is Union[T, None])
    if origin is typing.Union or (hasattr(types, "UnionType") and isinstance(annotation, types.UnionType)):
        # For Python 3.10+ union syntax (str | None)
        if hasattr(annotation, "__args__"):
            args = annotation.__args__

        # Filter out None type to get the actual type
        non_none_types = [t for t in args if t is type(None)]

        if non_none_types:
            # Return the first non-None type
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_65(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[1]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is not None:
        return annotation

    # For non-generic types, return as-is
    return annotation


def x_extract_concrete_type__mutmut_66(annotation: Any) -> type:
    """Extract concrete type from type annotation, handling unions, optionals, and string annotations.

    This function handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)
    - Generic types (list[int], dict[str, str])

    Args:
        annotation: Type annotation from function signature or attrs field

    Returns:
        Concrete type that can be used for parsing

    Examples:
        >>> extract_concrete_type(str | None)
        <class 'str'>
        >>> extract_concrete_type('str | None')
        <class 'str'>
        >>> extract_concrete_type(list[int])
        list[int]
    """
    # Handle string annotations (from __future__ import annotations)
    if isinstance(annotation, str):
        annotation = annotation.strip()

        # Handle Union types as strings (e.g., "str | None")
        if " | " in annotation:
            parts = [part.strip() for part in annotation.split(" | ")]
            non_none_parts = [part for part in parts if part != "None"]
            if non_none_parts:
                annotation = non_none_parts[0]
            else:
                return str  # Default to str if only None

        # Map string type names to actual types
        type_mapping = {
            "str": str,
            "int": int,
            "bool": bool,
            "float": float,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "Path": str,  # Path objects are handled as strings
            "pathlib.Path": str,
        }

        return type_mapping.get(annotation, str)

    # Handle None type
    if annotation is type(None):
        return str  # Default to str

    # Get origin and args for generic types
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
            return non_none_types[0]

        # If only None, default to str
        return str

    # For generic types, return as-is (e.g., list[int])
    if origin is None:
        return annotation

    # For non-generic types, return as-is
    return annotation

x_extract_concrete_type__mutmut_mutants : ClassVar[MutantDict] = {
'x_extract_concrete_type__mutmut_1': x_extract_concrete_type__mutmut_1, 
    'x_extract_concrete_type__mutmut_2': x_extract_concrete_type__mutmut_2, 
    'x_extract_concrete_type__mutmut_3': x_extract_concrete_type__mutmut_3, 
    'x_extract_concrete_type__mutmut_4': x_extract_concrete_type__mutmut_4, 
    'x_extract_concrete_type__mutmut_5': x_extract_concrete_type__mutmut_5, 
    'x_extract_concrete_type__mutmut_6': x_extract_concrete_type__mutmut_6, 
    'x_extract_concrete_type__mutmut_7': x_extract_concrete_type__mutmut_7, 
    'x_extract_concrete_type__mutmut_8': x_extract_concrete_type__mutmut_8, 
    'x_extract_concrete_type__mutmut_9': x_extract_concrete_type__mutmut_9, 
    'x_extract_concrete_type__mutmut_10': x_extract_concrete_type__mutmut_10, 
    'x_extract_concrete_type__mutmut_11': x_extract_concrete_type__mutmut_11, 
    'x_extract_concrete_type__mutmut_12': x_extract_concrete_type__mutmut_12, 
    'x_extract_concrete_type__mutmut_13': x_extract_concrete_type__mutmut_13, 
    'x_extract_concrete_type__mutmut_14': x_extract_concrete_type__mutmut_14, 
    'x_extract_concrete_type__mutmut_15': x_extract_concrete_type__mutmut_15, 
    'x_extract_concrete_type__mutmut_16': x_extract_concrete_type__mutmut_16, 
    'x_extract_concrete_type__mutmut_17': x_extract_concrete_type__mutmut_17, 
    'x_extract_concrete_type__mutmut_18': x_extract_concrete_type__mutmut_18, 
    'x_extract_concrete_type__mutmut_19': x_extract_concrete_type__mutmut_19, 
    'x_extract_concrete_type__mutmut_20': x_extract_concrete_type__mutmut_20, 
    'x_extract_concrete_type__mutmut_21': x_extract_concrete_type__mutmut_21, 
    'x_extract_concrete_type__mutmut_22': x_extract_concrete_type__mutmut_22, 
    'x_extract_concrete_type__mutmut_23': x_extract_concrete_type__mutmut_23, 
    'x_extract_concrete_type__mutmut_24': x_extract_concrete_type__mutmut_24, 
    'x_extract_concrete_type__mutmut_25': x_extract_concrete_type__mutmut_25, 
    'x_extract_concrete_type__mutmut_26': x_extract_concrete_type__mutmut_26, 
    'x_extract_concrete_type__mutmut_27': x_extract_concrete_type__mutmut_27, 
    'x_extract_concrete_type__mutmut_28': x_extract_concrete_type__mutmut_28, 
    'x_extract_concrete_type__mutmut_29': x_extract_concrete_type__mutmut_29, 
    'x_extract_concrete_type__mutmut_30': x_extract_concrete_type__mutmut_30, 
    'x_extract_concrete_type__mutmut_31': x_extract_concrete_type__mutmut_31, 
    'x_extract_concrete_type__mutmut_32': x_extract_concrete_type__mutmut_32, 
    'x_extract_concrete_type__mutmut_33': x_extract_concrete_type__mutmut_33, 
    'x_extract_concrete_type__mutmut_34': x_extract_concrete_type__mutmut_34, 
    'x_extract_concrete_type__mutmut_35': x_extract_concrete_type__mutmut_35, 
    'x_extract_concrete_type__mutmut_36': x_extract_concrete_type__mutmut_36, 
    'x_extract_concrete_type__mutmut_37': x_extract_concrete_type__mutmut_37, 
    'x_extract_concrete_type__mutmut_38': x_extract_concrete_type__mutmut_38, 
    'x_extract_concrete_type__mutmut_39': x_extract_concrete_type__mutmut_39, 
    'x_extract_concrete_type__mutmut_40': x_extract_concrete_type__mutmut_40, 
    'x_extract_concrete_type__mutmut_41': x_extract_concrete_type__mutmut_41, 
    'x_extract_concrete_type__mutmut_42': x_extract_concrete_type__mutmut_42, 
    'x_extract_concrete_type__mutmut_43': x_extract_concrete_type__mutmut_43, 
    'x_extract_concrete_type__mutmut_44': x_extract_concrete_type__mutmut_44, 
    'x_extract_concrete_type__mutmut_45': x_extract_concrete_type__mutmut_45, 
    'x_extract_concrete_type__mutmut_46': x_extract_concrete_type__mutmut_46, 
    'x_extract_concrete_type__mutmut_47': x_extract_concrete_type__mutmut_47, 
    'x_extract_concrete_type__mutmut_48': x_extract_concrete_type__mutmut_48, 
    'x_extract_concrete_type__mutmut_49': x_extract_concrete_type__mutmut_49, 
    'x_extract_concrete_type__mutmut_50': x_extract_concrete_type__mutmut_50, 
    'x_extract_concrete_type__mutmut_51': x_extract_concrete_type__mutmut_51, 
    'x_extract_concrete_type__mutmut_52': x_extract_concrete_type__mutmut_52, 
    'x_extract_concrete_type__mutmut_53': x_extract_concrete_type__mutmut_53, 
    'x_extract_concrete_type__mutmut_54': x_extract_concrete_type__mutmut_54, 
    'x_extract_concrete_type__mutmut_55': x_extract_concrete_type__mutmut_55, 
    'x_extract_concrete_type__mutmut_56': x_extract_concrete_type__mutmut_56, 
    'x_extract_concrete_type__mutmut_57': x_extract_concrete_type__mutmut_57, 
    'x_extract_concrete_type__mutmut_58': x_extract_concrete_type__mutmut_58, 
    'x_extract_concrete_type__mutmut_59': x_extract_concrete_type__mutmut_59, 
    'x_extract_concrete_type__mutmut_60': x_extract_concrete_type__mutmut_60, 
    'x_extract_concrete_type__mutmut_61': x_extract_concrete_type__mutmut_61, 
    'x_extract_concrete_type__mutmut_62': x_extract_concrete_type__mutmut_62, 
    'x_extract_concrete_type__mutmut_63': x_extract_concrete_type__mutmut_63, 
    'x_extract_concrete_type__mutmut_64': x_extract_concrete_type__mutmut_64, 
    'x_extract_concrete_type__mutmut_65': x_extract_concrete_type__mutmut_65, 
    'x_extract_concrete_type__mutmut_66': x_extract_concrete_type__mutmut_66
}

def extract_concrete_type(*args, **kwargs):
    result = _mutmut_trampoline(x_extract_concrete_type__mutmut_orig, x_extract_concrete_type__mutmut_mutants, args, kwargs)
    return result 

extract_concrete_type.__signature__ = _mutmut_signature(x_extract_concrete_type__mutmut_orig)
x_extract_concrete_type__mutmut_orig.__name__ = 'x_extract_concrete_type'


def x_parse_typed_value__mutmut_orig(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_1(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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
    if value is not None:
        return None

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_2(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = None
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_3(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(None, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_4(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, None)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_5(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_6(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, )
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_7(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None and target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_8(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_9(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type not in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_10(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = None
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_11(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(None, target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_12(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, None)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_13(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(target_type)
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_14(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, )
    if result is not None:
        return result

    # Default to string
    return value


def x_parse_typed_value__mutmut_15(value: str, target_type: type) -> Any:
    """Parse a string value to a specific type.

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

    # Try basic types first
    result = _parse_basic_type(value, target_type)
    if result is not None or target_type in (bool, int, float, str):
        return result

    # Try generic types
    result = _parse_generic_type(value, target_type)
    if result is None:
        return result

    # Default to string
    return value

x_parse_typed_value__mutmut_mutants : ClassVar[MutantDict] = {
'x_parse_typed_value__mutmut_1': x_parse_typed_value__mutmut_1, 
    'x_parse_typed_value__mutmut_2': x_parse_typed_value__mutmut_2, 
    'x_parse_typed_value__mutmut_3': x_parse_typed_value__mutmut_3, 
    'x_parse_typed_value__mutmut_4': x_parse_typed_value__mutmut_4, 
    'x_parse_typed_value__mutmut_5': x_parse_typed_value__mutmut_5, 
    'x_parse_typed_value__mutmut_6': x_parse_typed_value__mutmut_6, 
    'x_parse_typed_value__mutmut_7': x_parse_typed_value__mutmut_7, 
    'x_parse_typed_value__mutmut_8': x_parse_typed_value__mutmut_8, 
    'x_parse_typed_value__mutmut_9': x_parse_typed_value__mutmut_9, 
    'x_parse_typed_value__mutmut_10': x_parse_typed_value__mutmut_10, 
    'x_parse_typed_value__mutmut_11': x_parse_typed_value__mutmut_11, 
    'x_parse_typed_value__mutmut_12': x_parse_typed_value__mutmut_12, 
    'x_parse_typed_value__mutmut_13': x_parse_typed_value__mutmut_13, 
    'x_parse_typed_value__mutmut_14': x_parse_typed_value__mutmut_14, 
    'x_parse_typed_value__mutmut_15': x_parse_typed_value__mutmut_15
}

def parse_typed_value(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_typed_value__mutmut_orig, x_parse_typed_value__mutmut_mutants, args, kwargs)
    return result 

parse_typed_value.__signature__ = _mutmut_signature(x_parse_typed_value__mutmut_orig)
x_parse_typed_value__mutmut_orig.__name__ = 'x_parse_typed_value'


__all__ = [
    "_parse_basic_type",
    "_parse_generic_type",
    "_parse_list_type",
    "_parse_set_type",
    "_parse_tuple_type",
    "extract_concrete_type",
    "parse_typed_value",
]


# <3 🧱🤝🧩🪄
