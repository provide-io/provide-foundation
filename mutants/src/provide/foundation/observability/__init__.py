# provide/foundation/observability/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING, Any

"""Observability module for Foundation.

Provides integration with observability platforms like OpenObserve.
Only available when OpenTelemetry dependencies are installed.
"""

# OpenTelemetry feature detection - Pattern 1: _HAS_* flag
if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace

    _HAS_OTEL: bool = True  # Assume available during type checking
else:
    try:
        from opentelemetry import trace as _otel_trace_module

        _HAS_OTEL = True
        otel_trace = _otel_trace_module
    except ImportError:
        _HAS_OTEL = False
        otel_trace: Any = None

# Pattern 2: Import real implementation or create stubs
if _HAS_OTEL:
    try:
        from provide.foundation.integrations.openobserve import (
            OpenObserveClient,
            search_logs,
            stream_logs,
        )

        # Commands will auto-register if click is available
        with suppress(ImportError):
            from provide.foundation.integrations.openobserve.commands import (  # noqa: F401
                openobserve_group,
            )
    except ImportError:
        # OpenObserve module not available - create stubs
        from provide.foundation.utils.stubs import create_dependency_stub, create_function_stub

        OpenObserveClient = create_dependency_stub("opentelemetry", "observability")  # type: ignore[misc,assignment]
        search_logs = create_function_stub("opentelemetry", "observability")
        stream_logs = create_function_stub("opentelemetry", "observability")
else:
    # OpenTelemetry not available - create stubs
    from provide.foundation.utils.stubs import create_dependency_stub, create_function_stub

    OpenObserveClient = create_dependency_stub("opentelemetry", "observability")  # type: ignore[misc,assignment]
    search_logs = create_function_stub("opentelemetry", "observability")
    stream_logs = create_function_stub("opentelemetry", "observability")


# Static __all__ export (always the same, regardless of dependencies)
__all__ = [
    "_HAS_OTEL",
    "OpenObserveClient",
    "is_openobserve_available",
    "otel_trace",
    "search_logs",
    "stream_logs",
]
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


def x_is_openobserve_available__mutmut_orig() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "OpenObserveClient" in globals()


def x_is_openobserve_available__mutmut_1() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL or "OpenObserveClient" in globals()


def x_is_openobserve_available__mutmut_2() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "XXOpenObserveClientXX" in globals()


def x_is_openobserve_available__mutmut_3() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "openobserveclient" in globals()


def x_is_openobserve_available__mutmut_4() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "OPENOBSERVECLIENT" in globals()


def x_is_openobserve_available__mutmut_5() -> bool:
    """Check if OpenObserve integration is available.

    Returns:
        True if OpenTelemetry and OpenObserve are available

    """
    return _HAS_OTEL and "OpenObserveClient" not in globals()

x_is_openobserve_available__mutmut_mutants : ClassVar[MutantDict] = {
'x_is_openobserve_available__mutmut_1': x_is_openobserve_available__mutmut_1, 
    'x_is_openobserve_available__mutmut_2': x_is_openobserve_available__mutmut_2, 
    'x_is_openobserve_available__mutmut_3': x_is_openobserve_available__mutmut_3, 
    'x_is_openobserve_available__mutmut_4': x_is_openobserve_available__mutmut_4, 
    'x_is_openobserve_available__mutmut_5': x_is_openobserve_available__mutmut_5
}

def is_openobserve_available(*args, **kwargs):
    result = _mutmut_trampoline(x_is_openobserve_available__mutmut_orig, x_is_openobserve_available__mutmut_mutants, args, kwargs)
    return result 

is_openobserve_available.__signature__ = _mutmut_signature(x_is_openobserve_available__mutmut_orig)
x_is_openobserve_available__mutmut_orig.__name__ = 'x_is_openobserve_available'


# <3 🧱🤝🔭🪄
