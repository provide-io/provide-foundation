#
# spans.py
#
"""
Simple span implementation for Foundation tracer.
Provides basic tracing functionality without external dependencies.
"""

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Span:
    """
    A simple span implementation for basic tracing.
    
    Tracks operation timing, context, and metadata without requiring OpenTelemetry.
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
    
    def __post_init__(self) -> None:
        """Initialize span after creation."""
        if not hasattr(self, '_active'):
            self._active = True
    
    def set_tag(self, key: str, value: Any) -> None:
        """Set a tag on the span."""
        self.tags[key] = value
        
    def set_error(self, error: str | Exception) -> None:
        """Mark the span as having an error."""
        self.status = "error"
        self.error = str(error)
        
    def finish(self) -> None:
        """Finish the span and record end time."""
        if self._active:
            self.end_time = time.time()
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