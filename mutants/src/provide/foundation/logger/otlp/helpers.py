# provide/foundation/logger/otlp/helpers.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Generic OTLP helper functions for trace context, endpoints, and log formatting.

Provides utility functions for working with OTLP/OpenTelemetry including:
- Trace context extraction
- Endpoint URL building
- Header construction
- Attribute normalization
"""

from __future__ import annotations

import json
from typing import Any
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


def x_extract_trace_context__mutmut_orig() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_1() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = None
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_2() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span or span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_3() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = None
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_4() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "XXtrace_idXX": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_5() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "TRACE_ID": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_6() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(None, "032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_7() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, None),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_8() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format("032x"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_9() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(
                        span_context.trace_id,
                    ),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_10() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "XX032xXX"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_11() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032X"),
                    "span_id": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_12() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "XXspan_idXX": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_13() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "SPAN_ID": format(span_context.span_id, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_14() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(None, "016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_15() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, None),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_16() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format("016x"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_17() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(
                        span_context.span_id,
                    ),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_18() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "XX016xXX"),
                }
    except ImportError:
        pass

    return None


def x_extract_trace_context__mutmut_19() -> dict[str, str] | None:
    """Extract current trace context from OpenTelemetry.

    Extracts trace context from OpenTelemetry if SDK is available
    and a valid span is recording.

    Returns:
        Dict with 'trace_id' and 'span_id', or None if not available

    Examples:
        >>> context = extract_trace_context()
        >>> # Returns {'trace_id': '...', 'span_id': '...'} or None
    """
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        if span and span.is_recording():
            span_context = span.get_span_context()
            if span_context.is_valid:
                return {
                    "trace_id": format(span_context.trace_id, "032x"),
                    "span_id": format(span_context.span_id, "016X"),
                }
    except ImportError:
        pass

    return None


x_extract_trace_context__mutmut_mutants: ClassVar[MutantDict] = {
    "x_extract_trace_context__mutmut_1": x_extract_trace_context__mutmut_1,
    "x_extract_trace_context__mutmut_2": x_extract_trace_context__mutmut_2,
    "x_extract_trace_context__mutmut_3": x_extract_trace_context__mutmut_3,
    "x_extract_trace_context__mutmut_4": x_extract_trace_context__mutmut_4,
    "x_extract_trace_context__mutmut_5": x_extract_trace_context__mutmut_5,
    "x_extract_trace_context__mutmut_6": x_extract_trace_context__mutmut_6,
    "x_extract_trace_context__mutmut_7": x_extract_trace_context__mutmut_7,
    "x_extract_trace_context__mutmut_8": x_extract_trace_context__mutmut_8,
    "x_extract_trace_context__mutmut_9": x_extract_trace_context__mutmut_9,
    "x_extract_trace_context__mutmut_10": x_extract_trace_context__mutmut_10,
    "x_extract_trace_context__mutmut_11": x_extract_trace_context__mutmut_11,
    "x_extract_trace_context__mutmut_12": x_extract_trace_context__mutmut_12,
    "x_extract_trace_context__mutmut_13": x_extract_trace_context__mutmut_13,
    "x_extract_trace_context__mutmut_14": x_extract_trace_context__mutmut_14,
    "x_extract_trace_context__mutmut_15": x_extract_trace_context__mutmut_15,
    "x_extract_trace_context__mutmut_16": x_extract_trace_context__mutmut_16,
    "x_extract_trace_context__mutmut_17": x_extract_trace_context__mutmut_17,
    "x_extract_trace_context__mutmut_18": x_extract_trace_context__mutmut_18,
    "x_extract_trace_context__mutmut_19": x_extract_trace_context__mutmut_19,
}


def extract_trace_context(*args, **kwargs):
    result = _mutmut_trampoline(
        x_extract_trace_context__mutmut_orig, x_extract_trace_context__mutmut_mutants, args, kwargs
    )
    return result


extract_trace_context.__signature__ = _mutmut_signature(x_extract_trace_context__mutmut_orig)
x_extract_trace_context__mutmut_orig.__name__ = "x_extract_trace_context"


def x_add_trace_context_to_attributes__mutmut_orig(attributes: dict[str, Any]) -> None:
    """Add trace context to attributes dict (modifies in place).

    Extracts trace context and adds trace_id/span_id to attributes.
    Safe to call even if no trace context is available (no-op).

    Args:
        attributes: Dictionary to add trace context to (modified in place)

    Examples:
        >>> attrs = {"key": "value"}
        >>> add_trace_context_to_attributes(attrs)
        >>> # attrs may now include 'trace_id' and 'span_id' if context available
    """
    trace_context = extract_trace_context()
    if trace_context:
        attributes.update(trace_context)


def x_add_trace_context_to_attributes__mutmut_1(attributes: dict[str, Any]) -> None:
    """Add trace context to attributes dict (modifies in place).

    Extracts trace context and adds trace_id/span_id to attributes.
    Safe to call even if no trace context is available (no-op).

    Args:
        attributes: Dictionary to add trace context to (modified in place)

    Examples:
        >>> attrs = {"key": "value"}
        >>> add_trace_context_to_attributes(attrs)
        >>> # attrs may now include 'trace_id' and 'span_id' if context available
    """
    trace_context = None
    if trace_context:
        attributes.update(trace_context)


def x_add_trace_context_to_attributes__mutmut_2(attributes: dict[str, Any]) -> None:
    """Add trace context to attributes dict (modifies in place).

    Extracts trace context and adds trace_id/span_id to attributes.
    Safe to call even if no trace context is available (no-op).

    Args:
        attributes: Dictionary to add trace context to (modified in place)

    Examples:
        >>> attrs = {"key": "value"}
        >>> add_trace_context_to_attributes(attrs)
        >>> # attrs may now include 'trace_id' and 'span_id' if context available
    """
    trace_context = extract_trace_context()
    if trace_context:
        attributes.update(None)


x_add_trace_context_to_attributes__mutmut_mutants: ClassVar[MutantDict] = {
    "x_add_trace_context_to_attributes__mutmut_1": x_add_trace_context_to_attributes__mutmut_1,
    "x_add_trace_context_to_attributes__mutmut_2": x_add_trace_context_to_attributes__mutmut_2,
}


def add_trace_context_to_attributes(*args, **kwargs):
    result = _mutmut_trampoline(
        x_add_trace_context_to_attributes__mutmut_orig,
        x_add_trace_context_to_attributes__mutmut_mutants,
        args,
        kwargs,
    )
    return result


add_trace_context_to_attributes.__signature__ = _mutmut_signature(
    x_add_trace_context_to_attributes__mutmut_orig
)
x_add_trace_context_to_attributes__mutmut_orig.__name__ = "x_add_trace_context_to_attributes"


def x_build_otlp_endpoint__mutmut_orig(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_1(
    base_endpoint: str,
    signal_type: str = "XXlogsXX",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_2(
    base_endpoint: str,
    signal_type: str = "LOGS",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_3(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = None

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_4(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip(None)

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_5(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.lstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_6(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("XX/XX")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_7(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = None
    if endpoint.endswith(expected_suffix):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


def x_build_otlp_endpoint__mutmut_8(
    base_endpoint: str,
    signal_type: str = "logs",
) -> str:
    """Build OTLP endpoint URL for specific signal type.

    Constructs the full OTLP endpoint URL for the given signal type.
    Handles trailing slashes and is idempotent (won't double-add paths).

    Args:
        base_endpoint: Base OTLP endpoint (e.g., "https://api.example.com")
        signal_type: "logs", "traces", or "metrics"

    Returns:
        Full endpoint URL (e.g., "https://api.example.com/v1/logs")

    Examples:
        >>> build_otlp_endpoint("https://api.example.com")
        'https://api.example.com/v1/logs'

        >>> build_otlp_endpoint("https://api.example.com/", "traces")
        'https://api.example.com/v1/traces'

        >>> build_otlp_endpoint("https://api.example.com/v1/logs")
        'https://api.example.com/v1/logs'
    """
    # Remove trailing slash
    endpoint = base_endpoint.rstrip("/")

    # Check if already has /v1/{signal} path (idempotent)
    expected_suffix = f"/v1/{signal_type}"
    if endpoint.endswith(None):
        return endpoint

    # Build full endpoint
    return f"{endpoint}/v1/{signal_type}"


x_build_otlp_endpoint__mutmut_mutants: ClassVar[MutantDict] = {
    "x_build_otlp_endpoint__mutmut_1": x_build_otlp_endpoint__mutmut_1,
    "x_build_otlp_endpoint__mutmut_2": x_build_otlp_endpoint__mutmut_2,
    "x_build_otlp_endpoint__mutmut_3": x_build_otlp_endpoint__mutmut_3,
    "x_build_otlp_endpoint__mutmut_4": x_build_otlp_endpoint__mutmut_4,
    "x_build_otlp_endpoint__mutmut_5": x_build_otlp_endpoint__mutmut_5,
    "x_build_otlp_endpoint__mutmut_6": x_build_otlp_endpoint__mutmut_6,
    "x_build_otlp_endpoint__mutmut_7": x_build_otlp_endpoint__mutmut_7,
    "x_build_otlp_endpoint__mutmut_8": x_build_otlp_endpoint__mutmut_8,
}


def build_otlp_endpoint(*args, **kwargs):
    result = _mutmut_trampoline(
        x_build_otlp_endpoint__mutmut_orig, x_build_otlp_endpoint__mutmut_mutants, args, kwargs
    )
    return result


build_otlp_endpoint.__signature__ = _mutmut_signature(x_build_otlp_endpoint__mutmut_orig)
x_build_otlp_endpoint__mutmut_orig.__name__ = "x_build_otlp_endpoint"


def x_build_otlp_headers__mutmut_orig(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_1(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = None

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_2(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(None)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_3(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault(None, "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_4(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", None)

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_5(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_6(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault(
        "Content-Type",
    )

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_7(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("XXContent-TypeXX", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_8(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("content-type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_9(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("CONTENT-TYPE", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_10(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "XXapplication/x-protobufXX")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_11(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "APPLICATION/X-PROTOBUF")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_12(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["Authorization"] = None

    return headers


def x_build_otlp_headers__mutmut_13(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["XXAuthorizationXX"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_14(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["authorization"] = f"Bearer {auth_token}"

    return headers


def x_build_otlp_headers__mutmut_15(
    base_headers: dict[str, str] | None = None,
    auth_token: str | None = None,
) -> dict[str, str]:
    """Build OTLP headers with optional authentication.

    Creates headers dictionary with OTLP-required headers and optional auth.

    Args:
        base_headers: Base headers to include
        auth_token: Optional bearer token for authentication

    Returns:
        Complete headers dict with Content-Type and auth

    Examples:
        >>> build_otlp_headers()
        {'Content-Type': 'application/x-protobuf'}

        >>> build_otlp_headers(auth_token="secret123")
        {'Content-Type': 'application/x-protobuf', 'Authorization': 'Bearer secret123'}

        >>> build_otlp_headers(base_headers={"X-Custom": "value"})
        {'X-Custom': 'value', 'Content-Type': 'application/x-protobuf'}
    """
    headers: dict[str, str] = {}

    if base_headers:
        headers.update(base_headers)

    # Add OTLP content type
    headers.setdefault("Content-Type", "application/x-protobuf")

    # Add auth token if provided
    if auth_token:
        headers["AUTHORIZATION"] = f"Bearer {auth_token}"

    return headers


x_build_otlp_headers__mutmut_mutants: ClassVar[MutantDict] = {
    "x_build_otlp_headers__mutmut_1": x_build_otlp_headers__mutmut_1,
    "x_build_otlp_headers__mutmut_2": x_build_otlp_headers__mutmut_2,
    "x_build_otlp_headers__mutmut_3": x_build_otlp_headers__mutmut_3,
    "x_build_otlp_headers__mutmut_4": x_build_otlp_headers__mutmut_4,
    "x_build_otlp_headers__mutmut_5": x_build_otlp_headers__mutmut_5,
    "x_build_otlp_headers__mutmut_6": x_build_otlp_headers__mutmut_6,
    "x_build_otlp_headers__mutmut_7": x_build_otlp_headers__mutmut_7,
    "x_build_otlp_headers__mutmut_8": x_build_otlp_headers__mutmut_8,
    "x_build_otlp_headers__mutmut_9": x_build_otlp_headers__mutmut_9,
    "x_build_otlp_headers__mutmut_10": x_build_otlp_headers__mutmut_10,
    "x_build_otlp_headers__mutmut_11": x_build_otlp_headers__mutmut_11,
    "x_build_otlp_headers__mutmut_12": x_build_otlp_headers__mutmut_12,
    "x_build_otlp_headers__mutmut_13": x_build_otlp_headers__mutmut_13,
    "x_build_otlp_headers__mutmut_14": x_build_otlp_headers__mutmut_14,
    "x_build_otlp_headers__mutmut_15": x_build_otlp_headers__mutmut_15,
}


def build_otlp_headers(*args, **kwargs):
    result = _mutmut_trampoline(
        x_build_otlp_headers__mutmut_orig, x_build_otlp_headers__mutmut_mutants, args, kwargs
    )
    return result


build_otlp_headers.__signature__ = _mutmut_signature(x_build_otlp_headers__mutmut_orig)
x_build_otlp_headers__mutmut_orig.__name__ = "x_build_otlp_headers"


def x_normalize_attributes__mutmut_orig(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_1(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = None

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_2(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is not None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_3(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = None
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_4(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = "XXXX"
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_5(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = None
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_6(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = None
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_7(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(None)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_8(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = None
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_9(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(None)
        else:
            normalized[key] = str(value)

    return normalized


def x_normalize_attributes__mutmut_10(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = None

    return normalized


def x_normalize_attributes__mutmut_11(attributes: dict[str, Any]) -> dict[str, Any]:
    """Normalize attribute values for OTLP compatibility.

    Converts non-serializable types to OTLP-compatible values:
    - Non-serializable types → strings
    - Nested dicts → JSON strings
    - Lists → JSON strings
    - None values → empty strings

    Returns new dict (doesn't modify input).

    Args:
        attributes: Dictionary of attributes to normalize

    Returns:
        New dictionary with normalized values

    Examples:
        >>> normalize_attributes({"key": "value"})
        {'key': 'value'}

        >>> normalize_attributes({"num": 42, "list": [1, 2, 3]})
        {'num': 42, 'list': '[1, 2, 3]'}

        >>> normalize_attributes({"nested": {"a": 1}})
        {'nested': '{"a": 1}'}
    """
    normalized: dict[str, Any] = {}

    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            normalized[key] = value
        elif isinstance(value, (dict, list)):
            try:
                normalized[key] = json.dumps(value)
            except (TypeError, ValueError):
                normalized[key] = str(value)
        else:
            normalized[key] = str(None)

    return normalized


x_normalize_attributes__mutmut_mutants: ClassVar[MutantDict] = {
    "x_normalize_attributes__mutmut_1": x_normalize_attributes__mutmut_1,
    "x_normalize_attributes__mutmut_2": x_normalize_attributes__mutmut_2,
    "x_normalize_attributes__mutmut_3": x_normalize_attributes__mutmut_3,
    "x_normalize_attributes__mutmut_4": x_normalize_attributes__mutmut_4,
    "x_normalize_attributes__mutmut_5": x_normalize_attributes__mutmut_5,
    "x_normalize_attributes__mutmut_6": x_normalize_attributes__mutmut_6,
    "x_normalize_attributes__mutmut_7": x_normalize_attributes__mutmut_7,
    "x_normalize_attributes__mutmut_8": x_normalize_attributes__mutmut_8,
    "x_normalize_attributes__mutmut_9": x_normalize_attributes__mutmut_9,
    "x_normalize_attributes__mutmut_10": x_normalize_attributes__mutmut_10,
    "x_normalize_attributes__mutmut_11": x_normalize_attributes__mutmut_11,
}


def normalize_attributes(*args, **kwargs):
    result = _mutmut_trampoline(
        x_normalize_attributes__mutmut_orig, x_normalize_attributes__mutmut_mutants, args, kwargs
    )
    return result


normalize_attributes.__signature__ = _mutmut_signature(x_normalize_attributes__mutmut_orig)
x_normalize_attributes__mutmut_orig.__name__ = "x_normalize_attributes"


__all__ = [
    "add_trace_context_to_attributes",
    "build_otlp_endpoint",
    "build_otlp_headers",
    "extract_trace_context",
    "normalize_attributes",
]


# <3 🧱🤝📝🪄
