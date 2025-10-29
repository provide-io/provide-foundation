# provide/foundation/formatting/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.formatting.case import (
    to_camel_case,
    to_kebab_case,
    to_snake_case,
)
from provide.foundation.formatting.grouping import format_grouped
from provide.foundation.formatting.numbers import (
    format_duration,
    format_number,
    format_percentage,
    format_size,
)
from provide.foundation.formatting.tables import format_table
from provide.foundation.formatting.text import (
    indent,
    pluralize,
    strip_ansi,
    truncate,
    wrap_text,
)

"""Formatting utilities for provide.foundation.

Comprehensive text, numeric, and data formatting utilities for consistent
output across applications.
"""

__all__ = [
    # Numeric formatting
    "format_duration",
    # String grouping
    "format_grouped",
    "format_number",
    "format_percentage",
    "format_size",
    # Table formatting
    "format_table",
    # Text manipulation
    "indent",
    "pluralize",
    "strip_ansi",
    # Case conversion
    "to_camel_case",
    "to_kebab_case",
    "to_snake_case",
    "truncate",
    "wrap_text",
]
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


# <3 🧱🤝🎨🪄
