#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Foundation tracer spans module."""

from typing import Never

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
from provide.testkit.time import make_controlled_time
import pytest

from provide.foundation.tracer.spans import Span


class TestSpanContextManagement(FoundationTestCase):
    """Test context manager integration with Foundation tracer."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_context_manager_with_foundation_context_success(self) -> None:
        """Test context manager with successful Foundation tracer context setup."""
        with (
            patch("provide.foundation.tracer.context.set_current_span") as mock_set_span,
            Span(name="test_op", time_source=self.get_time) as span,
        ):
            assert span._active is True
            # Should be called twice: enter (with span) and exit (with None)
            assert mock_set_span.call_count >= 1
            mock_set_span.assert_any_call(span)

    def test_context_manager_with_foundation_context_error(self) -> None:
        """Test context manager when Foundation tracer context fails."""
        with patch("provide.foundation.tracer.context.set_current_span") as mock_set_span:
            mock_set_span.side_effect = [Exception("Context error"), None]

            with Span(name="test_op", time_source=self.get_time) as span:
                assert span._active is True
                # Should still work despite context error

            assert span._active is False

    def test_context_manager_foundation_import_error(self) -> None:
        """Test context manager when Foundation tracer context module can't be imported."""
        # Simplified test - just mock the import directly within the context manager methods
        import builtins

        original_import = builtins.__import__

        def failing_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "provide.foundation.tracer.context":
                raise ImportError("Module not found")
            return original_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", side_effect=failing_import):
            with Span(name="test_op", time_source=self.get_time) as span:
                assert span._active is True
                # Should still work despite import error

            assert span._active is False

    def test_context_manager_clears_foundation_context_on_exit(self) -> None:
        """Test that context manager clears Foundation tracer context on exit."""
        with patch("provide.foundation.tracer.context.set_current_span") as mock_set_span:
            with Span(name="test_op", time_source=self.get_time):
                pass

            # Should call with span on enter, then with None on exit
            mock_set_span.assert_any_call(None)

    def test_context_manager_handles_foundation_clear_error(self) -> None:
        """Test context manager when clearing Foundation context fails."""
        with patch("provide.foundation.tracer.context.set_current_span") as mock_set_span:
            mock_set_span.side_effect = [None, Exception("Clear error")]

            with Span(name="test_op", time_source=self.get_time) as span:
                pass

            assert span._active is False
            # Should still finish despite clear error


class TestSpanEdgeCases(FoundationTestCase):
    """Test edge cases and error scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Create controlled time for all tests
        self.get_time, self.advance_time, self.fake_sleep, self.fake_async_sleep = make_controlled_time()

    def test_span_without_otel_dependencies(self) -> None:
        """Test span creation when OpenTelemetry is not available."""
        with patch("provide.foundation.tracer.spans._HAS_OTEL", False):
            span = Span(name="test_op", time_source=self.get_time)

            assert span._otel_span is None
            # All operations should work normally
            span.set_tag("key", "value")
            span.set_error("Test error")
            span.finish()

            assert span.tags["key"] == "value"
            assert span.status == "error"
            assert span.error == "Test error"
            assert span._active is False

    def test_span_set_tag_with_none_otel_span(self) -> None:
        """Test setting tag when _otel_span is None."""
        span = Span(name="test_op", time_source=self.get_time)
        span._otel_span = None

        span.set_tag("user_id", "123")
        assert span.tags["user_id"] == "123"

    def test_span_set_error_without_status_classes(self) -> None:
        """Test setting error when Status/StatusCode are None."""
        from provide.testkit.mocking import MagicMock

        with (
            patch("provide.foundation.tracer.spans._HAS_OTEL", True),
            patch("provide.foundation.tracer.spans.Status", None),
            patch("provide.foundation.tracer.spans.StatusCode", None),
        ):
            span = Span(name="test_op", time_source=self.get_time)
            span._otel_span = MagicMock()

            span.set_error("Test error")

            assert span.status == "error"
            assert span.error == "Test error"

    def test_span_context_manager_with_none_exception_value(self) -> Never:
        """Test context manager when exception has no value."""
        with pytest.raises(ValueError), Span(name="test_op", time_source=self.get_time) as span:
            raise ValueError

        assert span.status == "error"
        assert span.error == ""

    def test_span_dataclass_field_defaults(self) -> None:
        """Test that dataclass fields have correct defaults."""
        span = Span(name="test_op", time_source=self.get_time)

        # Test all default values
        assert isinstance(span.span_id, str)
        assert len(span.span_id) == 36  # UUID4 format
        assert span.parent_id is None
        assert isinstance(span.trace_id, str)
        assert len(span.trace_id) == 36  # UUID4 format
        assert isinstance(span.start_time, float)
        assert span.start_time >= 0
        assert span.end_time is None
        assert span.tags == {}
        assert span.status == "ok"
        assert span.error is None
        assert span._active is True

    def test_span_to_dict_with_all_fields(self) -> None:
        """Test to_dict includes all expected fields."""
        span = Span(
            name="complex_op",
            span_id="custom-span-id",
            parent_id="custom-parent-id",
            trace_id="custom-trace-id",
            start_time=1000.0,
            tags={"user": "test"},
            status="pending",
            time_source=self.get_time,
        )
        span.end_time = 1002.0
        span.error = "Test error"

        result = span.to_dict()

        expected_keys = {
            "name",
            "span_id",
            "parent_id",
            "trace_id",
            "start_time",
            "end_time",
            "duration_ms",
            "tags",
            "status",
            "error",
        }
        assert set(result.keys()) == expected_keys
        assert result["name"] == "complex_op"
        assert result["span_id"] == "custom-span-id"
        assert result["parent_id"] == "custom-parent-id"
        assert result["trace_id"] == "custom-trace-id"
        assert result["start_time"] == 1000.0
        assert result["end_time"] == 1002.0
        assert result["duration_ms"] == 2000.0
        assert result["tags"] == {"user": "test"}
        assert result["status"] == "pending"
        assert result["error"] == "Test error"


# 🧱🏗️🔚
