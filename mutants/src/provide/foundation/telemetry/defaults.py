# provide/foundation/telemetry/defaults.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

"""Telemetry defaults for Foundation configuration."""

# =================================
# Telemetry Defaults
# =================================
DEFAULT_TELEMETRY_GLOBALLY_DISABLED = False
DEFAULT_TRACING_ENABLED = True
DEFAULT_METRICS_ENABLED = True
DEFAULT_OTLP_PROTOCOL = "http/protobuf"
DEFAULT_TRACE_SAMPLE_RATE = 1.0
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


# =================================
# Factory Functions
# =================================


def default_otlp_headers() -> dict[str, str]:
    """Factory for OTLP headers dictionary."""
    return {}


__all__ = [
    "DEFAULT_METRICS_ENABLED",
    "DEFAULT_OTLP_PROTOCOL",
    "DEFAULT_TELEMETRY_GLOBALLY_DISABLED",
    "DEFAULT_TRACE_SAMPLE_RATE",
    "DEFAULT_TRACING_ENABLED",
    "default_otlp_headers",
]


# <3 🧱🤝📡🪄
