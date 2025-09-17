"""Comprehensive tests for logger/processors/trace.py module."""

from unittest.mock import Mock, patch


class TestTraceProcessorWithOtel:
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


class TestTraceProcessorWithoutOtel:
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


class TestTraceProcessorImports:
    """Test module imports and dependencies."""

    def test_module_imports(self) -> None:
        """Test that the module can be imported."""
        from provide.foundation.logger.processors import trace

        assert trace is not None
        assert hasattr(trace, "inject_trace_context")

    def test_has_otel_flag(self) -> None:
        """Test _HAS_OTEL flag exists."""
        from provide.foundation.logger.processors import trace

        assert hasattr(trace, "_HAS_OTEL")
        assert isinstance(trace._HAS_OTEL, bool)

    def test_otel_import_handling(self) -> None:
        """Test OpenTelemetry import is handled properly."""
        # This test verifies the module handles OpenTelemetry imports
        from provide.foundation.logger.processors import trace

        # The module should handle OpenTelemetry availability
        assert hasattr(trace, "_HAS_OTEL")
        assert isinstance(trace._HAS_OTEL, bool)

        # If OpenTelemetry is available, _HAS_OTEL should be True
        # If not, it should be False and otel_trace_runtime should be None
        if trace._HAS_OTEL:
            assert trace.otel_trace_runtime is not None
        else:
            assert trace.otel_trace_runtime is None


class TestShouldInjectTraceContext:
    """Test should_inject_trace_context function."""

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


class TestTraceProcessorLogging:
    """Test logging behavior in trace processor."""

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
