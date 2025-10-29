# provide/foundation/process/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.errors.process import ProcessError
from provide.foundation.process.aio import async_run, async_shell, async_stream
from provide.foundation.process.exit import (
    exit_error,
    exit_interrupted,
    exit_success,
)
from provide.foundation.process.lifecycle import (
    ManagedProcess,
    wait_for_process_output,
)
from provide.foundation.process.shared import CompletedProcess
from provide.foundation.process.sync import run, run_simple, shell, stream

"""Process Execution Subsystem.

Provides an opinionated system for sync and async subprocess execution,
integrated with the framework's security model (command validation,
environment scrubbing) and logging. It also includes components for
advanced process lifecycle management.
"""

__all__ = [
    # Core types
    "CompletedProcess",
    # Process lifecycle management
    "ManagedProcess",
    "ProcessError",
    # Async execution (modern API)
    "async_run",
    "async_shell",
    "async_stream",
    # Exit utilities
    "exit_error",
    "exit_interrupted",
    "exit_success",
    # Sync execution
    "run",
    "run_simple",
    "shell",
    "stream",
    "wait_for_process_output",
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
