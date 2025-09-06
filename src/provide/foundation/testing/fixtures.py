"""
Common Test Fixtures for Foundation.

Provides pytest fixtures for capturing output, setting up telemetry,
and other common testing scenarios across the Foundation test suite.
"""

from collections.abc import Callable, Generator
import io
from typing import TextIO

import pytest

from provide.foundation import TelemetryConfig, setup_telemetry
from provide.foundation.testing.streams import set_log_stream_for_testing


@pytest.fixture
def captured_stderr_for_foundation() -> Generator[TextIO]:
    """
    Fixture to capture stderr output from Foundation's logging system.

    It redirects Foundation's log stream to an `io.StringIO` buffer, yields the buffer
    to the test, and then restores the original stream.
    """
    current_test_stream = io.StringIO()
    set_log_stream_for_testing(current_test_stream)
    yield current_test_stream
    set_log_stream_for_testing(None)
    current_test_stream.close()


@pytest.fixture
def setup_foundation_telemetry_for_test(
    captured_stderr_for_foundation: TextIO,
) -> Callable[[TelemetryConfig | None], None]:
    """
    Fixture providing a function to set up Foundation Telemetry for tests.

    This fixture captures stderr via `captured_stderr_for_foundation`
    and provides a callable to configure telemetry with custom settings.
    """

    def _setup(config: TelemetryConfig | None = None) -> None:
        if config is None:
            config = TelemetryConfig()
        setup_telemetry(config)

    return _setup
