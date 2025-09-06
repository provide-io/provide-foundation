#
# spans.py
#
"""
Enhanced span implementation for Foundation tracer.
Provides OpenTelemetry integration when available, falls back to simple tracing.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from provide.foundation.logger import get_logger

log = get_logger(__name__)

# OpenTelemetry feature detection
try:
    from opentelemetry import trace as otel_trace
    from opentelemetry.trace import Status, StatusCode
    _HAS_OTEL = True
except ImportError:
    otel_trace = None
    Status = None
    StatusCode = None
    _HAS_OTEL = False


@dataclass
class Span:
    """
    Enhanced span implementation with optional OpenTelemetry integration.
    
    Maintains simple API while providing distributed tracing when OpenTelemetry is available.
    """
    
    name: str
    span_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    status: str = "ok"
    error: Optional[str] = None
    
    # Internal OpenTelemetry span (when available)
    _otel_span: Optional["otel_trace.Span"] = field(default=None, init=False, repr=False)
    _active: bool = field(default=True, init=False, repr=False)
    
    def __post_init__(self) -> None:
        """Initialize span after creation."""
        # Try to create OpenTelemetry span if available
        if _HAS_OTEL:
            try:
                tracer = otel_trace.get_tracer(__name__)
                self._otel_span = tracer.start_span(self.name)
                
                # Sync OpenTelemetry span ID with our ID for consistency
                if hasattr(self._otel_span, 'get_span_context'):
                    span_context = self._otel_span.get_span_context()
                    # Convert to hex string for consistency
                    self.span_id = f"{span_context.span_id:016x}"
                    self.trace_id = f"{span_context.trace_id:032x}"
                    
                log.debug(f"🔍✨ Created OpenTelemetry span: {self.name}")
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to create OpenTelemetry span: {e}")
                self._otel_span = None
    
    def set_tag(self, key: str, value: Any) -> None:
        """Set a tag on the span."""
        self.tags[key] = value
        
        # Also set on OpenTelemetry span if available
        if self._otel_span and hasattr(self._otel_span, 'set_attribute'):
            try:
                self._otel_span.set_attribute(key, value)
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to set OpenTelemetry attribute: {e}")
        
    def set_error(self, error: str | Exception) -> None:
        """Mark the span as having an error."""
        self.status = "error"
        self.error = str(error)
        
        # Also set on OpenTelemetry span if available
        if self._otel_span and Status and StatusCode:
            try:
                self._otel_span.set_status(Status(StatusCode.ERROR, str(error)))
                self._otel_span.record_exception(error if isinstance(error, Exception) else Exception(error))
            except Exception as e:
                log.debug(f"🔍⚠️ Failed to set OpenTelemetry error: {e}")
        
    def finish(self) -> None:
        """Finish the span and record end time."""
        if self._active:
            self.end_time = time.time()
            self._active = False
            
            # Also finish OpenTelemetry span if available
            if self._otel_span:
                try:
                    self._otel_span.end()
                    log.debug(f"🔍✅ Finished OpenTelemetry span: {self.name}")
                except Exception as e:
                    log.debug(f"🔍⚠️ Failed to finish OpenTelemetry span: {e}")
            self._active = False
            
    def duration_ms(self) -> float:
        """Get the duration of the span in milliseconds."""
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000
        
    def to_dict(self) -> Dict[str, Any]:
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
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if exc_type is not None:
            self.set_error(f"{exc_type.__name__}: {exc_val}")
        self.finish()