# provide/foundation/parsers/collections.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Collection parsing functions for lists, dicts, tuples, and sets.

Handles parsing of collection types from string values with customizable
separators and formatting options.
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os

    mutant_under_test = os.environ["MUTANT_UNDER_TEST"]
    if mutant_under_test == "fail":
        from mutmut.__main__ import MutmutProgrammaticFailException

        raise MutmutProgrammaticFailException("Failed programmatically")
    elif mutant_under_test == "stats":
        from mutmut.__main__ import record_trampoline_hit

        record_trampoline_hit(orig.__module__ + "." + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + "." + orig.__name__ + "__mutmut_"
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition(".")[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_parse_list__mutmut_orig(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_1(
    value: str | list[str],
    separator: str = "XX,XX",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_2(
    value: str | list[str],
    separator: str = ",",
    strip: bool = False,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_3(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if value:
        return []

    items = value.split(separator)

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_4(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = None

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_5(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(None)

    if strip:
        items = [item.strip() for item in items]

    return items


def x_parse_list__mutmut_6(
    value: str | list[str],
    separator: str = ",",
    strip: bool = True,
) -> list[str]:
    """Parse a list from a string.

    Args:
        value: String or list to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        List of strings

    """
    if isinstance(value, list):
        return value

    if not value:
        return []

    items = value.split(separator)

    if strip:
        items = None

    return items


x_parse_list__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_list__mutmut_1": x_parse_list__mutmut_1,
    "x_parse_list__mutmut_2": x_parse_list__mutmut_2,
    "x_parse_list__mutmut_3": x_parse_list__mutmut_3,
    "x_parse_list__mutmut_4": x_parse_list__mutmut_4,
    "x_parse_list__mutmut_5": x_parse_list__mutmut_5,
    "x_parse_list__mutmut_6": x_parse_list__mutmut_6,
}


def parse_list(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_list__mutmut_orig, x_parse_list__mutmut_mutants, args, kwargs)
    return result


parse_list.__signature__ = _mutmut_signature(x_parse_list__mutmut_orig)
x_parse_list__mutmut_orig.__name__ = "x_parse_list"


def x_parse_tuple__mutmut_orig(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_1(
    value: str | tuple[str, ...],
    separator: str = "XX,XX",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_2(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = False,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_3(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = None
    return tuple(items)


def x_parse_tuple__mutmut_4(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(None, separator=separator, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_5(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=None, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_6(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=None)
    return tuple(items)


def x_parse_tuple__mutmut_7(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(separator=separator, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_8(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, strip=strip)
    return tuple(items)


def x_parse_tuple__mutmut_9(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(
        value,
        separator=separator,
    )
    return tuple(items)


def x_parse_tuple__mutmut_10(
    value: str | tuple[str, ...],
    separator: str = ",",
    strip: bool = True,
) -> tuple[str, ...]:
    """Parse a tuple from a string.

    Args:
        value: String or tuple to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Tuple of strings

    """
    if isinstance(value, tuple):
        return value

    # Reuse list parsing logic
    items = parse_list(value, separator=separator, strip=strip)
    return tuple(None)


x_parse_tuple__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_tuple__mutmut_1": x_parse_tuple__mutmut_1,
    "x_parse_tuple__mutmut_2": x_parse_tuple__mutmut_2,
    "x_parse_tuple__mutmut_3": x_parse_tuple__mutmut_3,
    "x_parse_tuple__mutmut_4": x_parse_tuple__mutmut_4,
    "x_parse_tuple__mutmut_5": x_parse_tuple__mutmut_5,
    "x_parse_tuple__mutmut_6": x_parse_tuple__mutmut_6,
    "x_parse_tuple__mutmut_7": x_parse_tuple__mutmut_7,
    "x_parse_tuple__mutmut_8": x_parse_tuple__mutmut_8,
    "x_parse_tuple__mutmut_9": x_parse_tuple__mutmut_9,
    "x_parse_tuple__mutmut_10": x_parse_tuple__mutmut_10,
}


def parse_tuple(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_tuple__mutmut_orig, x_parse_tuple__mutmut_mutants, args, kwargs)
    return result


parse_tuple.__signature__ = _mutmut_signature(x_parse_tuple__mutmut_orig)
x_parse_tuple__mutmut_orig.__name__ = "x_parse_tuple"


def x_parse_set__mutmut_orig(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=strip)
    return set(items)


def x_parse_set__mutmut_1(
    value: str | set[str],
    separator: str = "XX,XX",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=strip)
    return set(items)


def x_parse_set__mutmut_2(
    value: str | set[str],
    separator: str = ",",
    strip: bool = False,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=strip)
    return set(items)


def x_parse_set__mutmut_3(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = None
    return set(items)


def x_parse_set__mutmut_4(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(None, separator=separator, strip=strip)
    return set(items)


def x_parse_set__mutmut_5(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=None, strip=strip)
    return set(items)


def x_parse_set__mutmut_6(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=None)
    return set(items)


def x_parse_set__mutmut_7(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(separator=separator, strip=strip)
    return set(items)


def x_parse_set__mutmut_8(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, strip=strip)
    return set(items)


def x_parse_set__mutmut_9(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(
        value,
        separator=separator,
    )
    return set(items)


def x_parse_set__mutmut_10(
    value: str | set[str],
    separator: str = ",",
    strip: bool = True,
) -> set[str]:
    """Parse a set from a string.

    Args:
        value: String or set to parse
        separator: Separator character
        strip: Whether to strip whitespace from items

    Returns:
        Set of strings (duplicates removed)

    """
    if isinstance(value, set):
        return value

    # Reuse list parsing logic, then convert to set
    items = parse_list(value, separator=separator, strip=strip)
    return set(None)


x_parse_set__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_set__mutmut_1": x_parse_set__mutmut_1,
    "x_parse_set__mutmut_2": x_parse_set__mutmut_2,
    "x_parse_set__mutmut_3": x_parse_set__mutmut_3,
    "x_parse_set__mutmut_4": x_parse_set__mutmut_4,
    "x_parse_set__mutmut_5": x_parse_set__mutmut_5,
    "x_parse_set__mutmut_6": x_parse_set__mutmut_6,
    "x_parse_set__mutmut_7": x_parse_set__mutmut_7,
    "x_parse_set__mutmut_8": x_parse_set__mutmut_8,
    "x_parse_set__mutmut_9": x_parse_set__mutmut_9,
    "x_parse_set__mutmut_10": x_parse_set__mutmut_10,
}


def parse_set(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_set__mutmut_orig, x_parse_set__mutmut_mutants, args, kwargs)
    return result


parse_set.__signature__ = _mutmut_signature(x_parse_set__mutmut_orig)
x_parse_set__mutmut_orig.__name__ = "x_parse_set"


def x_parse_dict__mutmut_orig(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_1(
    value: str | dict[str, str],
    item_separator: str = "XX,XX",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_2(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "XX=XX",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_3(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = False,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_4(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_5(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = None
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_6(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = None

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_7(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(None)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_8(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_9(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            break

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_10(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_11(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(None)

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_12(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = None

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_13(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(None, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_14(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, None)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_15(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_16(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(
            key_separator,
        )

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_17(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.rsplit(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_18(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 2)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_19(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = None
            val = val.strip()

        result[key] = val

    return result


def x_parse_dict__mutmut_20(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = None

        result[key] = val

    return result


def x_parse_dict__mutmut_21(
    value: str | dict[str, str],
    item_separator: str = ",",
    key_separator: str = "=",
    strip: bool = True,
) -> dict[str, str]:
    """Parse a dictionary from a string.

    Format: "key1=value1,key2=value2"

    Args:
        value: String or dict to parse
        item_separator: Separator between items
        key_separator: Separator between key and value
        strip: Whether to strip whitespace

    Returns:
        Dictionary of string keys and values

    Raises:
        ValueError: If format is invalid

    """
    if isinstance(value, dict):
        return value

    if not value:
        return {}

    result = {}
    items = value.split(item_separator)

    for item in items:
        if not item:
            continue

        if key_separator not in item:
            raise ValueError(f"Invalid dict format: '{item}' missing '{key_separator}'")

        key, val = item.split(key_separator, 1)

        if strip:
            key = key.strip()
            val = val.strip()

        result[key] = None

    return result


x_parse_dict__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_dict__mutmut_1": x_parse_dict__mutmut_1,
    "x_parse_dict__mutmut_2": x_parse_dict__mutmut_2,
    "x_parse_dict__mutmut_3": x_parse_dict__mutmut_3,
    "x_parse_dict__mutmut_4": x_parse_dict__mutmut_4,
    "x_parse_dict__mutmut_5": x_parse_dict__mutmut_5,
    "x_parse_dict__mutmut_6": x_parse_dict__mutmut_6,
    "x_parse_dict__mutmut_7": x_parse_dict__mutmut_7,
    "x_parse_dict__mutmut_8": x_parse_dict__mutmut_8,
    "x_parse_dict__mutmut_9": x_parse_dict__mutmut_9,
    "x_parse_dict__mutmut_10": x_parse_dict__mutmut_10,
    "x_parse_dict__mutmut_11": x_parse_dict__mutmut_11,
    "x_parse_dict__mutmut_12": x_parse_dict__mutmut_12,
    "x_parse_dict__mutmut_13": x_parse_dict__mutmut_13,
    "x_parse_dict__mutmut_14": x_parse_dict__mutmut_14,
    "x_parse_dict__mutmut_15": x_parse_dict__mutmut_15,
    "x_parse_dict__mutmut_16": x_parse_dict__mutmut_16,
    "x_parse_dict__mutmut_17": x_parse_dict__mutmut_17,
    "x_parse_dict__mutmut_18": x_parse_dict__mutmut_18,
    "x_parse_dict__mutmut_19": x_parse_dict__mutmut_19,
    "x_parse_dict__mutmut_20": x_parse_dict__mutmut_20,
    "x_parse_dict__mutmut_21": x_parse_dict__mutmut_21,
}


def parse_dict(*args, **kwargs):
    result = _mutmut_trampoline(x_parse_dict__mutmut_orig, x_parse_dict__mutmut_mutants, args, kwargs)
    return result


parse_dict.__signature__ = _mutmut_signature(x_parse_dict__mutmut_orig)
x_parse_dict__mutmut_orig.__name__ = "x_parse_dict"


def x_parse_comma_list__mutmut_orig(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value or not value.strip():
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def x_parse_comma_list__mutmut_1(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value and not value.strip():
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def x_parse_comma_list__mutmut_2(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if value or not value.strip():
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def x_parse_comma_list__mutmut_3(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value or value.strip():
        return []

    return [item.strip() for item in value.split(",") if item.strip()]


def x_parse_comma_list__mutmut_4(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value or not value.strip():
        return []

    return [item.strip() for item in value.split(None) if item.strip()]


def x_parse_comma_list__mutmut_5(value: str) -> list[str]:
    """Parse comma-separated list of strings.

    Args:
        value: Comma-separated string

    Returns:
        List of trimmed non-empty strings

    """
    if not value or not value.strip():
        return []

    return [item.strip() for item in value.split("XX,XX") if item.strip()]


x_parse_comma_list__mutmut_mutants: ClassVar[MutantDict] = {
    "x_parse_comma_list__mutmut_1": x_parse_comma_list__mutmut_1,
    "x_parse_comma_list__mutmut_2": x_parse_comma_list__mutmut_2,
    "x_parse_comma_list__mutmut_3": x_parse_comma_list__mutmut_3,
    "x_parse_comma_list__mutmut_4": x_parse_comma_list__mutmut_4,
    "x_parse_comma_list__mutmut_5": x_parse_comma_list__mutmut_5,
}


def parse_comma_list(*args, **kwargs):
    result = _mutmut_trampoline(
        x_parse_comma_list__mutmut_orig, x_parse_comma_list__mutmut_mutants, args, kwargs
    )
    return result


parse_comma_list.__signature__ = _mutmut_signature(x_parse_comma_list__mutmut_orig)
x_parse_comma_list__mutmut_orig.__name__ = "x_parse_comma_list"


__all__ = [
    "parse_comma_list",
    "parse_dict",
    "parse_list",
    "parse_set",
    "parse_tuple",
]


# <3 🧱🤝🧩🪄
