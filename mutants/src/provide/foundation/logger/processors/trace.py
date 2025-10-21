# provide/foundation/logger/processors/trace.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import structlog

"""Trace context processor for injecting trace/span IDs into logs."""

if TYPE_CHECKING:
    pass

# Note: Cannot import get_logger here due to circular dependency during setup
# Use structlog directly but bind logger_name for OTLP exports

log = structlog.get_logger().bind(logger_name=__name__)

# Note: Internal trace injection logging removed to avoid circular dependencies
# and level registration issues during logger setup

# OpenTelemetry feature detection
try:
    from opentelemetry import trace as _otel_trace_module

    _HAS_OTEL = True
    otel_trace_runtime: Any = _otel_trace_module
except ImportError:
    _HAS_OTEL = False
    otel_trace_runtime = None
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


def x__inject_otel_trace_context__mutmut_orig(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_1(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_2(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL or otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_3(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return True

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_4(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = None
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_5(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span or current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_6(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = None

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_7(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "XXtrace_idXX" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_8(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "TRACE_ID" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_9(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_10(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = None
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_11(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["XXtrace_idXX"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_12(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["TRACE_ID"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_13(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "XXspan_idXX" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_14(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "SPAN_ID" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_15(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_16(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = None

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_17(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["XXspan_idXX"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_18(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["SPAN_ID"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_19(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = None

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_20(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["XXtrace_flagsXX"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_21(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["TRACE_FLAGS"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_22(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return False
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return False


def x__inject_otel_trace_context__mutmut_23(event_dict: dict[str, Any]) -> bool:
    """Try to inject OpenTelemetry trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if OpenTelemetry context was injected successfully
    """
    if not (_HAS_OTEL and otel_trace_runtime):
        return False

    try:
        current_span = otel_trace_runtime.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()

            # Add OpenTelemetry trace and span IDs (only if not already present)
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
            if "span_id" not in event_dict:
                event_dict["span_id"] = f"{span_context.span_id:016x}"

            # Add trace flags if present
            if span_context.trace_flags:
                event_dict["trace_flags"] = span_context.trace_flags

            return True
    except Exception:
        # OpenTelemetry trace context unavailable
        pass

    return True

x__inject_otel_trace_context__mutmut_mutants : ClassVar[MutantDict] = {
'x__inject_otel_trace_context__mutmut_1': x__inject_otel_trace_context__mutmut_1, 
    'x__inject_otel_trace_context__mutmut_2': x__inject_otel_trace_context__mutmut_2, 
    'x__inject_otel_trace_context__mutmut_3': x__inject_otel_trace_context__mutmut_3, 
    'x__inject_otel_trace_context__mutmut_4': x__inject_otel_trace_context__mutmut_4, 
    'x__inject_otel_trace_context__mutmut_5': x__inject_otel_trace_context__mutmut_5, 
    'x__inject_otel_trace_context__mutmut_6': x__inject_otel_trace_context__mutmut_6, 
    'x__inject_otel_trace_context__mutmut_7': x__inject_otel_trace_context__mutmut_7, 
    'x__inject_otel_trace_context__mutmut_8': x__inject_otel_trace_context__mutmut_8, 
    'x__inject_otel_trace_context__mutmut_9': x__inject_otel_trace_context__mutmut_9, 
    'x__inject_otel_trace_context__mutmut_10': x__inject_otel_trace_context__mutmut_10, 
    'x__inject_otel_trace_context__mutmut_11': x__inject_otel_trace_context__mutmut_11, 
    'x__inject_otel_trace_context__mutmut_12': x__inject_otel_trace_context__mutmut_12, 
    'x__inject_otel_trace_context__mutmut_13': x__inject_otel_trace_context__mutmut_13, 
    'x__inject_otel_trace_context__mutmut_14': x__inject_otel_trace_context__mutmut_14, 
    'x__inject_otel_trace_context__mutmut_15': x__inject_otel_trace_context__mutmut_15, 
    'x__inject_otel_trace_context__mutmut_16': x__inject_otel_trace_context__mutmut_16, 
    'x__inject_otel_trace_context__mutmut_17': x__inject_otel_trace_context__mutmut_17, 
    'x__inject_otel_trace_context__mutmut_18': x__inject_otel_trace_context__mutmut_18, 
    'x__inject_otel_trace_context__mutmut_19': x__inject_otel_trace_context__mutmut_19, 
    'x__inject_otel_trace_context__mutmut_20': x__inject_otel_trace_context__mutmut_20, 
    'x__inject_otel_trace_context__mutmut_21': x__inject_otel_trace_context__mutmut_21, 
    'x__inject_otel_trace_context__mutmut_22': x__inject_otel_trace_context__mutmut_22, 
    'x__inject_otel_trace_context__mutmut_23': x__inject_otel_trace_context__mutmut_23
}

def _inject_otel_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(x__inject_otel_trace_context__mutmut_orig, x__inject_otel_trace_context__mutmut_mutants, args, kwargs)
    return result 

_inject_otel_trace_context.__signature__ = _mutmut_signature(x__inject_otel_trace_context__mutmut_orig)
x__inject_otel_trace_context__mutmut_orig.__name__ = 'x__inject_otel_trace_context'


def x__inject_foundation_trace_context__mutmut_orig(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_1(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = None
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_2(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = None

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_3(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "XXtrace_idXX" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_4(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "TRACE_ID" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_5(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_6(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = None
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_7(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["XXtrace_idXX"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_8(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["TRACE_ID"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_9(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "XXspan_idXX" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_10(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "SPAN_ID" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_11(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_12(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = None
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_13(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["XXspan_idXX"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_14(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["SPAN_ID"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_15(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return False
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_16(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id or "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_17(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "XXtrace_idXX" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_18(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "TRACE_ID" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_19(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_20(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = None
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_21(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["XXtrace_idXX"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_22(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["TRACE_ID"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_23(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return False

    except Exception:
        # Foundation trace context unavailable
        pass

    return False


def x__inject_foundation_trace_context__mutmut_24(event_dict: dict[str, Any]) -> bool:
    """Try to inject Foundation trace context.

    Args:
        event_dict: Event dictionary to modify

    Returns:
        True if Foundation context was injected successfully
    """
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        foundation_span = get_current_span()
        current_trace_id = get_current_trace_id()

        if foundation_span:
            if "trace_id" not in event_dict:
                event_dict["trace_id"] = foundation_span.trace_id
            if "span_id" not in event_dict:
                event_dict["span_id"] = foundation_span.span_id
            return True
        elif current_trace_id and "trace_id" not in event_dict:
            event_dict["trace_id"] = current_trace_id
            return True

    except Exception:
        # Foundation trace context unavailable
        pass

    return True

x__inject_foundation_trace_context__mutmut_mutants : ClassVar[MutantDict] = {
'x__inject_foundation_trace_context__mutmut_1': x__inject_foundation_trace_context__mutmut_1, 
    'x__inject_foundation_trace_context__mutmut_2': x__inject_foundation_trace_context__mutmut_2, 
    'x__inject_foundation_trace_context__mutmut_3': x__inject_foundation_trace_context__mutmut_3, 
    'x__inject_foundation_trace_context__mutmut_4': x__inject_foundation_trace_context__mutmut_4, 
    'x__inject_foundation_trace_context__mutmut_5': x__inject_foundation_trace_context__mutmut_5, 
    'x__inject_foundation_trace_context__mutmut_6': x__inject_foundation_trace_context__mutmut_6, 
    'x__inject_foundation_trace_context__mutmut_7': x__inject_foundation_trace_context__mutmut_7, 
    'x__inject_foundation_trace_context__mutmut_8': x__inject_foundation_trace_context__mutmut_8, 
    'x__inject_foundation_trace_context__mutmut_9': x__inject_foundation_trace_context__mutmut_9, 
    'x__inject_foundation_trace_context__mutmut_10': x__inject_foundation_trace_context__mutmut_10, 
    'x__inject_foundation_trace_context__mutmut_11': x__inject_foundation_trace_context__mutmut_11, 
    'x__inject_foundation_trace_context__mutmut_12': x__inject_foundation_trace_context__mutmut_12, 
    'x__inject_foundation_trace_context__mutmut_13': x__inject_foundation_trace_context__mutmut_13, 
    'x__inject_foundation_trace_context__mutmut_14': x__inject_foundation_trace_context__mutmut_14, 
    'x__inject_foundation_trace_context__mutmut_15': x__inject_foundation_trace_context__mutmut_15, 
    'x__inject_foundation_trace_context__mutmut_16': x__inject_foundation_trace_context__mutmut_16, 
    'x__inject_foundation_trace_context__mutmut_17': x__inject_foundation_trace_context__mutmut_17, 
    'x__inject_foundation_trace_context__mutmut_18': x__inject_foundation_trace_context__mutmut_18, 
    'x__inject_foundation_trace_context__mutmut_19': x__inject_foundation_trace_context__mutmut_19, 
    'x__inject_foundation_trace_context__mutmut_20': x__inject_foundation_trace_context__mutmut_20, 
    'x__inject_foundation_trace_context__mutmut_21': x__inject_foundation_trace_context__mutmut_21, 
    'x__inject_foundation_trace_context__mutmut_22': x__inject_foundation_trace_context__mutmut_22, 
    'x__inject_foundation_trace_context__mutmut_23': x__inject_foundation_trace_context__mutmut_23, 
    'x__inject_foundation_trace_context__mutmut_24': x__inject_foundation_trace_context__mutmut_24
}

def _inject_foundation_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(x__inject_foundation_trace_context__mutmut_orig, x__inject_foundation_trace_context__mutmut_mutants, args, kwargs)
    return result 

_inject_foundation_trace_context.__signature__ = _mutmut_signature(x__inject_foundation_trace_context__mutmut_orig)
x__inject_foundation_trace_context__mutmut_orig.__name__ = 'x__inject_foundation_trace_context'


def x_inject_trace_context__mutmut_orig(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Processor to inject trace context into log records.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Current event dictionary

    Returns:
        Event dictionary with trace context added

    """
    # Try OpenTelemetry trace context first
    if _inject_otel_trace_context(event_dict):
        return event_dict

    # Fallback to Foundation's simple tracer context
    _inject_foundation_trace_context(event_dict)

    return event_dict


def x_inject_trace_context__mutmut_1(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Processor to inject trace context into log records.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Current event dictionary

    Returns:
        Event dictionary with trace context added

    """
    # Try OpenTelemetry trace context first
    if _inject_otel_trace_context(None):
        return event_dict

    # Fallback to Foundation's simple tracer context
    _inject_foundation_trace_context(event_dict)

    return event_dict


def x_inject_trace_context__mutmut_2(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    """Processor to inject trace context into log records.

    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Current event dictionary

    Returns:
        Event dictionary with trace context added

    """
    # Try OpenTelemetry trace context first
    if _inject_otel_trace_context(event_dict):
        return event_dict

    # Fallback to Foundation's simple tracer context
    _inject_foundation_trace_context(None)

    return event_dict

x_inject_trace_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_inject_trace_context__mutmut_1': x_inject_trace_context__mutmut_1, 
    'x_inject_trace_context__mutmut_2': x_inject_trace_context__mutmut_2
}

def inject_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(x_inject_trace_context__mutmut_orig, x_inject_trace_context__mutmut_mutants, args, kwargs)
    return result 

inject_trace_context.__signature__ = _mutmut_signature(x_inject_trace_context__mutmut_orig)
x_inject_trace_context__mutmut_orig.__name__ = 'x_inject_trace_context'


def x_should_inject_trace_context__mutmut_orig() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_1() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL or otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_2() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = None
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_3() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span or current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_4() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return False
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_5() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None and get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_6() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is None or get_current_trace_id() is not None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_7() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is None
    except Exception:
        pass

    return False


def x_should_inject_trace_context__mutmut_8() -> bool:
    """Check if trace context injection is available.

    Returns:
        True if trace context can be injected

    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL and otel_trace_runtime:
        try:
            current_span = otel_trace_runtime.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass

    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import (
            get_current_span,
            get_current_trace_id,
        )

        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass

    return True

x_should_inject_trace_context__mutmut_mutants : ClassVar[MutantDict] = {
'x_should_inject_trace_context__mutmut_1': x_should_inject_trace_context__mutmut_1, 
    'x_should_inject_trace_context__mutmut_2': x_should_inject_trace_context__mutmut_2, 
    'x_should_inject_trace_context__mutmut_3': x_should_inject_trace_context__mutmut_3, 
    'x_should_inject_trace_context__mutmut_4': x_should_inject_trace_context__mutmut_4, 
    'x_should_inject_trace_context__mutmut_5': x_should_inject_trace_context__mutmut_5, 
    'x_should_inject_trace_context__mutmut_6': x_should_inject_trace_context__mutmut_6, 
    'x_should_inject_trace_context__mutmut_7': x_should_inject_trace_context__mutmut_7, 
    'x_should_inject_trace_context__mutmut_8': x_should_inject_trace_context__mutmut_8
}

def should_inject_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(x_should_inject_trace_context__mutmut_orig, x_should_inject_trace_context__mutmut_mutants, args, kwargs)
    return result 

should_inject_trace_context.__signature__ = _mutmut_signature(x_should_inject_trace_context__mutmut_orig)
x_should_inject_trace_context__mutmut_orig.__name__ = 'x_should_inject_trace_context'


# <3 🧱🤝📝🪄
