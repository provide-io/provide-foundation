"""Trace context processor for injecting trace/span IDs into logs."""

from typing import Any, Dict

# Note: Cannot import get_logger here due to circular dependency during setup
# Will log directly when needed
import logging
log = logging.getLogger(__name__)

# OpenTelemetry feature detection
try:
    from opentelemetry import trace as otel_trace
    _HAS_OTEL = True
except ImportError:
    otel_trace = None
    _HAS_OTEL = False


def inject_trace_context(logger: Any, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Processor to inject trace context into log records.
    
    Args:
        logger: Logger instance
        method_name: Method name being called
        event_dict: Current event dictionary
        
    Returns:
        Event dictionary with trace context added
    """
    # Try OpenTelemetry trace context first
    if _HAS_OTEL:
        try:
            current_span = otel_trace.get_current_span()
            if current_span and current_span.is_recording():
                span_context = current_span.get_span_context()
                
                # Add OpenTelemetry trace and span IDs
                event_dict["trace_id"] = f"{span_context.trace_id:032x}"
                event_dict["span_id"] = f"{span_context.span_id:016x}"
                
                # Add trace flags if present
                if span_context.trace_flags:
                    event_dict["trace_flags"] = span_context.trace_flags
                    
                # Use level 5 (below DEBUG=10) for trace-level logging
                log.log(5, "🔍📝 Injected OpenTelemetry trace context into log")
                return event_dict
        except Exception as e:
            log.log(5, f"🔍⚠️ Failed to get OpenTelemetry trace context: {e}")
    
    # Fallback to Foundation's simple tracer context
    try:
        from provide.foundation.tracer.context import get_current_span, get_current_trace_id
        
        current_span = get_current_span()
        current_trace_id = get_current_trace_id()
        
        if current_span:
            event_dict["trace_id"] = current_span.trace_id
            event_dict["span_id"] = current_span.span_id
            log.log(5, "🔍📝 Injected Foundation trace context into log")
        elif current_trace_id:
            event_dict["trace_id"] = current_trace_id
            log.log(5, "🔍📝 Injected Foundation trace ID into log")
            
    except Exception as e:
        log.log(5, f"🔍⚠️ Failed to get Foundation trace context: {e}")
    
    return event_dict


def should_inject_trace_context() -> bool:
    """Check if trace context injection is available.
    
    Returns:
        True if trace context can be injected
    """
    # Check if OpenTelemetry is available and has active span
    if _HAS_OTEL:
        try:
            current_span = otel_trace.get_current_span()
            if current_span and current_span.is_recording():
                return True
        except Exception:
            pass
    
    # Check if Foundation tracer has active context
    try:
        from provide.foundation.tracer.context import get_current_span, get_current_trace_id
        return get_current_span() is not None or get_current_trace_id() is not None
    except Exception:
        pass
    
    return False