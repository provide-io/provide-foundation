# provide/foundation/hub/categories.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Component category definitions for Foundation Hub.

This module contains only the ComponentCategory enum to avoid circular imports.
It can be safely imported by any other hub module.
"""

from __future__ import annotations

from enum import Enum
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


class ComponentCategory(Enum):
    """Predefined component categories for Foundation.

    These are the standard dimension values used internally by Foundation.
    External components can still use custom string dimensions for compatibility.
    """

    # Core categories
    COMMAND = "command"
    COMPONENT = "component"

    # Configuration and data sources
    CONFIG_SOURCE = "config_source"
    CONFIG_SCHEMA = "config_schema"

    # Processing pipeline
    PROCESSOR = "processor"
    ERROR_HANDLER = "error_handler"
    FORMATTER = "formatter"
    FILTER = "filter"

    # Transport layer
    TRANSPORT = "transport"
    TRANSPORT_MIDDLEWARE = "transport.middleware"
    TRANSPORT_AUTH = "transport.auth"
    TRANSPORT_CACHE = "transport.cache"

    # Event system
    EVENT_SET = "eventset"


__all__ = ["ComponentCategory"]


# <3 🧱🤝🌐🪄
