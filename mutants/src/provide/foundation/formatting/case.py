# provide/foundation/formatting/case.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Case conversion utilities.

Provides utilities for converting between different text case formats
like snake_case, kebab-case, and camelCase.
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


def x_to_snake_case__mutmut_orig(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_1(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = None

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_2(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace(None, "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_3(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", None)

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_4(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_5(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace(
        "-",
    )

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_6(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("XX-XX", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_7(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "XX_XX")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_8(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = None

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_9(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(None, r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_10(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", None, text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_11(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", None)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_12(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_13(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_14(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1_\2",
    )

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_15(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"XX([a-z0-9])([A-Z])XX", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_16(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([a-z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_17(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([A-Z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_18(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"XX\1_\2XX", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_19(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_20(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_snake_case__mutmut_21(text: str) -> str:
    """Convert text to snake_case.

    Args:
        text: Text to convert

    Returns:
        snake_case text

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("some-kebab-case")
        'some_kebab_case'

    """
    import re

    # Replace hyphens with underscores
    text = text.replace("-", "_")

    # Insert underscore before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)

    # Convert to lowercase
    return text.upper()


x_to_snake_case__mutmut_mutants: ClassVar[MutantDict] = {
    "x_to_snake_case__mutmut_1": x_to_snake_case__mutmut_1,
    "x_to_snake_case__mutmut_2": x_to_snake_case__mutmut_2,
    "x_to_snake_case__mutmut_3": x_to_snake_case__mutmut_3,
    "x_to_snake_case__mutmut_4": x_to_snake_case__mutmut_4,
    "x_to_snake_case__mutmut_5": x_to_snake_case__mutmut_5,
    "x_to_snake_case__mutmut_6": x_to_snake_case__mutmut_6,
    "x_to_snake_case__mutmut_7": x_to_snake_case__mutmut_7,
    "x_to_snake_case__mutmut_8": x_to_snake_case__mutmut_8,
    "x_to_snake_case__mutmut_9": x_to_snake_case__mutmut_9,
    "x_to_snake_case__mutmut_10": x_to_snake_case__mutmut_10,
    "x_to_snake_case__mutmut_11": x_to_snake_case__mutmut_11,
    "x_to_snake_case__mutmut_12": x_to_snake_case__mutmut_12,
    "x_to_snake_case__mutmut_13": x_to_snake_case__mutmut_13,
    "x_to_snake_case__mutmut_14": x_to_snake_case__mutmut_14,
    "x_to_snake_case__mutmut_15": x_to_snake_case__mutmut_15,
    "x_to_snake_case__mutmut_16": x_to_snake_case__mutmut_16,
    "x_to_snake_case__mutmut_17": x_to_snake_case__mutmut_17,
    "x_to_snake_case__mutmut_18": x_to_snake_case__mutmut_18,
    "x_to_snake_case__mutmut_19": x_to_snake_case__mutmut_19,
    "x_to_snake_case__mutmut_20": x_to_snake_case__mutmut_20,
    "x_to_snake_case__mutmut_21": x_to_snake_case__mutmut_21,
}


def to_snake_case(*args, **kwargs):
    result = _mutmut_trampoline(x_to_snake_case__mutmut_orig, x_to_snake_case__mutmut_mutants, args, kwargs)
    return result


to_snake_case.__signature__ = _mutmut_signature(x_to_snake_case__mutmut_orig)
x_to_snake_case__mutmut_orig.__name__ = "x_to_snake_case"


def x_to_kebab_case__mutmut_orig(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_1(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = None

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_2(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace(None, "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_3(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", None)

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_4(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_5(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace(
        "_",
    )

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_6(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("XX_XX", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_7(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "XX-XX")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_8(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = None

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_9(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(None, r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_10(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", None, text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_11(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", None)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_12(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_13(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_14(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1-\2",
    )

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_15(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"XX([a-z0-9])([A-Z])XX", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_16(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([a-z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_17(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([A-Z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_18(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"XX\1-\2XX", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_19(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_20(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.lower()


def x_to_kebab_case__mutmut_21(text: str) -> str:
    """Convert text to kebab-case.

    Args:
        text: Text to convert

    Returns:
        kebab-case text

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("some_snake_case")
        'some-snake-case'

    """
    import re

    # Replace underscores with hyphens
    text = text.replace("_", "-")

    # Insert hyphen before uppercase letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)

    # Convert to lowercase
    return text.upper()


x_to_kebab_case__mutmut_mutants: ClassVar[MutantDict] = {
    "x_to_kebab_case__mutmut_1": x_to_kebab_case__mutmut_1,
    "x_to_kebab_case__mutmut_2": x_to_kebab_case__mutmut_2,
    "x_to_kebab_case__mutmut_3": x_to_kebab_case__mutmut_3,
    "x_to_kebab_case__mutmut_4": x_to_kebab_case__mutmut_4,
    "x_to_kebab_case__mutmut_5": x_to_kebab_case__mutmut_5,
    "x_to_kebab_case__mutmut_6": x_to_kebab_case__mutmut_6,
    "x_to_kebab_case__mutmut_7": x_to_kebab_case__mutmut_7,
    "x_to_kebab_case__mutmut_8": x_to_kebab_case__mutmut_8,
    "x_to_kebab_case__mutmut_9": x_to_kebab_case__mutmut_9,
    "x_to_kebab_case__mutmut_10": x_to_kebab_case__mutmut_10,
    "x_to_kebab_case__mutmut_11": x_to_kebab_case__mutmut_11,
    "x_to_kebab_case__mutmut_12": x_to_kebab_case__mutmut_12,
    "x_to_kebab_case__mutmut_13": x_to_kebab_case__mutmut_13,
    "x_to_kebab_case__mutmut_14": x_to_kebab_case__mutmut_14,
    "x_to_kebab_case__mutmut_15": x_to_kebab_case__mutmut_15,
    "x_to_kebab_case__mutmut_16": x_to_kebab_case__mutmut_16,
    "x_to_kebab_case__mutmut_17": x_to_kebab_case__mutmut_17,
    "x_to_kebab_case__mutmut_18": x_to_kebab_case__mutmut_18,
    "x_to_kebab_case__mutmut_19": x_to_kebab_case__mutmut_19,
    "x_to_kebab_case__mutmut_20": x_to_kebab_case__mutmut_20,
    "x_to_kebab_case__mutmut_21": x_to_kebab_case__mutmut_21,
}


def to_kebab_case(*args, **kwargs):
    result = _mutmut_trampoline(x_to_kebab_case__mutmut_orig, x_to_kebab_case__mutmut_mutants, args, kwargs)
    return result


to_kebab_case.__signature__ = _mutmut_signature(x_to_kebab_case__mutmut_orig)
x_to_kebab_case__mutmut_orig.__name__ = "x_to_kebab_case"


def x_to_camel_case__mutmut_orig(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_1(text: str, upper_first: bool = True) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_2(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = None

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_3(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(None, text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_4(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", None)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_5(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_6(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(
        r"[-_\s]+",
    )

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_7(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.rsplit(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_8(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"XX[-_\s]+XX", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_9(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_10(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_11(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_12(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = None
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_13(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(None):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_14(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 or not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_15(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i != 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_16(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 1 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_17(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_18(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(None)
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_19(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.upper())
        else:
            result.append(part.capitalize())

    return "".join(result)


def x_to_camel_case__mutmut_20(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(None)

    return "".join(result)


def x_to_camel_case__mutmut_21(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "".join(None)


def x_to_camel_case__mutmut_22(text: str, upper_first: bool = False) -> str:
    """Convert text to camelCase or PascalCase.

    Args:
        text: Text to convert
        upper_first: Use PascalCase instead of camelCase

    Returns:
        camelCase or PascalCase text

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("hello-world", upper_first=True)
        'HelloWorld'

    """
    import re

    # Split on underscores, hyphens, and spaces
    parts = re.split(r"[-_\s]+", text)

    if not parts:
        return text

    # Capitalize each part except possibly the first
    result = []
    for i, part in enumerate(parts):
        if i == 0 and not upper_first:
            result.append(part.lower())
        else:
            result.append(part.capitalize())

    return "XXXX".join(result)


x_to_camel_case__mutmut_mutants: ClassVar[MutantDict] = {
    "x_to_camel_case__mutmut_1": x_to_camel_case__mutmut_1,
    "x_to_camel_case__mutmut_2": x_to_camel_case__mutmut_2,
    "x_to_camel_case__mutmut_3": x_to_camel_case__mutmut_3,
    "x_to_camel_case__mutmut_4": x_to_camel_case__mutmut_4,
    "x_to_camel_case__mutmut_5": x_to_camel_case__mutmut_5,
    "x_to_camel_case__mutmut_6": x_to_camel_case__mutmut_6,
    "x_to_camel_case__mutmut_7": x_to_camel_case__mutmut_7,
    "x_to_camel_case__mutmut_8": x_to_camel_case__mutmut_8,
    "x_to_camel_case__mutmut_9": x_to_camel_case__mutmut_9,
    "x_to_camel_case__mutmut_10": x_to_camel_case__mutmut_10,
    "x_to_camel_case__mutmut_11": x_to_camel_case__mutmut_11,
    "x_to_camel_case__mutmut_12": x_to_camel_case__mutmut_12,
    "x_to_camel_case__mutmut_13": x_to_camel_case__mutmut_13,
    "x_to_camel_case__mutmut_14": x_to_camel_case__mutmut_14,
    "x_to_camel_case__mutmut_15": x_to_camel_case__mutmut_15,
    "x_to_camel_case__mutmut_16": x_to_camel_case__mutmut_16,
    "x_to_camel_case__mutmut_17": x_to_camel_case__mutmut_17,
    "x_to_camel_case__mutmut_18": x_to_camel_case__mutmut_18,
    "x_to_camel_case__mutmut_19": x_to_camel_case__mutmut_19,
    "x_to_camel_case__mutmut_20": x_to_camel_case__mutmut_20,
    "x_to_camel_case__mutmut_21": x_to_camel_case__mutmut_21,
    "x_to_camel_case__mutmut_22": x_to_camel_case__mutmut_22,
}


def to_camel_case(*args, **kwargs):
    result = _mutmut_trampoline(x_to_camel_case__mutmut_orig, x_to_camel_case__mutmut_mutants, args, kwargs)
    return result


to_camel_case.__signature__ = _mutmut_signature(x_to_camel_case__mutmut_orig)
x_to_camel_case__mutmut_orig.__name__ = "x_to_camel_case"


__all__ = [
    "to_camel_case",
    "to_kebab_case",
    "to_snake_case",
]


# <3 🧱🤝🎨🪄
