# provide/foundation/hub/type_mapping.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Type system and Click type mapping utilities."""

from __future__ import annotations

from typing import Any

from provide.foundation.parsers import extract_concrete_type
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


def x_extract_click_type__mutmut_orig(annotation: Any) -> type:
    """Extract a Click-compatible type from a Python type annotation.

    This is a wrapper around extract_concrete_type() that ensures
    compatibility with Click's type system.

    Handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)

    Args:
        annotation: Type annotation from function signature

    Returns:
        A type that Click can understand

    """
    return extract_concrete_type(annotation)


def x_extract_click_type__mutmut_1(annotation: Any) -> type:
    """Extract a Click-compatible type from a Python type annotation.

    This is a wrapper around extract_concrete_type() that ensures
    compatibility with Click's type system.

    Handles:
    - Union types (str | None, Union[str, None])
    - Optional types (str | None)
    - Regular types (str, int, bool)
    - String annotations (from __future__ import annotations)

    Args:
        annotation: Type annotation from function signature

    Returns:
        A type that Click can understand

    """
    return extract_concrete_type(None)


x_extract_click_type__mutmut_mutants: ClassVar[MutantDict] = {
    "x_extract_click_type__mutmut_1": x_extract_click_type__mutmut_1
}


def extract_click_type(*args, **kwargs):
    result = _mutmut_trampoline(
        x_extract_click_type__mutmut_orig, x_extract_click_type__mutmut_mutants, args, kwargs
    )
    return result


extract_click_type.__signature__ = _mutmut_signature(x_extract_click_type__mutmut_orig)
x_extract_click_type__mutmut_orig.__name__ = "x_extract_click_type"


__all__ = ["extract_click_type"]


# <3 🧱🤝🌐🪄
