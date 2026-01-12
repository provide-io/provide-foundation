#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for trace processor with Foundation tracer fallback."""

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch


class TestTraceProcessorWithoutOtel(FoundationTestCase):
    """Test trace processor without OpenTelemetry."""

    def test_inject_trace_context_foundation_only(self) -> None:
        """Test using Foundation tracer when OpenTelemetry is not available."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with patch("provide.foundation.logger.processors.trace._HAS_OTEL", False):
            mock_span = Mock()
            mock_span.trace_id = "foundation-trace-xyz"
            mock_span.span_id = "foundation-span-abc"

            with (
                patch(
                    "provide.foundation.tracer.context.get_current_trace_id",
                    return_value="foundation-trace-xyz",
                ),
                patch(
                    "provide.foundation.tracer.context.get_current_span",
                    return_value=mock_span,
                ),
            ):
                event_dict = {"event": "test"}
                result = inject_trace_context(None, "info", event_dict)

                assert result["trace_id"] == "foundation-trace-xyz"
                assert result["span_id"] == "foundation-span-abc"

    def test_inject_trace_context_no_current_span(self) -> None:
        """Test when there's no current span."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                return_value="trace-only",
            ),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=None,
            ),
        ):
            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            assert result["trace_id"] == "trace-only"
            assert "span_id" not in result

    def test_inject_trace_context_no_trace_or_span(self) -> None:
        """Test when there's no trace ID or span."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                return_value=None,
            ),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=None,
            ),
        ):
            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            # Should return event_dict unchanged
            assert result == event_dict
            assert "trace_id" not in result
            assert "span_id" not in result

    def test_inject_trace_context_foundation_exception(self) -> None:
        """Test handling exception in Foundation tracer code."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                side_effect=Exception("Foundation Error"),
            ),
        ):
            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            # Should catch exception and return event_dict unchanged
            assert result == event_dict
            assert "trace_id" not in result


class TestShouldInjectTraceContextFoundation(FoundationTestCase):
    """Test should_inject_trace_context with Foundation tracer."""

    def test_should_inject_foundation_span(self) -> None:
        """Test should inject when Foundation has active span."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=Mock(),
            ),
        ):
            assert should_inject_trace_context() is True

    def test_should_inject_foundation_trace_id_only(self) -> None:
        """Test should inject when Foundation has trace ID only."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=None,
            ),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                return_value="trace-123",
            ),
        ):
            assert should_inject_trace_context() is True

    def test_should_not_inject_no_context(self) -> None:
        """Test should not inject when no trace context available."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=None,
            ),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                return_value=None,
            ),
        ):
            assert should_inject_trace_context() is False

    def test_should_not_inject_foundation_exception(self) -> None:
        """Test should not inject when Foundation tracer fails."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_span",
                side_effect=Exception("Foundation Error"),
            ),
        ):
            assert should_inject_trace_context() is False


class TestTraceProcessorFoundationLogging(FoundationTestCase):
    """Test logging behavior with Foundation tracer."""

    def test_debug_logging_on_foundation_injection(self) -> None:
        """Test successful Foundation trace injection (no internal logging)."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with patch("provide.foundation.logger.processors.trace._HAS_OTEL", False):
            mock_span = Mock()
            mock_span.trace_id = "trace-123"
            mock_span.span_id = "span-456"

            with (
                patch(
                    "provide.foundation.tracer.context.get_current_trace_id",
                    return_value="trace-123",
                ),
                patch(
                    "provide.foundation.tracer.context.get_current_span",
                    return_value=mock_span,
                ),
            ):
                event_dict = {"event": "test"}
                result = inject_trace_context(None, "info", event_dict)

                # Check Foundation trace context was injected
                assert "trace_id" in result
                assert "span_id" in result
                assert result["trace_id"] == "trace-123"
                assert result["span_id"] == "span-456"

    def test_debug_logging_on_foundation_failure(self) -> None:
        """Test Foundation tracer failure handling (no internal logging)."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", False),
            patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                side_effect=RuntimeError("Foundation error"),
            ),
        ):
            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            # Check that no trace context was injected due to error
            assert "trace_id" not in result or result.get("trace_id") is None
            # Should still return the original event dict
            assert result["event"] == "test"


# 🧱🏗️🔚
