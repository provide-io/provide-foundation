# provide/foundation/concurrency/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.concurrency.async_locks import (
    AsyncLockInfo,
    AsyncLockManager,
    get_async_lock_manager,
    register_foundation_async_locks,
)
from provide.foundation.concurrency.core import (
    async_gather,
    async_run,
    async_sleep,
    async_wait_for,
)
from provide.foundation.concurrency.locks import (
    LockInfo,
    LockManager,
    get_lock_manager,
    register_foundation_locks,
)

"""Concurrency utilities for Foundation.

Provides consistent async/await patterns, task management,
and concurrency utilities for Foundation applications.
"""

__all__ = [
    "AsyncLockInfo",
    "AsyncLockManager",
    "LockInfo",
    "LockManager",
    "async_gather",
    "async_run",
    "async_sleep",
    "async_wait_for",
    "get_async_lock_manager",
    "get_lock_manager",
    "register_foundation_async_locks",
    "register_foundation_locks",
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


# <3 🧱🤝🧵🪄
