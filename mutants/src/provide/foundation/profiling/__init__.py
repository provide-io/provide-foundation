# provide/foundation/profiling/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from provide.foundation.errors.profiling import (
    ExporterError,
    MetricsError,
    ProfilingError,
    SamplingError,
)
from provide.foundation.profiling.component import ProfilingComponent, register_profiling
from provide.foundation.profiling.metrics import ProfileMetrics
from provide.foundation.profiling.processor import ProfilingProcessor

"""Performance profiling hooks for Foundation telemetry.

Provides lightweight metrics collection and monitoring capabilities
for Foundation's logging and telemetry infrastructure.

Example:
    >>> from provide.foundation.profiling import register_profiling
    >>> from provide.foundation.hub import Hub
    >>>
    >>> hub = Hub()
    >>> register_profiling(hub)
    >>> profiler = hub.get_component("profiler")
    >>> profiler.enable()
    >>>
    >>> # Metrics are automatically collected
    >>> metrics = profiler.get_metrics()
    >>> print(f"Processing {metrics.messages_per_second:.0f} msg/sec")

"""

__all__ = [
    "ExporterError",
    "MetricsError",
    # Core components
    "ProfileMetrics",
    "ProfilingComponent",
    # Error classes
    "ProfilingError",
    "ProfilingProcessor",
    "SamplingError",
    "register_profiling",
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


# <3 🧱🤝⏱️🪄
