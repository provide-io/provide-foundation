# provide/foundation/cli/commands/logs/query.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any

from provide.foundation.cli.deps import click
from provide.foundation.cli.helpers import get_client_from_context, requires_click
from provide.foundation.cli.shutdown import with_cleanup
from provide.foundation.logger import get_logger
from provide.foundation.process import exit_error

"""Query logs command for Foundation CLI."""

log = get_logger(__name__)
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


def x__get_trace_id_if_needed__mutmut_orig(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_1(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_2(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = None
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_3(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span or current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_4(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = None
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_5(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = None
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_6(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_7(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo(None, err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_8(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=None)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_9(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo(err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_10(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo(
                "No active trace found.",
            )
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_11(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("XXNo active trace found.XX", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_12(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("no active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_13(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("NO ACTIVE TRACE FOUND.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_14(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=False)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_15(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo(None, err=True)
        return None


def x__get_trace_id_if_needed__mutmut_16(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=None)
        return None


def x__get_trace_id_if_needed__mutmut_17(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo(err=True)
        return None


def x__get_trace_id_if_needed__mutmut_18(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo(
            "Tracing not available.",
        )
        return None


def x__get_trace_id_if_needed__mutmut_19(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("XXTracing not available.XX", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_20(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("tracing not available.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_21(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("TRACING NOT AVAILABLE.", err=True)
        return None


def x__get_trace_id_if_needed__mutmut_22(current_trace: bool, trace_id: str | None) -> str | None:
    """Get trace ID from current trace context if needed."""
    if not current_trace:
        return trace_id

    try:
        # Try OpenTelemetry first
        from opentelemetry import trace

        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            return f"{span_context.trace_id:032x}"
        # Try Foundation tracer
        from provide.foundation.tracer.context import get_current_trace_id

        found_trace_id = get_current_trace_id()
        if not found_trace_id:
            click.echo("No active trace found.", err=True)
            return None
        return found_trace_id
    except ImportError:
        click.echo("Tracing not available.", err=False)
        return None


x__get_trace_id_if_needed__mutmut_mutants: ClassVar[MutantDict] = {
    "x__get_trace_id_if_needed__mutmut_1": x__get_trace_id_if_needed__mutmut_1,
    "x__get_trace_id_if_needed__mutmut_2": x__get_trace_id_if_needed__mutmut_2,
    "x__get_trace_id_if_needed__mutmut_3": x__get_trace_id_if_needed__mutmut_3,
    "x__get_trace_id_if_needed__mutmut_4": x__get_trace_id_if_needed__mutmut_4,
    "x__get_trace_id_if_needed__mutmut_5": x__get_trace_id_if_needed__mutmut_5,
    "x__get_trace_id_if_needed__mutmut_6": x__get_trace_id_if_needed__mutmut_6,
    "x__get_trace_id_if_needed__mutmut_7": x__get_trace_id_if_needed__mutmut_7,
    "x__get_trace_id_if_needed__mutmut_8": x__get_trace_id_if_needed__mutmut_8,
    "x__get_trace_id_if_needed__mutmut_9": x__get_trace_id_if_needed__mutmut_9,
    "x__get_trace_id_if_needed__mutmut_10": x__get_trace_id_if_needed__mutmut_10,
    "x__get_trace_id_if_needed__mutmut_11": x__get_trace_id_if_needed__mutmut_11,
    "x__get_trace_id_if_needed__mutmut_12": x__get_trace_id_if_needed__mutmut_12,
    "x__get_trace_id_if_needed__mutmut_13": x__get_trace_id_if_needed__mutmut_13,
    "x__get_trace_id_if_needed__mutmut_14": x__get_trace_id_if_needed__mutmut_14,
    "x__get_trace_id_if_needed__mutmut_15": x__get_trace_id_if_needed__mutmut_15,
    "x__get_trace_id_if_needed__mutmut_16": x__get_trace_id_if_needed__mutmut_16,
    "x__get_trace_id_if_needed__mutmut_17": x__get_trace_id_if_needed__mutmut_17,
    "x__get_trace_id_if_needed__mutmut_18": x__get_trace_id_if_needed__mutmut_18,
    "x__get_trace_id_if_needed__mutmut_19": x__get_trace_id_if_needed__mutmut_19,
    "x__get_trace_id_if_needed__mutmut_20": x__get_trace_id_if_needed__mutmut_20,
    "x__get_trace_id_if_needed__mutmut_21": x__get_trace_id_if_needed__mutmut_21,
    "x__get_trace_id_if_needed__mutmut_22": x__get_trace_id_if_needed__mutmut_22,
}


def _get_trace_id_if_needed(*args, **kwargs):
    result = _mutmut_trampoline(
        x__get_trace_id_if_needed__mutmut_orig, x__get_trace_id_if_needed__mutmut_mutants, args, kwargs
    )
    return result


_get_trace_id_if_needed.__signature__ = _mutmut_signature(x__get_trace_id_if_needed__mutmut_orig)
x__get_trace_id_if_needed__mutmut_orig.__name__ = "x__get_trace_id_if_needed"


def x__build_query_sql__mutmut_orig(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_1(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_2(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(None, stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_3(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", None):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_4(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_5(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(
        r"^[a-zA-Z0-9_]+$",
    ):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_6(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"XX^[a-zA-Z0-9_]+$XX", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_7(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-za-z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_8(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[A-ZA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_9(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(None)

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_10(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 and size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_11(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) and size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_12(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_13(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size < 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_14(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 1 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_15(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size >= 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_16(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10001:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_17(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(None)

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_18(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = None
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_19(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_20(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(None, trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_21(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", None):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_22(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_23(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(
            r"^[a-fA-F0-9\-]+$",
        ):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_24(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"XX^[a-fA-F0-9\-]+$XX", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_25(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fa-f0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_26(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[A-FA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_27(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(None)
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_28(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(None)

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_29(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_30(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(None)
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_31(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(None)

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_32(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_33(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(None, service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_34(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", None):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_35(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_36(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(
            r"^[a-zA-Z0-9_\-\.]+$",
        ):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_37(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"XX^[a-zA-Z0-9_\-\.]+$XX", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_38(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-za-z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_39(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[A-ZA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_40(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(None)
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_41(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(None)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_42(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = None
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_43(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(None)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_44(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {'XX AND XX'.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_45(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' and '.join(conditions)}" if conditions else ""
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


def x__build_query_sql__mutmut_46(
    trace_id: str | None,
    level: str | None,
    service: str | None,
    stream: str,
    size: int,
) -> str:
    """Build SQL query with WHERE conditions."""
    import re

    # Sanitize stream name - only allow alphanumeric and underscores
    if not re.match(r"^[a-zA-Z0-9_]+$", stream):
        raise ValueError(f"Invalid stream name: {stream}")

    # Sanitize size parameter
    if not isinstance(size, int) or size <= 0 or size > 10000:
        raise ValueError(f"Invalid size parameter: {size}")

    conditions = []
    if trace_id:
        # Sanitize trace_id - should be hex string or UUID format
        if not re.match(r"^[a-fA-F0-9\-]+$", trace_id):
            raise ValueError(f"Invalid trace_id format: {trace_id}")
        conditions.append(f"trace_id = '{trace_id}'")

    if level:
        # Sanitize level using Foundation's existing validation
        from provide.foundation.parsers.errors import _VALID_LOG_LEVEL_TUPLE

        if level not in _VALID_LOG_LEVEL_TUPLE:
            raise ValueError(f"Invalid log level: {level}")
        conditions.append(f"level = '{level}'")

    if service:
        # Sanitize service name - allow alphanumeric, hyphens, underscores, dots
        if not re.match(r"^[a-zA-Z0-9_\-\.]+$", service):
            raise ValueError(f"Invalid service name: {service}")
        conditions.append(f"service = '{service}'")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else "XXXX"
    # All parameters are sanitized above with regex validation
    return f"SELECT * FROM {stream} {where_clause} ORDER BY _timestamp DESC LIMIT {size}"  # nosec B608


x__build_query_sql__mutmut_mutants: ClassVar[MutantDict] = {
    "x__build_query_sql__mutmut_1": x__build_query_sql__mutmut_1,
    "x__build_query_sql__mutmut_2": x__build_query_sql__mutmut_2,
    "x__build_query_sql__mutmut_3": x__build_query_sql__mutmut_3,
    "x__build_query_sql__mutmut_4": x__build_query_sql__mutmut_4,
    "x__build_query_sql__mutmut_5": x__build_query_sql__mutmut_5,
    "x__build_query_sql__mutmut_6": x__build_query_sql__mutmut_6,
    "x__build_query_sql__mutmut_7": x__build_query_sql__mutmut_7,
    "x__build_query_sql__mutmut_8": x__build_query_sql__mutmut_8,
    "x__build_query_sql__mutmut_9": x__build_query_sql__mutmut_9,
    "x__build_query_sql__mutmut_10": x__build_query_sql__mutmut_10,
    "x__build_query_sql__mutmut_11": x__build_query_sql__mutmut_11,
    "x__build_query_sql__mutmut_12": x__build_query_sql__mutmut_12,
    "x__build_query_sql__mutmut_13": x__build_query_sql__mutmut_13,
    "x__build_query_sql__mutmut_14": x__build_query_sql__mutmut_14,
    "x__build_query_sql__mutmut_15": x__build_query_sql__mutmut_15,
    "x__build_query_sql__mutmut_16": x__build_query_sql__mutmut_16,
    "x__build_query_sql__mutmut_17": x__build_query_sql__mutmut_17,
    "x__build_query_sql__mutmut_18": x__build_query_sql__mutmut_18,
    "x__build_query_sql__mutmut_19": x__build_query_sql__mutmut_19,
    "x__build_query_sql__mutmut_20": x__build_query_sql__mutmut_20,
    "x__build_query_sql__mutmut_21": x__build_query_sql__mutmut_21,
    "x__build_query_sql__mutmut_22": x__build_query_sql__mutmut_22,
    "x__build_query_sql__mutmut_23": x__build_query_sql__mutmut_23,
    "x__build_query_sql__mutmut_24": x__build_query_sql__mutmut_24,
    "x__build_query_sql__mutmut_25": x__build_query_sql__mutmut_25,
    "x__build_query_sql__mutmut_26": x__build_query_sql__mutmut_26,
    "x__build_query_sql__mutmut_27": x__build_query_sql__mutmut_27,
    "x__build_query_sql__mutmut_28": x__build_query_sql__mutmut_28,
    "x__build_query_sql__mutmut_29": x__build_query_sql__mutmut_29,
    "x__build_query_sql__mutmut_30": x__build_query_sql__mutmut_30,
    "x__build_query_sql__mutmut_31": x__build_query_sql__mutmut_31,
    "x__build_query_sql__mutmut_32": x__build_query_sql__mutmut_32,
    "x__build_query_sql__mutmut_33": x__build_query_sql__mutmut_33,
    "x__build_query_sql__mutmut_34": x__build_query_sql__mutmut_34,
    "x__build_query_sql__mutmut_35": x__build_query_sql__mutmut_35,
    "x__build_query_sql__mutmut_36": x__build_query_sql__mutmut_36,
    "x__build_query_sql__mutmut_37": x__build_query_sql__mutmut_37,
    "x__build_query_sql__mutmut_38": x__build_query_sql__mutmut_38,
    "x__build_query_sql__mutmut_39": x__build_query_sql__mutmut_39,
    "x__build_query_sql__mutmut_40": x__build_query_sql__mutmut_40,
    "x__build_query_sql__mutmut_41": x__build_query_sql__mutmut_41,
    "x__build_query_sql__mutmut_42": x__build_query_sql__mutmut_42,
    "x__build_query_sql__mutmut_43": x__build_query_sql__mutmut_43,
    "x__build_query_sql__mutmut_44": x__build_query_sql__mutmut_44,
    "x__build_query_sql__mutmut_45": x__build_query_sql__mutmut_45,
    "x__build_query_sql__mutmut_46": x__build_query_sql__mutmut_46,
}


def _build_query_sql(*args, **kwargs):
    result = _mutmut_trampoline(
        x__build_query_sql__mutmut_orig, x__build_query_sql__mutmut_mutants, args, kwargs
    )
    return result


_build_query_sql.__signature__ = _mutmut_signature(x__build_query_sql__mutmut_orig)
x__build_query_sql__mutmut_orig.__name__ = "x__build_query_sql"


def x__execute_and_display_query__mutmut_orig(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_1(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = None

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_2(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(None)

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_3(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=None,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_4(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=None,
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_5(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time=None,
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_6(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=None,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_7(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=None,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_8(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_9(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_10(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_11(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_12(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_13(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "XX-1hXX",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_14(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1H",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_15(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="XXnowXX",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_16(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="NOW",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_17(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total != 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_18(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 1:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_19(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo(None)
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_20(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("XXNo logs found matching the query.XX")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_21(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("no logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_22(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("NO LOGS FOUND MATCHING THE QUERY.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_23(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = None
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_24(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(None, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_25(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=None)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_26(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_27(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(
                response,
            )
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_28(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(None)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_29(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format == "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_30(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "XXsummaryXX":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_31(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "SUMMARY":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_32(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(None)

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_33(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 1
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 1


def x__execute_and_display_query__mutmut_34(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(None, err=True)
        return 1


def x__execute_and_display_query__mutmut_35(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=None)
        return 1


def x__execute_and_display_query__mutmut_36(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(err=True)
        return 1


def x__execute_and_display_query__mutmut_37(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(
            f"Query failed: {e}",
        )
        return 1


def x__execute_and_display_query__mutmut_38(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=False)
        return 1


def x__execute_and_display_query__mutmut_39(sql: str, last: str, size: int, format: str, client: Any) -> int:
    """Execute query and display results."""
    from provide.foundation.integrations.openobserve import format_output, search_logs
    from provide.foundation.utils.async_helpers import run_async

    try:
        response = run_async(
            search_logs(
                sql=sql,
                start_time=f"-{last}" if last else "-1h",
                end_time="now",
                size=size,
                client=client,
            )
        )

        # Format and display results
        if response.total == 0:
            click.echo("No logs found matching the query.")
        else:
            output = format_output(response, format_type=format)
            click.echo(output)

            # Show summary for non-summary formats
            if format != "summary":
                click.echo(f"\n📊 Found {response.total} logs, showing {len(response.hits)}")

        return 0
    except Exception as e:
        click.echo(f"Query failed: {e}", err=True)
        return 2


x__execute_and_display_query__mutmut_mutants: ClassVar[MutantDict] = {
    "x__execute_and_display_query__mutmut_1": x__execute_and_display_query__mutmut_1,
    "x__execute_and_display_query__mutmut_2": x__execute_and_display_query__mutmut_2,
    "x__execute_and_display_query__mutmut_3": x__execute_and_display_query__mutmut_3,
    "x__execute_and_display_query__mutmut_4": x__execute_and_display_query__mutmut_4,
    "x__execute_and_display_query__mutmut_5": x__execute_and_display_query__mutmut_5,
    "x__execute_and_display_query__mutmut_6": x__execute_and_display_query__mutmut_6,
    "x__execute_and_display_query__mutmut_7": x__execute_and_display_query__mutmut_7,
    "x__execute_and_display_query__mutmut_8": x__execute_and_display_query__mutmut_8,
    "x__execute_and_display_query__mutmut_9": x__execute_and_display_query__mutmut_9,
    "x__execute_and_display_query__mutmut_10": x__execute_and_display_query__mutmut_10,
    "x__execute_and_display_query__mutmut_11": x__execute_and_display_query__mutmut_11,
    "x__execute_and_display_query__mutmut_12": x__execute_and_display_query__mutmut_12,
    "x__execute_and_display_query__mutmut_13": x__execute_and_display_query__mutmut_13,
    "x__execute_and_display_query__mutmut_14": x__execute_and_display_query__mutmut_14,
    "x__execute_and_display_query__mutmut_15": x__execute_and_display_query__mutmut_15,
    "x__execute_and_display_query__mutmut_16": x__execute_and_display_query__mutmut_16,
    "x__execute_and_display_query__mutmut_17": x__execute_and_display_query__mutmut_17,
    "x__execute_and_display_query__mutmut_18": x__execute_and_display_query__mutmut_18,
    "x__execute_and_display_query__mutmut_19": x__execute_and_display_query__mutmut_19,
    "x__execute_and_display_query__mutmut_20": x__execute_and_display_query__mutmut_20,
    "x__execute_and_display_query__mutmut_21": x__execute_and_display_query__mutmut_21,
    "x__execute_and_display_query__mutmut_22": x__execute_and_display_query__mutmut_22,
    "x__execute_and_display_query__mutmut_23": x__execute_and_display_query__mutmut_23,
    "x__execute_and_display_query__mutmut_24": x__execute_and_display_query__mutmut_24,
    "x__execute_and_display_query__mutmut_25": x__execute_and_display_query__mutmut_25,
    "x__execute_and_display_query__mutmut_26": x__execute_and_display_query__mutmut_26,
    "x__execute_and_display_query__mutmut_27": x__execute_and_display_query__mutmut_27,
    "x__execute_and_display_query__mutmut_28": x__execute_and_display_query__mutmut_28,
    "x__execute_and_display_query__mutmut_29": x__execute_and_display_query__mutmut_29,
    "x__execute_and_display_query__mutmut_30": x__execute_and_display_query__mutmut_30,
    "x__execute_and_display_query__mutmut_31": x__execute_and_display_query__mutmut_31,
    "x__execute_and_display_query__mutmut_32": x__execute_and_display_query__mutmut_32,
    "x__execute_and_display_query__mutmut_33": x__execute_and_display_query__mutmut_33,
    "x__execute_and_display_query__mutmut_34": x__execute_and_display_query__mutmut_34,
    "x__execute_and_display_query__mutmut_35": x__execute_and_display_query__mutmut_35,
    "x__execute_and_display_query__mutmut_36": x__execute_and_display_query__mutmut_36,
    "x__execute_and_display_query__mutmut_37": x__execute_and_display_query__mutmut_37,
    "x__execute_and_display_query__mutmut_38": x__execute_and_display_query__mutmut_38,
    "x__execute_and_display_query__mutmut_39": x__execute_and_display_query__mutmut_39,
}


def _execute_and_display_query(*args, **kwargs):
    result = _mutmut_trampoline(
        x__execute_and_display_query__mutmut_orig, x__execute_and_display_query__mutmut_mutants, args, kwargs
    )
    return result


_execute_and_display_query.__signature__ = _mutmut_signature(x__execute_and_display_query__mutmut_orig)
x__execute_and_display_query__mutmut_orig.__name__ = "x__execute_and_display_query"


@click.command("query")
@click.option(
    "--sql",
    help="SQL query to execute (if not provided, builds from other options)",
)
@click.option(
    "--current-trace",
    is_flag=True,
    help="Query logs for the current active trace",
)
@click.option(
    "--trace-id",
    help="Query logs for a specific trace ID",
)
@click.option(
    "--level",
    type=click.Choice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]),
    help="Filter by log level",
)
@click.option(
    "--service",
    help="Filter by service name",
)
@click.option(
    "--last",
    help="Time range (e.g., 1h, 30m, 5m)",
    default="1h",
)
@click.option(
    "--stream",
    default="default",
    help="Stream to query",
)
@click.option(
    "--size",
    "-n",
    type=int,
    default=100,
    help="Number of results",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "log", "table", "csv", "summary"]),
    default="log",
    help="Output format",
)
@click.pass_context
@requires_click
@with_cleanup
def query_command(
    ctx: click.Context,
    sql: str | None,
    current_trace: bool,
    trace_id: str | None,
    level: str | None,
    service: str | None,
    last: str,
    stream: str,
    size: int,
    format: str,
) -> int | None:
    """Query logs from OpenObserve.

    Examples:
        # Query recent logs
        foundation logs query --last 30m

        # Query errors
        foundation logs query --level ERROR --last 1h

        # Query by current trace
        foundation logs query --current-trace

        # Query by specific trace
        foundation logs query --trace-id abc123def456

        # Query by service
        foundation logs query --service auth-service --last 15m

        # Custom SQL query
        foundation logs query --sql "SELECT * FROM default WHERE duration_ms > 1000"

    """
    # Get client from context using shared helper
    client, error_code = get_client_from_context(ctx)
    if error_code != 0:
        exit_error("OpenObserve client not configured", code=error_code)

    # Build SQL query if not provided
    if not sql:
        trace_id_result = _get_trace_id_if_needed(current_trace, trace_id)
        if trace_id_result is None:
            exit_error("Trace ID not available", code=1)
        if trace_id_result:
            trace_id = trace_id_result

        sql = _build_query_sql(trace_id, level, service, stream, size)

    # Execute query and display results
    result = _execute_and_display_query(sql, last, size, format, client)
    if result != 0:
        exit_error("Query execution failed", code=result)

    return None


# <3 🧱🤝💻🪄
