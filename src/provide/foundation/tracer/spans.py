#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""TODO: Add module docstring."""

from __future__ import annotations

#
# spans.py
#
import time
from typing import TYPE_CHECKING, Any
import uuid

from attrs import define, field

from provide.foundation.config.defaults import (
    DEFAULT_TRACER_ACTIVE,
    DEFAULT_TRACER_OTEL_SPAN,
)
from provide.foundation.logger import get_logger

"""Enhanced span implementation for Foundation tracer.
Provides OpenTelemetry integration when available, falls back to simple tracing.
"""

# OpenTelemetry feature detection
_HAS_OTEL: bool

if TYPE_CHECKING:
    from opentelemetry import trace as otel_trace
    from opentelemetry.trace import Status, StatusCode
else:
    try:
        from opentelemetry import trace as otel_trace
        from opentelemetry.trace import Status, StatusCode

        _HAS_OTEL = True
    except ImportError:
        otel_trace: Any = None
        Status: Any = None
        StatusCode: Any = None
        _HAS_OTEL = False

log = get_logger(__name__)


@define(slots=True, kw_only=True)
class Span:
    """Enhanced span implementation with optional OpenTelemetry integration.

    Maintains simple API while providing distributed tracing when OpenTelemetry is available.
    """

    name: str
    span_id: str = field(factory=lambda: str(uuid.uuid4()))
    parent_id: str | None = None
    trace_id: str = field(factory=lambda: str(uuid.uuid4()))
    start_time: float | None = None
    end_time: float | None = None
    tags: dict[str, Any] = field(factory=dict)
    status: str = "ok"
    error: str | None = None
    time_source: Any = field(default=None)

    # Internal OpenTelemetry span (when available)
    _otel_span: otel_trace.Span | None = field(default=DEFAULT_TRACER_OTEL_SPAN, init=False, repr=False)
    _active: bool = field(default=DEFAULT_TRACER_ACTIVE, init=False, repr=False)
    _time_source: Any = field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        """Initialize span after creation."""
        # Set up time source
        self._time_source = self.time_source if self.time_source is not None else time.time

        # Set start_time if not provided
        if self.start_time is None:
            object.__setattr__(self, "start_time", self._time_source())

        # Try to create OpenTelemetry span if available
        if _HAS_OTEL:
            try:
                tracer = otel_trace.get_tracer(__name__)
                self._otel_span = tracer.start_span(self.name)

                log.debug(f"🔍✨ Created OpenTelemetry span: {self.name}")
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to create OpenTelemetry span: {e}")
                self._otel_span = None

    def set_tag(self, key: str, value: Any) -> None:
        """Set a tag on the span."""
        self.tags[key] = value

        # Also set on OpenTelemetry span if available
        if self._otel_span and hasattr(self._otel_span, "set_attribute"):
            try:
                self._otel_span.set_attribute(key, value)
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to set OpenTelemetry attribute: {e}")

    def set_error(self, error: str | Exception) -> None:
        """Mark the span as having an error."""
        self.status = "error"
        self.error = str(error)

        # Also set on OpenTelemetry span if available
        if self._otel_span and Status is not None and StatusCode is not None:
            try:
                self._otel_span.set_status(Status(StatusCode.ERROR, str(error)))
                self._otel_span.record_exception(error if isinstance(error, Exception) else Exception(error))
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to set OpenTelemetry error: {e}")

    def finish(self) -> None:
        """Finish the span and record end time."""
        if self._active:
            self.end_time = self._time_source()
            self._active = False

            # Also finish OpenTelemetry span if available
            if self._otel_span:
                try:
                    self._otel_span.end()
                except Exception as e:
                    log.debug(f"🔍⚠️ Failed to finish OpenTelemetry span: {e}")

    def __enter__(self) -> Span:
        """Context manager entry."""
        # Set this span as current in OpenTelemetry context if available
        if self._otel_span and _HAS_OTEL:
            try:
                # OpenTelemetry spans are automatically set as current when started
                pass
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to set OpenTelemetry span context: {e}")

        # Also set in Foundation tracer context
        try:
            from provide.foundation.tracer.context import set_current_span

            set_current_span(self)
        except Exception as e:
            log.debug(f"🔍⚠️ Failed to set Foundation span context: {e}")

        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        """Context manager exit."""
        # Handle exceptions
        if exc_type is not None:
            error_msg = str(exc_val) if exc_val else exc_type.__name__
            if isinstance(exc_val, Exception):
                self.set_error(exc_val)
            else:
                self.set_error(error_msg)

        # Finish the span
        self.finish()

        # Clear from Foundation tracer context
        try:
            from provide.foundation.tracer.context import set_current_span

            set_current_span(None)
        except Exception as e:
            log.debug(f"🔍⚠️ Failed to clear Foundation span context: {e}")

    def duration_ms(self) -> float:
        """Get the duration of the span in milliseconds."""
        # start_time is guaranteed to be set in __attrs_post_init__
        start = self.start_time if self.start_time is not None else 0.0
        if self.end_time is None:
            return (self._time_source() - start) * 1000
        return (self.end_time - start) * 1000

    def to_dict(self) -> dict[str, Any]:
        """Convert span to dictionary representation."""
        return {
            "name": self.name,
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "trace_id": self.trace_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms(),
            "tags": self.tags,
            "status": self.status,
            "error": self.error,
        }


# 🧱🏗️🔚
