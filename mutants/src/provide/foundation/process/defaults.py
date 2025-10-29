# provide/foundation/process/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Process defaults for Foundation configuration."""

# =================================
# Process Execution Defaults
# =================================
DEFAULT_PROCESS_READLINE_TIMEOUT = 2.0
DEFAULT_PROCESS_READCHAR_TIMEOUT = 1.0
DEFAULT_PROCESS_TERMINATE_TIMEOUT = 7.0
DEFAULT_PROCESS_WAIT_TIMEOUT = 10.0

# =================================
# Shell Safety Defaults
# =================================
DEFAULT_SHELL_ALLOW_FEATURES = False

# =================================
# Environment Scrubbing Defaults
# =================================
DEFAULT_ENV_SCRUBBING_ENABLED = True

__all__ = [
    "DEFAULT_ENV_SCRUBBING_ENABLED",
    "DEFAULT_PROCESS_READCHAR_TIMEOUT",
    "DEFAULT_PROCESS_READLINE_TIMEOUT",
    "DEFAULT_PROCESS_TERMINATE_TIMEOUT",
    "DEFAULT_PROCESS_WAIT_TIMEOUT",
    "DEFAULT_SHELL_ALLOW_FEATURES",
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


# <3 🧱🤝🏃🪄
