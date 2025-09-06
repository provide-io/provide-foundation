#
# tests/conftest.py
#
"""
Pytest configuration and global fixtures for provide-foundation tests.

This file contains only the essential global fixtures and configuration
that must be at the root level for pytest.
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


# Import and re-export fixtures so they're available to all tests
from tests.fixtures.hub import default_container_directory
from tests.fixtures.logger import (
    captured_stderr_for_foundation,
    setup_foundation_telemetry_for_test,
)
from tests.fixtures.crypto import (
    client_cert,
    server_cert,
    ca_cert,
    valid_cert_pem,
    valid_key_pem,
    invalid_cert_pem,
    invalid_key_pem,
    malformed_cert_pem,
    empty_cert,
    temporary_cert_file,
    temporary_key_file,
    cert_with_windows_line_endings,
    cert_with_utf8_bom,
    cert_with_extra_whitespace,
    external_ca_pem,
)

# Re-export for pytest discovery
__all__ = [
    "captured_stderr_for_foundation",
    "default_container_directory", 
    "setup_foundation_telemetry_for_test",
    # Crypto fixtures
    "client_cert",
    "server_cert",
    "ca_cert", 
    "valid_cert_pem",
    "valid_key_pem",
    "invalid_cert_pem",
    "invalid_key_pem",
    "malformed_cert_pem",
    "empty_cert",
    "temporary_cert_file", 
    "temporary_key_file",
    "cert_with_windows_line_endings",
    "cert_with_utf8_bom",
    "cert_with_extra_whitespace",
    "external_ca_pem",
]
