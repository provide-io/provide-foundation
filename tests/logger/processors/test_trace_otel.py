#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for trace processor with OpenTelemetry integration."""

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch


class TestTraceProcessorWithOtel(FoundationTestCase):
    """Test trace processor with OpenTelemetry available."""

    def test_inject_trace_context_with_otel_span(self) -> None:
        """Test injecting trace context when OpenTelemetry span is available."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        # Mock OpenTelemetry components
        mock_span = Mock()
        mock_span.is_recording.return_value = True
        mock_span_context = Mock()
        mock_span_context.trace_id = 0x123456789ABCDEF
        mock_span_context.span_id = 0xFEDCBA987654321
        mock_span_context.trace_flags = 1
        mock_span.get_span_context.return_value = mock_span_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            assert "trace_id" in result
            assert result["trace_id"] == "00000000000000000123456789abcdef"
            assert "span_id" in result
            assert result["span_id"] == "0fedcba987654321"
            assert "trace_flags" in result
            assert result["trace_flags"] == 1

    def test_inject_trace_context_otel_not_recording(self) -> None:
        """Test when OpenTelemetry span exists but is not recording."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        mock_span = Mock()
        mock_span.is_recording.return_value = False

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            # Should fall through to Foundation tracer
            mock_foundation_span = Mock()
            mock_foundation_span.trace_id = "foundation-trace-123"
            mock_foundation_span.span_id = "foundation-span-456"

            with (
                patch(
                    "provide.foundation.tracer.context.get_current_trace_id",
                    return_value="foundation-trace-123",
                ),
                patch(
                    "provide.foundation.tracer.context.get_current_span",
                    return_value=mock_foundation_span,
                ),
            ):
                event_dict = {"event": "test"}
                result = inject_trace_context(None, "info", event_dict)

                assert result["trace_id"] == "foundation-trace-123"
                assert result["span_id"] == "foundation-span-456"

    def test_inject_trace_context_otel_exception(self) -> None:
        """Test handling exception in OpenTelemetry code."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.side_effect = Exception("OTEL Error")

            # Should catch exception and fall through to Foundation tracer
            mock_fallback_span = Mock()
            mock_fallback_span.trace_id = "fallback-trace"
            mock_fallback_span.span_id = "fallback-span"

            with (
                patch(
                    "provide.foundation.tracer.context.get_current_trace_id",
                    return_value="fallback-trace",
                ),
                patch(
                    "provide.foundation.tracer.context.get_current_span",
                    return_value=mock_fallback_span,
                ),
            ):
                event_dict = {"event": "test"}
                result = inject_trace_context(None, "info", event_dict)

                assert result["trace_id"] == "fallback-trace"
                assert result["span_id"] == "fallback-span"

    def test_inject_trace_context_no_trace_flags(self) -> None:
        """Test when OpenTelemetry span has no trace flags."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        mock_span = Mock()
        mock_span.is_recording.return_value = True
        mock_span_context = Mock()
        mock_span_context.trace_id = 0xABC
        mock_span_context.span_id = 0xDEF
        mock_span_context.trace_flags = 0  # No flags
        mock_span.get_span_context.return_value = mock_span_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            assert "trace_id" in result
            assert "span_id" in result
            # trace_flags should not be added when it's 0
            assert "trace_flags" not in result or result["trace_flags"] == 0


class TestShouldInjectTraceContextOtel(FoundationTestCase):
    """Test should_inject_trace_context with OpenTelemetry."""

    def test_should_inject_with_otel_active_span(self) -> None:
        """Test should inject when OpenTelemetry has active span."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        mock_span = Mock()
        mock_span.is_recording.return_value = True

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            assert should_inject_trace_context() is True

    def test_should_not_inject_otel_not_recording(self) -> None:
        """Test should not inject when OpenTelemetry span not recording."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        mock_span = Mock()
        mock_span.is_recording.return_value = False

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            # Falls through to check Foundation tracer
            with (
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

    def test_should_inject_otel_exception_foundation_fallback(self) -> None:
        """Test fallback to Foundation when OpenTelemetry fails."""
        from provide.foundation.logger.processors.trace import (
            should_inject_trace_context,
        )

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.side_effect = Exception("OTEL Error")

            # Should fall through to Foundation check
            with patch(
                "provide.foundation.tracer.context.get_current_span",
                return_value=Mock(),
            ):
                assert should_inject_trace_context() is True


class TestTraceProcessorOtelLogging(FoundationTestCase):
    """Test logging behavior with OpenTelemetry."""

    def test_debug_logging_on_successful_otel_injection(self) -> None:
        """Test successful OpenTelemetry trace injection (no internal logging)."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        mock_span = Mock()
        mock_span.is_recording.return_value = True
        mock_span_context = Mock()
        mock_span_context.trace_id = 0x123
        mock_span_context.span_id = 0x456
        mock_span_context.trace_flags = 1
        mock_span.get_span_context.return_value = mock_span_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.return_value = mock_span

            event_dict = {"event": "test"}
            result = inject_trace_context(None, "info", event_dict)

            # Check trace context was injected
            assert "trace_id" in result
            assert "span_id" in result
            assert result["trace_id"] == f"{0x123:032x}"
            assert result["span_id"] == f"{0x456:016x}"

    def test_debug_logging_on_otel_failure(self) -> None:
        """Test OpenTelemetry failure handling (fallback to Foundation tracer)."""
        from provide.foundation.logger.processors.trace import inject_trace_context

        with (
            patch("provide.foundation.logger.processors.trace._HAS_OTEL", True),
            patch(
                "provide.foundation.logger.processors.trace.otel_trace_runtime",
            ) as mock_otel,
        ):
            mock_otel.get_current_span.side_effect = ValueError("Test error")

            with patch(
                "provide.foundation.tracer.context.get_current_trace_id",
                return_value="foundation_trace_123",
            ):
                event_dict = {"event": "test"}
                result = inject_trace_context(None, "info", event_dict)

                # Check fallback to Foundation tracer worked
                assert "trace_id" in result
                assert result["trace_id"] == "foundation_trace_123"


# 🧱🏗️🔚
