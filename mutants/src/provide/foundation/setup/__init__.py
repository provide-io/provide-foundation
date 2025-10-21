# provide/foundation/setup/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

#
# __init__.py
#
from provide.foundation.concurrency.locks import get_lock_manager
from provide.foundation.logger.setup import internal_setup
from provide.foundation.metrics.otel import shutdown_opentelemetry_metrics
from provide.foundation.streams.file import flush_log_streams
from provide.foundation.tracer.otel import shutdown_opentelemetry

"""Foundation Setup Module.

This module provides the main setup API for Foundation,
orchestrating logging, tracing, and other subsystems.
"""

_EXPLICIT_SETUP_DONE = False
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


async def x_shutdown_foundation__mutmut_orig(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire("foundation.logger.setup"):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


async def x_shutdown_foundation__mutmut_1(timeout_millis: int = 5001) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire("foundation.logger.setup"):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


async def x_shutdown_foundation__mutmut_2(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire(None):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


async def x_shutdown_foundation__mutmut_3(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire("XXfoundation.logger.setupXX"):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()


async def x_shutdown_foundation__mutmut_4(timeout_millis: int = 5000) -> None:
    """Gracefully shutdown all Foundation subsystems.

    Args:
        timeout_millis: Timeout for shutdown (currently unused)

    """
    with get_lock_manager().acquire("FOUNDATION.LOGGER.SETUP"):
        # Shutdown OpenTelemetry tracing and metrics
        shutdown_opentelemetry()
        shutdown_opentelemetry_metrics()

        # Flush logging streams
        flush_log_streams()

x_shutdown_foundation__mutmut_mutants : ClassVar[MutantDict] = {
'x_shutdown_foundation__mutmut_1': x_shutdown_foundation__mutmut_1, 
    'x_shutdown_foundation__mutmut_2': x_shutdown_foundation__mutmut_2, 
    'x_shutdown_foundation__mutmut_3': x_shutdown_foundation__mutmut_3, 
    'x_shutdown_foundation__mutmut_4': x_shutdown_foundation__mutmut_4
}

def shutdown_foundation(*args, **kwargs):
    result = _mutmut_trampoline(x_shutdown_foundation__mutmut_orig, x_shutdown_foundation__mutmut_mutants, args, kwargs)
    return result 

shutdown_foundation.__signature__ = _mutmut_signature(x_shutdown_foundation__mutmut_orig)
x_shutdown_foundation__mutmut_orig.__name__ = 'x_shutdown_foundation'


__all__ = [
    "internal_setup",
    "shutdown_foundation",
]


# <3 🧱🤝🛠️🪄
