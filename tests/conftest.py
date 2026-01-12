#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pytest configuration and global fixtures for provide-foundation tests.

This file contains only the essential global fixtures and configuration
that must be at the root level for pytest.

All tests should inherit from FoundationTestCase which handles
Foundation reset automatically."""

from __future__ import annotations

from collections.abc import Generator
import logging as stdlib_logging
import os
import sys

import provide.testkit  # noqa: F401 - Installs setproctitle blocker early
import pytest

# Mock opentelemetry module for tests when it's not available
# This must be done before any test imports try to use OTLP client
if "opentelemetry" not in sys.modules:
    from unittest.mock import MagicMock

    mock_opentelemetry = MagicMock()

    # Mock _logs submodule
    mock_opentelemetry._logs = MagicMock()
    mock_opentelemetry._logs.LogRecord = MagicMock()
    mock_opentelemetry._logs.SeverityNumber = MagicMock()

    # Mock trace submodule for trace context extraction

    mock_trace = MagicMock()
    mock_span = MagicMock()
    mock_span_context = MagicMock()

    # Configure span to return a valid but empty span context
    mock_span.is_recording.return_value = True
    mock_span.get_span_context.return_value = mock_span_context
    mock_span_context.is_valid = False  # Mark as invalid so trace context won't be extracted

    # Create proper mock trace and span IDs that support formatting
    class FormattableMock(MagicMock):
        """Mock that supports format() operations."""

        def __format__(self, format_spec):
            if format_spec == "032x":
                return "0" * 32
            elif format_spec == "016x":
                return "0" * 16
            return str(self)

    mock_span_context.trace_id = FormattableMock()
    mock_span_context.span_id = FormattableMock()

    mock_trace.get_current_span.return_value = mock_span
    mock_opentelemetry.trace = mock_trace

    # Mock SDK resources for resource creation
    mock_sdk = MagicMock()
    mock_resources = MagicMock()
    mock_resources.Resource = MagicMock()
    mock_sdk.resources = mock_resources
    mock_opentelemetry.sdk = mock_sdk

    # Register all modules
    sys.modules["opentelemetry"] = mock_opentelemetry
    sys.modules["opentelemetry._logs"] = mock_opentelemetry._logs
    sys.modules["opentelemetry.trace"] = mock_trace
    sys.modules["opentelemetry.sdk"] = mock_sdk
    sys.modules["opentelemetry.sdk.resources"] = mock_resources

# Register plugins for assertion rewriting at the root level
pytest_plugins = [
    "provide.testkit.hub.fixtures",
]

# Set DEBUG log level for all tests
os.environ.setdefault("PROVIDE_LOG_LEVEL", "DEBUG")

# Temporarily suppress testing warnings only for the import
with_suppression = os.environ.get("FOUNDATION_SUPPRESS_TESTING_WARNINGS")
os.environ["FOUNDATION_SUPPRESS_TESTING_WARNINGS"] = "true"

import contextlib

from provide.testkit import set_log_stream_for_testing  # type: ignore

# Restore original warning suppression state
if with_suppression is None:
    os.environ.pop("FOUNDATION_SUPPRESS_TESTING_WARNINGS", None)
else:
    os.environ["FOUNDATION_SUPPRESS_TESTING_WARNINGS"] = with_suppression

_conftest_diag_logger_name = "provide.foundation.conftest_diag"


def _get_conftest_diag_logger() -> stdlib_logging.Logger:
    """Initializes and returns a diagnostic logger for conftest operations."""
    logger = stdlib_logging.getLogger(_conftest_diag_logger_name)
    if not logger.handlers:
        handler = stdlib_logging.StreamHandler(
            sys.stderr,
        )  # Actual stderr for diagnostics
        formatter = stdlib_logging.Formatter(
            "[Conftest DIAG] %(levelname)s (%(name)s): %(message)s",
        )
        handler.setFormatter(formatter)
        level_str = os.getenv("PYTEST_CONTEST_DIAG_LOG_LEVEL", "DEBUG").upper()
        level = getattr(stdlib_logging, level_str, stdlib_logging.DEBUG)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
    return logger


conftest_diag_logger = _get_conftest_diag_logger()
if not os.getenv("PYTEST_WORKER_ID"):  # Avoid multiple messages with xdist
    pass  # Placeholder for potential diagnostic logging

# Removed no_cover hook - not needed, issue is time_machine + asyncio, not coverage


@pytest.fixture(autouse=True, scope="function")
def _intercept_event_loop_creation(request: pytest.FixtureRequest) -> Generator[None]:
    """Intercept asyncio event loop creation to ensure time is unfrozen.

    This fixture patches asyncio.new_event_loop() to forcibly stop all time_machine
    patches BEFORE creating new event loops. This ensures loops are created with
    correct time.monotonic references, not frozen ones.

    CRITICAL FIX: Must ALWAYS activate (not just for time_machine tests) because
    time_machine patches can persist from PREVIOUS tests, corrupting async tests
    that follow time_machine tests in serial execution.
    """
    import asyncio

    original_new_event_loop = asyncio.new_event_loop

    def ensure_time_unfrozen() -> None:
        """Ensure time is unfrozen before event loop operations."""
        try:
            from unittest.mock import _patch

            from provide.testkit.time.classes import get_active_time_machines

            # Use registry to find and cleanup frozen TimeMachines - O(1) instead of O(n)
            for machine in get_active_time_machines():
                if machine.is_frozen:
                    with contextlib.suppress(Exception):
                        machine.cleanup()

            # Also scan for any orphaned _patch objects for time functions
            # This handles edge cases where patches exist without associated TimeMachines
            import gc

            for obj in gc.get_objects():
                if isinstance(obj, _patch):
                    try:
                        if hasattr(obj, "attribute") and obj.attribute in ("time", "monotonic"):
                            obj.stop()
                    except Exception:
                        pass

        except Exception:
            pass

    def patched_new_event_loop() -> asyncio.AbstractEventLoop:
        """Create new event loop after ensuring time is unfrozen."""
        ensure_time_unfrozen()
        return original_new_event_loop()

    original_get_event_loop = asyncio.get_event_loop

    def patched_get_event_loop() -> asyncio.AbstractEventLoop:
        """Get event loop after ensuring time is unfrozen."""
        # If there's no current loop, we'll create a new one - ensure time is unfrozen first
        try:
            loop = original_get_event_loop()
            # Loop exists and is not closed, ensure it wasn't created with frozen time
            if not loop.is_closed():
                ensure_time_unfrozen()
            return loop
        except RuntimeError:
            # No current event loop - create a new one with unfrozen time
            ensure_time_unfrozen()
            # Create and set a new loop (don't call get_event_loop again - it will just error)
            new_loop = original_new_event_loop()
            asyncio.set_event_loop(new_loop)
            return new_loop

    # Patch both new and get
    asyncio.new_event_loop = patched_new_event_loop
    asyncio.get_event_loop = patched_get_event_loop

    try:
        yield
    finally:
        # Restore original functions
        asyncio.new_event_loop = original_new_event_loop
        asyncio.get_event_loop = original_get_event_loop

        # NOTE: We do NOT close event loops here because:
        # 1. Pytest manages event loop lifecycle for async tests
        # 2. Closing loops here can interfere with subsequent async tests in serial execution
        # 3. The reset_foundation_for_all_tests fixture handles cleanup after each test


@pytest.fixture(autouse=True)
def reset_foundation_for_all_tests(request: pytest.FixtureRequest) -> Generator[None]:
    """Autouse fixture to reset Foundation state after each test.

    This ensures ALL tests get Foundation reset after completion, preventing global
    Hub state pollution between tests. This is critical for parallel test execution
    where environment variables and Hub state can leak between tests.

    The reset happens in the finally block (after test completion) to ensure that:
    1. TestEnvironment context managers complete their cleanup first
    2. Any state from the test is fully cleared before the next test starts
    3. Environment variables set by the test don't affect the next test
    """

    from provide.testkit import reset_foundation_setup_for_testing

    try:
        yield
    finally:
        # ALWAYS reset Foundation after each test, regardless of test type
        # This ensures clean state for the next test in the worker
        reset_foundation_setup_for_testing()

        # If this test used time_machine, aggressively cleanup to prevent event loop corruption
        # This must happen IMMEDIATELY after test completes, before next test starts
        used_time_machine = "time_machine" in request.fixturenames
        if used_time_machine:
            try:
                import asyncio
                import gc
                from unittest.mock import _patch

                # Force stop all active time machines using testkit registry
                try:
                    from provide.testkit.time.classes import get_active_time_machines

                    for machine in get_active_time_machines():
                        with contextlib.suppress(Exception):
                            # Try stop() first (more forceful), then cleanup()
                            if hasattr(machine, "stop"):
                                machine.stop()
                            elif hasattr(machine, "cleanup"):
                                machine.cleanup()
                except Exception:
                    pass

                # Aggressively stop ANY mock patches on time functions
                # This handles cases where testkit's registry might not catch everything
                for obj in gc.get_objects():
                    if isinstance(obj, _patch):
                        try:
                            if hasattr(obj, "attribute") and obj.attribute in (
                                "time",
                                "monotonic",
                                "perf_counter",
                                "sleep",
                                "gmtime",
                                "localtime",
                                "strftime",
                            ):
                                with contextlib.suppress(Exception):
                                    obj.stop()
                        except Exception:
                            pass

                # Force gc to clean up any remaining patch references
                gc.collect()

                # CRITICAL: Close and clear the event loop that may have been corrupted by time_machine
                # The event loop was created with frozen time.monotonic, so it must be discarded
                try:
                    loop = asyncio.get_event_loop()
                    if loop and not loop.is_closed():
                        # Stop all running tasks
                        tasks = [t for t in asyncio.all_tasks(loop) if not t.done()]
                        for task in tasks:
                            task.cancel()
                        # Clear internal queues
                        if hasattr(loop, "_ready"):
                            loop._ready.clear()
                        if hasattr(loop, "_scheduled"):
                            loop._scheduled.clear()
                        # Close the loop
                        loop.close()
                except Exception:
                    pass

                # Clear the event loop so pytest-asyncio creates a fresh one for the next test
                with contextlib.suppress(Exception):
                    asyncio.set_event_loop(None)

            except Exception:
                pass

        # NOTE: We do NOT close event loops in normal cases because:
        # 1. pytest-asyncio manages event loop lifecycle
        # 2. Closing loops interferes with pytest-asyncio's cleanup
        # 3. Clearing event loop policy breaks subsequent async tests

        # NOTE: We do NOT remove modules from sys.modules because:
        # 1. Removing modules causes them to be re-imported
        # 2. Re-importing triggers module-level initialization code
        # 3. This can cause infinite loops (e.g., transport auto-registration)
        # 4. The reset_foundation_setup_for_testing() handles state cleanup
        # 5. Tests should use proper mocking instead of sys.modules patching

        # Ensure stream is reset to default stderr after each test
        # Handle potential closed streams during parallel execution
        from provide.foundation.errors.decorators import suppress_and_log

        @suppress_and_log(ValueError, OSError, log_level="debug")
        def reset_stream_safely() -> None:
            """Reset the log stream with automatic error suppression and logging."""
            return set_log_stream_for_testing(None)

        reset_stream_safely()


# Import and re-export fixtures from the unified testing module
from provide.testkit import (
    async_stream_reader,
    async_timeout,
    binary_file,
    ca_cert,
    captured_stderr_for_foundation,
    cert_with_extra_whitespace,
    cert_with_utf8_bom,
    cert_with_windows_line_endings,
    # New async fixtures
    clean_event_loop,
    # CLI fixtures
    click_testing_mode,
    # Logger fixtures
    client_cert,
    # Original fixtures
    default_container_directory,
    empty_cert,
    empty_directory,
    external_ca_pem,
    # New network fixtures
    free_port,
    httpx_mock_responses,
    invalid_cert_pem,
    invalid_key_pem,
    # New DI fixtures
    malformed_cert_pem,
    mock_async_process,
    mock_cache,
    # New mock fixtures
    mock_http_config,
    mock_logger,
    mock_server,
    mock_telemetry_config,
    mock_transport,
    nested_directory_structure,
    readonly_file,
    server_cert,
    setup_foundation_telemetry_for_test,
    # New file fixtures
    temp_directory,
    temp_file,
    temporary_cert_file,
    temporary_key_file,
    test_files_structure,
    # Time fixtures
    # time_machine,  # Not available in current testkit version
    valid_cert_pem,
    valid_key_pem,
)

# Re-export for pytest discovery
__all__ = [
    "async_stream_reader",
    "async_timeout",
    "binary_file",
    "ca_cert",
    # Original exports
    "captured_stderr_for_foundation",
    "cert_with_extra_whitespace",
    "cert_with_utf8_bom",
    "cert_with_windows_line_endings",
    # New async fixtures
    "clean_event_loop",
    # CLI exports
    "click_testing_mode",
    # Crypto fixtures
    "client_cert",
    "default_container_directory",
    "empty_cert",
    "empty_directory",
    "external_ca_pem",
    # New network fixtures
    "free_port",
    "httpx_mock_responses",
    "invalid_cert_pem",
    "invalid_key_pem",
    # New DI fixtures
    "malformed_cert_pem",
    "mock_async_process",
    "mock_cache",
    # New mock fixtures
    "mock_http_config",
    # Logger exports
    "mock_logger",
    "mock_server",
    "mock_telemetry_config",
    "mock_transport",
    "nested_directory_structure",
    "readonly_file",
    "server_cert",
    "setup_foundation_telemetry_for_test",
    # New file fixtures
    "temp_directory",
    "temp_file",
    "temporary_cert_file",
    "temporary_key_file",
    "test_files_structure",
    # Time fixtures
    # "time_machine",  # Not available in current testkit version
    "valid_cert_pem",
    "valid_key_pem",
    "benchmark",
]


# Only define benchmark fixture if pytest-benchmark is NOT installed
# This prevents shadowing the real benchmark fixture when it's available
try:
    import pytest_benchmark  # noqa: F401

    # pytest-benchmark is installed, it will provide the benchmark fixture
except ImportError:
    # pytest-benchmark not installed, provide a skip fixture
    @pytest.fixture
    def benchmark():
        """Benchmark fixture that skips when pytest-benchmark is not installed."""
        pytest.skip("pytest-benchmark not installed")


# 🧱🏗️🔚
