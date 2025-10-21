# provide/foundation/config/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path

"""Centralized default values for Foundation configuration.
All defaults are defined here instead of inline in field definitions.
"""

# =================================
# Context Defaults
# =================================
DEFAULT_CONTEXT_LOG_LEVEL = "INFO"
DEFAULT_CONTEXT_PROFILE = "default"
DEFAULT_CONTEXT_DEBUG = False
DEFAULT_CONTEXT_JSON_OUTPUT = False
DEFAULT_CONTEXT_CONFIG_FILE = None
DEFAULT_CONTEXT_LOG_FILE = None
DEFAULT_CONTEXT_LOG_FORMAT = "key_value"
DEFAULT_CONTEXT_NO_COLOR = False
DEFAULT_CONTEXT_NO_EMOJI = False

# =================================
# Exit codes
# =================================
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_SIGINT = 130  # Standard exit code for SIGINT

# =================================
# Testing defaults
# =================================
DEFAULT_TEST_WAIT_TIMEOUT = 5.0
DEFAULT_TEST_PARALLEL_TIMEOUT = 10.0
DEFAULT_TEST_CHECKPOINT_TIMEOUT = 5.0

# =================================
# File/Lock defaults
# =================================
DEFAULT_FILE_LOCK_TIMEOUT = 10.0

# =================================
# File operation defaults
# =================================
DEFAULT_FILE_OP_IS_ATOMIC = False
DEFAULT_FILE_OP_IS_SAFE = True
DEFAULT_FILE_OP_HAS_BACKUP = False

# =================================
# Temporary file/directory defaults
# =================================
DEFAULT_TEMP_PREFIX = "provide_"
DEFAULT_TEMP_SUFFIX = ""
DEFAULT_TEMP_CLEANUP = True
DEFAULT_TEMP_TEXT_MODE = False

# =================================
# Directory operation defaults
# =================================
DEFAULT_DIR_MODE = 0o755
DEFAULT_DIR_PARENTS = True
DEFAULT_MISSING_OK = True

# =================================
# Atomic write defaults
# =================================
DEFAULT_ATOMIC_MODE = 0o644
DEFAULT_ATOMIC_ENCODING = "utf-8"

# =================================
# EventSet defaults
# =================================
DEFAULT_EVENT_KEY = "default"

# =================================
# Component defaults
# =================================
DEFAULT_COMPONENT_DIMENSION = "component"

# =================================
# State config defaults
# =================================
DEFAULT_STATE_CONFIG_NAME = ""

# =================================
# Tracer defaults
# =================================
DEFAULT_TRACER_OTEL_SPAN = None
DEFAULT_TRACER_ACTIVE = True
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

# =================================
# Factory functions for mutable defaults
# =================================


def default_empty_dict() -> dict[str, str]:
    """Factory for empty string dictionaries."""
    return {}


def x_path_converter__mutmut_orig(x: str | None) -> Path | None:
    """Convert string to Path or None."""
    return Path(x) if x else None


def x_path_converter__mutmut_1(x: str | None) -> Path | None:
    """Convert string to Path or None."""
    return Path(None) if x else None

x_path_converter__mutmut_mutants : ClassVar[MutantDict] = {
'x_path_converter__mutmut_1': x_path_converter__mutmut_1
}

def path_converter(*args, **kwargs):
    result = _mutmut_trampoline(x_path_converter__mutmut_orig, x_path_converter__mutmut_mutants, args, kwargs)
    return result 

path_converter.__signature__ = _mutmut_signature(x_path_converter__mutmut_orig)
x_path_converter__mutmut_orig.__name__ = 'x_path_converter'


# <3 🧱🤝⚙️🪄
