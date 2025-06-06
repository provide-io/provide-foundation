#
# tests/conftest.py
#
"""
Pytest configuration and fixtures for pyvider-telemetry tests.

This file defines shared fixtures used across multiple test modules,
primarily for managing the telemetry system's state during testing,
capturing log output, and providing diagnostic logging for the test setup itself.
"""
from collections.abc import Callable, Generator
import io  # For io.StringIO
import logging as stdlib_logging
import os
import sys
from typing import TextIO  # Corrected: TextIO from typing

import pytest

from pyvider.telemetry import TelemetryConfig, setup_telemetry

# ensure_config_warnings_logger_configured is removed from config.py, so remove import
# from pyvider.telemetry.config import ensure_config_warnings_logger_configured
from pyvider.telemetry.core import (
    _set_log_stream_for_testing,
    reset_pyvider_setup_for_testing,
)

_conftest_diag_logger_name = "pyvider.telemetry.conftest_diag"

def _get_conftest_diag_logger() -> stdlib_logging.Logger:
    """Initializes and returns a diagnostic logger for conftest operations."""
    logger = stdlib_logging.getLogger(_conftest_diag_logger_name)
    if not logger.handlers:
        handler = stdlib_logging.StreamHandler(sys.stderr) # Actual stderr for diagnostics
        formatter = stdlib_logging.Formatter(
            "[Conftest DIAG] %(levelname)s (%(name)s): %(message)s"
        )
        handler.setFormatter(formatter)
        level_str = os.getenv("PYTEST_CONTEST_DIAG_LOG_LEVEL", "DEBUG").upper()
        level = getattr(stdlib_logging, level_str, stdlib_logging.DEBUG)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

conftest_diag_logger = _get_conftest_diag_logger()
if not os.getenv("PYTEST_WORKER_ID"): # Avoid multiple messages with xdist
    conftest_diag_logger.debug("⚙️➡️🔍 Conftest loaded.")


@pytest.fixture(autouse=True)
def manage_telemetry_reset_for_each_test() -> Generator[None]:
    """
    Autouse fixture to reset Pyvider telemetry before and after each test.
    Ensures test isolation by calling `reset_pyvider_setup_for_testing()`.
    """
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug("🔄 (Pre-test) Calling reset_pyvider_setup_for_testing()")
    reset_pyvider_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    yield
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug("🔄 (Post-test) Calling reset_pyvider_setup_for_testing()")
    reset_pyvider_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    _set_log_stream_for_testing(None) # Ensure stream is reset to default stderr


@pytest.fixture
def captured_stderr_for_pyvider() -> Generator[TextIO]: # Corrected: TextIO, and it's io.StringIO which is a TextIO
    """
    Fixture to capture stderr output from Pyvider's logging system.

    It redirects Pyvider's log stream to an `io.StringIO` buffer, yields the buffer
    to the test, and then restores the original stream.
    """
    current_test_stream = io.StringIO()
    _set_log_stream_for_testing(current_test_stream)
    yield current_test_stream
    _set_log_stream_for_testing(None)
    current_test_stream.close()


@pytest.fixture
def setup_pyvider_telemetry_for_test(
    captured_stderr_for_pyvider: TextIO # Corrected: TextIO
) -> Callable[[TelemetryConfig | None], None]:
    """
    Fixture providing a function to set up Pyvider telemetry for a test.

    The setup function uses the `captured_stderr_for_pyvider` fixture to ensure
    log output during setup (and subsequent logging) is captured.

    Args:
        captured_stderr_for_pyvider: Fixture to capture stderr.

    Returns:
        A callable that takes an optional `TelemetryConfig` and calls `setup_telemetry`.
    """
    def _setup_func(config: TelemetryConfig | None = None) -> None:
        # The `config` parameter is correctly defined to accept TelemetryConfig or None.
        # Calls like _setup_func(config=cfg_instance) or _setup_func(cfg_instance) are valid.
        setup_telemetry(config)
    return _setup_func

@pytest.fixture(scope="session")
def pyvider_conftest_diagnostic_logger() -> stdlib_logging.Logger:
    """Session-scoped fixture providing the conftest diagnostic logger."""
    return _get_conftest_diag_logger()

# 🧪⚙️
