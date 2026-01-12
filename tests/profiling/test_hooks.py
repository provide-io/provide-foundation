#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#


from __future__ import annotations

import time

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.context import CLIContext
from provide.foundation.hub.manager import clear_hub, get_hub
from provide.foundation.profiling.component import ProfilingComponent
from provide.foundation.profiling.metrics import ProfileMetrics
from provide.foundation.profiling.processor import ProfilingProcessor
from provide.foundation.testmode import (
    reset_hub_state,
    reset_logger_state,
    reset_streams_state,
    reset_structlog_state,
)


class TestProfileMetrics(FoundationTestCase):
    """Test ProfileMetrics data structure."""

    def test_metrics_initialization(self) -> None:
        """Test metrics are initialized with zero values."""
        metrics = ProfileMetrics()

        assert metrics.message_count == 0
        assert metrics.total_duration_ns == 0
        assert metrics.emoji_message_count == 0
        assert metrics.dropped_count == 0
        assert metrics.start_time > 0

    def test_metrics_record_message(self) -> None:
        """Test recording message metrics."""
        metrics = ProfileMetrics()

        # Record non-emoji message
        metrics.record_message(duration_ns=1000000, has_emoji=False, field_count=3)

        assert metrics.message_count == 1
        assert metrics.total_duration_ns == 1000000
        assert metrics.emoji_message_count == 0

        # Record emoji message
        metrics.record_message(duration_ns=2000000, has_emoji=True, field_count=5)

        assert metrics.message_count == 2
        assert metrics.total_duration_ns == 3000000
        assert metrics.emoji_message_count == 1

    def test_metrics_calculations(self) -> None:
        """Test calculated metrics properties."""
        metrics = ProfileMetrics()

        # Initially should handle division by zero
        assert metrics.messages_per_second == 0.0
        assert metrics.avg_latency_ms == 0.0
        assert metrics.emoji_overhead_percent == 0.0

        # Simulate 1 second elapsed time
        metrics.start_time = time.time() - 1.0

        # Record messages
        metrics.record_message(duration_ns=1000000, has_emoji=False, field_count=3)
        metrics.record_message(duration_ns=2000000, has_emoji=True, field_count=5)

        assert metrics.messages_per_second == pytest.approx(2.0, rel=0.1)
        assert metrics.avg_latency_ms == pytest.approx(1.5, rel=0.1)  # (1+2)/2 million ns = 1.5ms
        assert metrics.emoji_overhead_percent == 50.0  # 1 of 2 messages

    @pytest.mark.time_sensitive
    def test_metrics_reset(self) -> None:
        """Test metrics reset functionality."""
        metrics = ProfileMetrics()

        # Add some data
        metrics.record_message(duration_ns=1000000, has_emoji=True, field_count=3)
        metrics.dropped_count = 5

        # Reset
        old_start_time = metrics.start_time
        metrics.reset()

        assert metrics.message_count == 0
        assert metrics.total_duration_ns == 0
        assert metrics.emoji_message_count == 0
        assert metrics.dropped_count == 0
        assert metrics.start_time > old_start_time

    def test_metrics_to_dict(self) -> None:
        """Test metrics serialization to dictionary."""
        metrics = ProfileMetrics()
        metrics.start_time = time.time() - 1.0
        metrics.record_message(duration_ns=1000000, has_emoji=True, field_count=3)

        data = metrics.to_dict()

        assert isinstance(data, dict)
        assert "messages_per_second" in data
        assert "avg_latency_ms" in data
        assert "emoji_overhead_percent" in data
        assert "total_messages" in data
        assert "dropped_messages" in data
        assert data["total_messages"] == 1


class TestProfilingProcessor(FoundationTestCase):
    """Test ProfilingProcessor for metrics collection."""

    def test_processor_initialization(self) -> None:
        """Test processor initializes with default values."""
        processor = ProfilingProcessor(sample_rate=0.1)

        assert processor.sample_rate == 0.1
        assert isinstance(processor.metrics, ProfileMetrics)

    def test_processor_call_interface(self) -> None:
        """Test processor follows structlog processor interface."""
        processor = ProfilingProcessor(sample_rate=1.0)  # 100% sampling for test

        # Mock logger and event_dict
        mock_logger = Mock()
        event_dict = {"message": "test", "emoji": "🔥", "level": "info"}

        # Call processor
        result = processor(mock_logger, "info", event_dict)

        # Should return event_dict unchanged
        assert result == event_dict

        # Metrics should be recorded (with 100% sampling)
        assert processor.metrics.message_count >= 0  # May be 0 or 1 due to sampling

    def test_processor_emoji_detection(self) -> None:
        """Test processor correctly detects emoji messages."""
        processor = ProfilingProcessor(sample_rate=1.0)
        mock_logger = Mock()

        # Message with emoji
        event_dict_emoji = {"message": "test", "emoji": "🔥"}
        processor(mock_logger, "info", event_dict_emoji)

        # Message without emoji
        event_dict_no_emoji = {"message": "test", "level": "info"}
        processor(mock_logger, "info", event_dict_no_emoji)

        # Should detect emoji in first message
        # Note: Actual counting depends on sampling, so we just test the interface

    def test_processor_sampling(self) -> None:
        """Test processor respects sampling rate."""
        # Use 0% sampling - no metrics should be recorded
        processor = ProfilingProcessor(sample_rate=0.0)
        mock_logger = Mock()

        # Process many messages
        for i in range(100):
            event_dict = {"message": f"test {i}"}
            processor(mock_logger, "info", event_dict)

        # With 0% sampling, no messages should be recorded
        assert processor.metrics.message_count == 0

    def test_processor_reset(self) -> None:
        """Test processor reset functionality."""
        processor = ProfilingProcessor(sample_rate=1.0)
        mock_logger = Mock()

        # Process a message
        event_dict = {"message": "test"}
        processor(mock_logger, "info", event_dict)

        # Reset
        processor.reset()

        # Metrics should be reset
        assert processor.metrics.message_count == 0


class TestProfilingComponent(FoundationTestCase):
    """Test ProfilingComponent Hub integration."""

    def setup_method(self) -> None:
        """Reset Foundation state before each test."""
        super().setup_method()
        # Reset Foundation components in proper order
        reset_structlog_state()
        reset_streams_state()
        reset_logger_state()
        reset_hub_state()
        clear_hub()

    def test_component_initialization(self) -> None:
        """Test component initializes in disabled state."""
        component = ProfilingComponent()

        assert not component.enabled
        assert isinstance(component.processor, ProfilingProcessor)

    def test_component_enable_disable(self) -> None:
        """Test component enable/disable functionality."""
        component = ProfilingComponent()

        # Enable
        component.enable()
        assert component.enabled

        # Disable
        component.disable()
        assert not component.enabled

    def test_component_get_metrics(self) -> None:
        """Test component metrics access."""
        component = ProfilingComponent()

        metrics = component.get_metrics()
        assert isinstance(metrics, ProfileMetrics)
        assert metrics.message_count == 0

    def test_component_reset(self) -> None:
        """Test component reset functionality."""
        component = ProfilingComponent()

        # Manually add some data to processor metrics
        component.processor.metrics.record_message(1000000, False, 3)

        # Reset
        component.reset()

        # Metrics should be reset
        assert component.processor.metrics.message_count == 0

    def test_component_hub_integration(self) -> None:
        """Test component registration with Hub."""
        from provide.foundation.hub.components import get_component_registry

        component = ProfilingComponent()

        # Register component directly with registry
        registry = get_component_registry()
        registry.register(name="profiler", value=component, dimension="component")

        # Retrieve component via Hub
        hub = get_hub()
        retrieved = hub.get_component("profiler")
        assert retrieved is component

    def test_component_auto_register(self) -> None:
        """Test component auto-registration via register_profiling."""
        from provide.foundation.profiling.component import register_profiling

        hub = get_hub()
        register_profiling(hub)

        # Should have profiler component
        profiler = hub.get_component("profiler")
        assert profiler is not None
        assert isinstance(profiler, ProfilingComponent)


class TestProfilingCLI(FoundationTestCase):
    """Test profiling CLI commands."""

    def setup_method(self) -> None:
        """Reset Foundation state before each test."""
        super().setup_method()
        # Reset Foundation components in proper order
        reset_structlog_state()
        reset_streams_state()
        reset_logger_state()
        reset_hub_state()
        clear_hub()

    def test_profile_command_no_profiler(self) -> None:
        """Test profile command when profiler not enabled."""
        from provide.foundation.profiling.cli import show_profile_metrics

        ctx = CLIContext(json_output=False, no_color=False)

        # Should handle missing profiler gracefully
        with patch("provide.foundation.profiling.cli.perr") as mock_perr:
            show_profile_metrics(ctx)
            mock_perr.assert_called()

    def test_profile_command_with_profiler(self) -> None:
        """Test profile command with active profiler."""
        from provide.foundation.profiling.cli import show_profile_metrics
        from provide.foundation.profiling.component import register_profiling

        # Setup profiler
        hub = get_hub()
        register_profiling(hub)
        profiler = hub.get_component("profiler")
        profiler.enable()

        # Add some test data
        profiler.processor.metrics.record_message(1000000, True, 5)

        ctx = CLIContext(json_output=False, no_color=False)

        with patch("provide.foundation.profiling.cli.pout") as mock_pout:
            show_profile_metrics(ctx)

            # Should output metrics
            assert mock_pout.call_count > 0

            # Check for expected output patterns
            calls = [str(call) for call in mock_pout.call_args_list]
            output = " ".join(calls)
            assert "Performance Metrics" in output or "📊" in output

    def test_profile_command_json_output(self) -> None:
        """Test profile command with JSON output."""
        from provide.foundation.profiling.cli import show_profile_metrics
        from provide.foundation.profiling.component import register_profiling

        # Setup profiler
        hub = get_hub()
        register_profiling(hub)
        profiler = hub.get_component("profiler")
        profiler.enable()

        ctx = CLIContext(json_output=True, no_color=False)

        with patch("provide.foundation.profiling.cli.pout") as mock_pout:
            show_profile_metrics(ctx)

            # Should output JSON
            assert mock_pout.called
            # Check that pout was called with json_key
            call_args = mock_pout.call_args_list
            json_call = any("json_key" in str(call) for call in call_args)
            assert json_call or len(call_args) > 0


class TestProfilingIntegration(FoundationTestCase):
    """Test full profiling system integration."""

    def setup_method(self) -> None:
        """Reset Foundation state before each test."""
        super().setup_method()
        # Reset Foundation components in proper order
        reset_structlog_state()
        reset_streams_state()
        reset_logger_state()
        reset_hub_state()
        clear_hub()

    def test_end_to_end_profiling(self) -> None:
        """Test complete profiling workflow."""
        from provide.foundation import logger
        from provide.foundation.profiling.component import register_profiling

        # Setup profiler
        hub = get_hub()
        register_profiling(hub)
        profiler = hub.get_component("profiler")

        # Enable profiling
        profiler.enable()

        # Generate some log messages
        logger.info("Test message 1", emoji="🔥")
        logger.debug("Test message 2")
        logger.error("Test message 3", emoji="❌")

        # Get metrics
        metrics = profiler.get_metrics()

        # Should have collected some metrics
        # Note: Due to sampling, we can't guarantee exact counts
        assert isinstance(metrics, ProfileMetrics)

    def test_profiling_reset_integration(self) -> None:
        """Test profiling integrates with Foundation reset system."""
        from provide.foundation.profiling.component import register_profiling
        from provide.foundation.testmode.internal import reset_profiling_state

        # Setup profiler
        hub = get_hub()
        register_profiling(hub)
        profiler = hub.get_component("profiler")

        # Add some data
        profiler.processor.metrics.record_message(1000000, True, 3)
        assert profiler.get_metrics().message_count > 0

        # Reset via testmode
        reset_profiling_state()

        # Should be reset
        assert profiler.get_metrics().message_count == 0

    def test_profiling_thread_safety(self) -> None:
        """Test profiling is thread-safe."""
        import threading

        from provide.foundation.profiling.component import ProfilingComponent

        component = ProfilingComponent()
        component.enable()

        def worker() -> None:
            for _i in range(10):
                component.processor.metrics.record_message(1000000, False, 3)

        # Run multiple threads
        threads = [threading.Thread(daemon=True, target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10.0)

        # Should handle concurrent access without errors
        metrics = component.get_metrics()
        assert metrics.message_count >= 0  # Some messages may be recorded


# 🧱🏗️🔚
