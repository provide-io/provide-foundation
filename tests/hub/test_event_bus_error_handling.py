#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive error handling tests for EventBus.

Tests that event handler errors are properly logged and isolated,
ensuring one failing handler doesn't break the entire event system."""

from __future__ import annotations

from io import StringIO
import threading

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch

from provide.foundation.hub.events import Event, EventBus, RegistryEvent


class TestEventBusErrorHandling(FoundationTestCase):
    """Test EventBus error handling and isolation."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.bus = EventBus()
        self.calls: list[str] = []

    def test_handler_exception_is_logged_to_stderr(self) -> None:
        """Test that handler exceptions are logged to stderr."""

        def failing_handler(event: Event) -> None:
            raise ValueError("Test error")

        self.bus.subscribe("test.event", failing_handler)

        # Capture stderr
        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            event = Event(name="test.event", data={})
            self.bus.emit(event)

            # Check that error was logged to stderr
            stderr_output = mock_stderr.getvalue()
            assert "ERROR: Event handler failed" in stderr_output
            assert "test.event" in stderr_output
            assert "failing_handler" in stderr_output
            assert "ValueError" in stderr_output
            assert "Test error" in stderr_output

    def test_failed_handler_does_not_break_other_handlers(self) -> None:
        """Test that one failing handler doesn't prevent others from running."""

        def handler1(event: Event) -> None:
            self.calls.append("handler1")

        def failing_handler(event: Event) -> None:
            self.calls.append("failing")
            raise RuntimeError("Handler failed")

        def handler3(event: Event) -> None:
            self.calls.append("handler3")

        # Subscribe all three handlers
        self.bus.subscribe("test.event", handler1)
        self.bus.subscribe("test.event", failing_handler)
        self.bus.subscribe("test.event", handler3)

        # Emit event
        with patch("sys.stderr", new=StringIO()):
            event = Event(name="test.event")
            self.bus.emit(event)

        # All handlers should have been called
        assert "handler1" in self.calls
        assert "failing" in self.calls
        assert "handler3" in self.calls

    def test_error_stats_track_failures(self) -> None:
        """Test that error statistics correctly track handler failures."""

        def failing_handler(event: Event) -> None:
            raise ValueError("Error 1")

        def another_failing_handler(event: Event) -> None:
            raise TypeError("Error 2")

        self.bus.subscribe("test.event", failing_handler)
        self.bus.subscribe("test.event", another_failing_handler)

        # Emit event (both handlers fail)
        with patch("sys.stderr", new=StringIO()):
            event = Event(name="test.event")
            self.bus.emit(event)

        # Check error stats
        stats = self.bus.get_error_stats()
        assert stats["failed_handler_count"] == 2
        assert len(stats["recent_errors"]) == 2

        # Check error details
        errors = stats["recent_errors"]
        assert errors[0]["event_name"] == "test.event"
        assert errors[0]["error_type"] == "ValueError"
        assert errors[0]["error_message"] == "Error 1"

        assert errors[1]["event_name"] == "test.event"
        assert errors[1]["error_type"] == "TypeError"
        assert errors[1]["error_message"] == "Error 2"

    def test_error_stats_limited_to_10_recent(self) -> None:
        """Test that error history is limited to 10 most recent errors."""

        def failing_handler(event: Event) -> None:
            raise ValueError(f"Error {event.data['count']}")

        self.bus.subscribe("test.event", failing_handler)

        # Generate 15 errors
        with patch("sys.stderr", new=StringIO()):
            for i in range(15):
                event = Event(name="test.event", data={"count": i})
                self.bus.emit(event)

        stats = self.bus.get_error_stats()
        assert stats["failed_handler_count"] == 15
        # Only last 10 errors kept
        assert len(stats["recent_errors"]) == 10
        # Should have errors 5-14 (dropped 0-4)
        assert stats["recent_errors"][0]["error_message"] == "Error 5"
        assert stats["recent_errors"][-1]["error_message"] == "Error 14"

    def test_clear_resets_error_stats(self) -> None:
        """Test that clear() resets error statistics."""

        def failing_handler(event: Event) -> None:
            raise ValueError("Test error")

        self.bus.subscribe("test.event", failing_handler)

        with patch("sys.stderr", new=StringIO()):
            event = Event(name="test.event")
            self.bus.emit(event)

        # Verify error was tracked
        assert self.bus.get_error_stats()["failed_handler_count"] == 1

        # Clear and verify reset
        self.bus.clear()
        stats = self.bus.get_error_stats()
        assert stats["failed_handler_count"] == 0
        assert len(stats["recent_errors"]) == 0

    def test_multiple_events_with_mixed_success_failure(self) -> None:
        """Test multiple events where some handlers succeed and some fail."""

        def success_handler(event: Event) -> None:
            self.calls.append(f"success-{event.name}")

        def failing_handler(event: Event) -> None:
            self.calls.append(f"fail-{event.name}")
            if event.name == "test.event.2":
                raise RuntimeError("Only fail on event 2")

        self.bus.subscribe("test.event.1", success_handler)
        self.bus.subscribe("test.event.1", failing_handler)
        self.bus.subscribe("test.event.2", success_handler)
        self.bus.subscribe("test.event.2", failing_handler)

        with patch("sys.stderr", new=StringIO()):
            self.bus.emit(Event(name="test.event.1"))
            self.bus.emit(Event(name="test.event.2"))

        # Both events should have called both handlers
        assert "success-test.event.1" in self.calls
        assert "fail-test.event.1" in self.calls
        assert "success-test.event.2" in self.calls
        assert "fail-test.event.2" in self.calls

        # Only one error (from event 2)
        assert self.bus.get_error_stats()["failed_handler_count"] == 1

    def test_weakref_cleanup_works_after_handler_error(self) -> None:
        """Test that weakref cleanup still works when handlers fail."""

        def create_failing_handler() -> callable:
            def handler(event: Event) -> None:
                raise ValueError("Test error")

            return handler

        # Create and subscribe handler
        handler = create_failing_handler()
        self.bus.subscribe("test.event", handler)

        # Emit event (handler fails)
        with patch("sys.stderr", new=StringIO()):
            self.bus.emit(Event(name="test.event"))

        # Delete handler reference
        del handler

        # Force cleanup
        self.bus.force_cleanup()

        # Handler should be gone
        mem_stats = self.bus.get_memory_stats()
        assert mem_stats["dead_handlers"] == 0
        assert mem_stats["live_handlers"] == 0

    def test_registry_event_handler_errors(self) -> None:
        """Test error handling with RegistryEvent."""

        def failing_handler(event: RegistryEvent) -> None:
            raise TypeError("Registry handler failed")

        self.bus.subscribe("registry.register", failing_handler)

        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            event = RegistryEvent(
                name="registry.register",
                operation="register",
                item_name="test_component",
                dimension="component",
            )
            self.bus.emit(event)

            # Verify error logged
            stderr_output = mock_stderr.getvalue()
            assert "ERROR: Event handler failed" in stderr_output
            assert "registry.register" in stderr_output
            assert "TypeError" in stderr_output


class TestEventBusConcurrentErrorHandling(FoundationTestCase):
    """Test EventBus error handling under concurrent access."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.bus = EventBus()

    def test_concurrent_handler_failures_thread_safe(self) -> None:
        """Test that concurrent handler failures are thread-safe."""
        errors_per_thread = 10
        num_threads = 5

        def failing_handler(event: Event) -> None:
            raise RuntimeError(f"Thread error: {event.data['thread_id']}")

        self.bus.subscribe("test.event", failing_handler)

        def emit_events(thread_id: int) -> None:
            with patch("sys.stderr", new=StringIO()):
                for i in range(errors_per_thread):
                    event = Event(name="test.event", data={"thread_id": thread_id, "count": i})
                    self.bus.emit(event)

        # Start threads
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=emit_events, args=(i,))
            threads.append(t)
            t.start()

        # Wait for completion
        for t in threads:
            t.join()

        # All errors should be counted
        stats = self.bus.get_error_stats()
        assert stats["failed_handler_count"] == num_threads * errors_per_thread

        # Recent errors limited to 10
        assert len(stats["recent_errors"]) == 10

    def test_concurrent_emit_with_mixed_handlers(self) -> None:
        """Test concurrent emits with mix of successful and failing handlers."""
        calls = []
        lock = threading.Lock()

        def success_handler(event: Event) -> None:
            with lock:
                calls.append("success")

        def failing_handler(event: Event) -> None:
            with lock:
                calls.append("fail")
            raise ValueError("Concurrent failure")

        self.bus.subscribe("test.event", success_handler)
        self.bus.subscribe("test.event", failing_handler)

        def emit_many() -> None:
            with patch("sys.stderr", new=StringIO()):
                for _ in range(20):
                    self.bus.emit(Event(name="test.event"))

        # Run from multiple threads
        threads = []
        for _ in range(3):
            t = threading.Thread(target=emit_many)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Both handlers should have been called many times
        success_count = calls.count("success")
        fail_count = calls.count("fail")
        assert success_count == 60  # 3 threads * 20 emits
        assert fail_count == 60


class TestEventBusEdgeCases(FoundationTestCase):
    """Test EventBus edge cases and corner scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.bus = EventBus()

    def test_no_handlers_no_errors(self) -> None:
        """Test that emitting event with no handlers doesn't error."""
        # Should not raise
        event = Event(name="no.handlers")
        self.bus.emit(event)

        # No errors tracked
        assert self.bus.get_error_stats()["failed_handler_count"] == 0

    def test_handler_modifies_event_during_failure(self) -> None:
        """Test handler that modifies event data before failing."""

        def modifying_failing_handler(event: Event) -> None:
            # Try to modify frozen event (will fail because attrs frozen=True)
            # This tests that the error is caught and logged
            raise AttributeError("Cannot modify frozen event")

        self.bus.subscribe("test.event", modifying_failing_handler)

        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            event = Event(name="test.event", data={"key": "value"})
            self.bus.emit(event)

            # Error should be logged
            assert "AttributeError" in mock_stderr.getvalue()

        # Error tracked
        assert self.bus.get_error_stats()["failed_handler_count"] == 1

    def test_handler_with_no_name_attribute(self) -> None:
        """Test handler without __name__ attribute gets repr() in logs."""

        class CallableWithoutName:
            def __call__(self, event: Event) -> None:
                raise ValueError("Custom callable failed")

        handler = CallableWithoutName()
        self.bus.subscribe("test.event", handler)

        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            self.bus.emit(Event(name="test.event"))

            stderr_output = mock_stderr.getvalue()
            # Should use repr() since no __name__
            assert "CallableWithoutName" in stderr_output

    def test_error_record_includes_event_source(self) -> None:
        """Test that error records include event source when available."""

        def failing_handler(event: Event) -> None:
            raise RuntimeError("Handler failed")

        self.bus.subscribe("test.event", failing_handler)

        with patch("sys.stderr", new=StringIO()):
            event = Event(name="test.event", source="test_source")
            self.bus.emit(event)

        stats = self.bus.get_error_stats()
        assert stats["recent_errors"][0]["event_source"] == "test_source"

    def test_handler_raises_during_weakref_cleanup(self) -> None:
        """Test that errors during weakref processing don't break the system."""
        calls = []

        def handler1(event: Event) -> None:
            calls.append("handler1")

        def handler2(event: Event) -> None:
            calls.append("handler2")
            raise ValueError("Handler2 failed")

        self.bus.subscribe("test.event", handler1)
        self.bus.subscribe("test.event", handler2)

        with patch("sys.stderr", new=StringIO()):
            self.bus.emit(Event(name="test.event"))

        # Both handlers called
        assert "handler1" in calls
        assert "handler2" in calls

        # Error tracked
        assert self.bus.get_error_stats()["failed_handler_count"] == 1


# 🧱🏗️🔚
