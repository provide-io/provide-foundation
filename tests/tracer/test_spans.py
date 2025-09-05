#
# test_spans.py
#
"""Tests for Foundation tracer spans module."""

import time
import uuid
from unittest.mock import patch

import pytest

from provide.foundation.tracer.spans import Span


class TestSpan:
    """Test Span functionality."""
    
    def test_span_creation_with_defaults(self):
        """Test creating a span with default values."""
        span = Span("test_operation")
        
        assert span.name == "test_operation"
        assert span.span_id is not None
        assert span.trace_id is not None
        assert span.parent_id is None
        assert span.start_time > 0
        assert span.end_time is None
        assert span.tags == {}
        assert span.status == "ok"
        assert span.error is None
        assert span._active is True
    
    def test_span_creation_with_custom_values(self):
        """Test creating a span with custom values."""
        custom_span_id = str(uuid.uuid4())
        custom_trace_id = str(uuid.uuid4())
        custom_parent_id = str(uuid.uuid4())
        custom_start_time = time.time()
        custom_tags = {"service": "auth", "user_id": "123"}
        
        span = Span(
            name="auth_check",
            span_id=custom_span_id,
            trace_id=custom_trace_id,
            parent_id=custom_parent_id,
            start_time=custom_start_time,
            tags=custom_tags,
            status="pending"
        )
        
        assert span.name == "auth_check"
        assert span.span_id == custom_span_id
        assert span.trace_id == custom_trace_id
        assert span.parent_id == custom_parent_id
        assert span.start_time == custom_start_time
        assert span.tags == custom_tags
        assert span.status == "pending"
    
    def test_set_tag(self):
        """Test setting tags on a span."""
        span = Span("test_op")
        
        span.set_tag("user_id", "12345")
        span.set_tag("action", "login")
        
        assert span.tags["user_id"] == "12345"
        assert span.tags["action"] == "login"
    
    def test_set_error_with_string(self):
        """Test setting error with string message."""
        span = Span("test_op")
        
        span.set_error("Database connection failed")
        
        assert span.status == "error"
        assert span.error == "Database connection failed"
    
    def test_set_error_with_exception(self):
        """Test setting error with exception object."""
        span = Span("test_op")
        error = ValueError("Invalid input")
        
        span.set_error(error)
        
        assert span.status == "error"
        assert span.error == "Invalid input"
    
    def test_finish_span(self):
        """Test finishing a span."""
        span = Span("test_op")
        assert span._active is True
        assert span.end_time is None
        
        span.finish()
        
        assert span._active is False
        assert span.end_time is not None
        assert span.end_time > span.start_time
    
    def test_finish_span_twice(self):
        """Test that finishing a span twice doesn't change end_time."""
        span = Span("test_op")
        
        span.finish()
        first_end_time = span.end_time
        
        time.sleep(0.001)  # Small delay
        span.finish()
        
        assert span.end_time == first_end_time
    
    def test_duration_ms_active_span(self):
        """Test duration calculation for active span."""
        # Create span with known start time
        span = Span("test_op", start_time=1000.0)
        
        with patch('time.time') as mock_time:
            mock_time.return_value = 1001.5
            duration = span.duration_ms()
            
            assert duration == 1500.0  # 1.5 seconds = 1500ms
    
    def test_duration_ms_finished_span(self):
        """Test duration calculation for finished span."""
        # Create span with known start and end times
        span = Span("test_op", start_time=1000.0)
        span.end_time = 1002.0
        
        duration = span.duration_ms()
        assert duration == 2000.0  # 2 seconds = 2000ms
    
    def test_to_dict(self):
        """Test converting span to dictionary."""
        span = Span("test_op")
        span.set_tag("user_id", "123")
        span.set_tag("action", "login")
        span.finish()
        
        span_dict = span.to_dict()
        
        assert span_dict["name"] == "test_op"
        assert span_dict["span_id"] == span.span_id
        assert span_dict["trace_id"] == span.trace_id
        assert span_dict["parent_id"] is None
        assert span_dict["start_time"] == span.start_time
        assert span_dict["end_time"] == span.end_time
        assert span_dict["duration_ms"] > 0
        assert span_dict["tags"] == {"user_id": "123", "action": "login"}
        assert span_dict["status"] == "ok"
        assert span_dict["error"] is None
    
    def test_context_manager_success(self):
        """Test using span as context manager with success."""
        with Span("test_op") as span:
            span.set_tag("result", "success")
            assert span._active is True
        
        assert span._active is False
        assert span.end_time is not None
        assert span.status == "ok"
        assert span.error is None
    
    def test_context_manager_with_exception(self):
        """Test using span as context manager with exception."""
        with pytest.raises(ValueError):
            with Span("test_op") as span:
                span.set_tag("action", "failing_op")
                raise ValueError("Something went wrong")
        
        assert span._active is False
        assert span.end_time is not None
        assert span.status == "error"
        assert span.error == "ValueError: Something went wrong"
    
    def test_unique_ids_generated(self):
        """Test that unique IDs are generated for different spans."""
        span1 = Span("op1")
        span2 = Span("op2")
        
        assert span1.span_id != span2.span_id
        assert span1.trace_id != span2.trace_id
        
        # But they should be valid UUIDs
        uuid.UUID(span1.span_id)  # Should not raise
        uuid.UUID(span1.trace_id)  # Should not raise
        uuid.UUID(span2.span_id)  # Should not raise
        uuid.UUID(span2.trace_id)  # Should not raise


class TestSpanIntegration:
    """Test span integration scenarios."""
    
    def test_parent_child_relationship(self):
        """Test setting up parent-child span relationship."""
        parent_span = Span("parent_op")
        child_span = Span(
            "child_op", 
            parent_id=parent_span.span_id,
            trace_id=parent_span.trace_id
        )
        
        assert child_span.parent_id == parent_span.span_id
        assert child_span.trace_id == parent_span.trace_id
        assert child_span.span_id != parent_span.span_id
    
    def test_nested_context_managers(self):
        """Test nested spans using context managers."""
        with Span("outer_op") as outer_span:
            outer_span.set_tag("level", "outer")
            
            with Span("inner_op", parent_id=outer_span.span_id, trace_id=outer_span.trace_id) as inner_span:
                inner_span.set_tag("level", "inner")
                
                assert inner_span._active is True
                assert outer_span._active is True
            
            # Inner span should be finished
            assert inner_span._active is False
            assert outer_span._active is True
        
        # Both spans should be finished
        assert inner_span._active is False
        assert outer_span._active is False
    
    def test_span_timing_realistic(self):
        """Test span timing with realistic operation."""
        span = Span("database_query")
        span.set_tag("query", "SELECT * FROM users")
        
        # Simulate some work
        time.sleep(0.01)
        
        span.finish()
        
        duration = span.duration_ms()
        assert duration >= 10.0  # At least 10ms
        assert duration < 100.0  # But not too long for test