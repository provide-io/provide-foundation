#
# tests/conftest.py
#
"""
Pytest configuration and fixtures for provide-foundation tests.

This file defines shared fixtures used across multiple test modules,
primarily for managing the telemetry system's state during testing,
capturing log output, and providing diagnostic logging for the test setup itself.
"""

from collections.abc import Generator
import logging as stdlib_logging
import os
import sys

import pytest

from provide.foundation.core import (
    _set_log_stream_for_testing,
    reset_foundation_setup_for_testing,
)

# Import fixtures from modules for backward compatibility
from tests.fixtures.logger import (
    captured_stderr_for_foundation,
    setup_foundation_telemetry_for_test,
)

_conftest_diag_logger_name = "provide.foundation.conftest_diag"


def _get_conftest_diag_logger() -> stdlib_logging.Logger:
    """Initializes and returns a diagnostic logger for conftest operations."""
    logger = stdlib_logging.getLogger(_conftest_diag_logger_name)
    if not logger.handlers:
        handler = stdlib_logging.StreamHandler(
            sys.stderr
        )  # Actual stderr for diagnostics
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
if not os.getenv("PYTEST_WORKER_ID"):  # Avoid multiple messages with xdist
    conftest_diag_logger.debug("⚙️➡️🔍 Conftest loaded.")


@pytest.fixture(autouse=True)
def manage_telemetry_reset_for_each_test() -> Generator[None]:
    """
    Autouse fixture to reset Foundation Telemetry before and after each test.
    Ensures test isolation by calling `reset_foundation_setup_for_testing()`.
    """
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug(
            "🔄 (Pre-test) Calling reset_foundation_setup_for_testing()"
        )
    reset_foundation_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    yield
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug(
            "🔄 (Post-test) Calling reset_foundation_setup_for_testing()"
        )
    reset_foundation_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    _set_log_stream_for_testing(None)  # Ensure stream is reset to default stderr


# Fixtures are now imported from tests.fixtures.logger above
# for backward compatibility - tests can still use them from conftest


@pytest.fixture(scope="session")
def foundation_conftest_diagnostic_logger() -> stdlib_logging.Logger:
    """Session-scoped fixture providing the conftest diagnostic logger."""
    return _get_conftest_diag_logger()


# 🧪⚙️
