# provide/foundation/streams/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.streams.console import (
    get_console_stream,
    is_tty,
    supports_color,
    write_to_console,
)
from provide.foundation.streams.core import (
    ensure_stderr_default,
    get_log_stream,
    set_log_stream_for_testing,
)
from provide.foundation.streams.file import (
    close_log_streams,
    configure_file_logging,
    flush_log_streams,
    reset_streams,
)

"""Foundation Streams Module.

Provides stream management functionality including console, file,
and core stream operations.
"""

__all__ = [
    "close_log_streams",
    # File stream functions
    "configure_file_logging",
    "ensure_stderr_default",
    "flush_log_streams",
    # Console stream functions
    "get_console_stream",
    # Core stream functions
    "get_log_stream",
    "is_tty",
    "reset_streams",
    "set_log_stream_for_testing",
    "supports_color",
    "write_to_console",
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


# <3 🧱🤝🌊🪄
