#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

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


def _inject_otel_trace_context(event_dict: dict[str, Any]) -> bool:
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


def _inject_foundation_trace_context(event_dict: dict[str, Any]) -> bool:
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


def inject_trace_context(logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
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


def should_inject_trace_context() -> bool:
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


# 🧱🏗️🔚
