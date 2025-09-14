#
# tests/conftest.py
#
"""Pytest configuration and global fixtures for provide-foundation tests.

This file contains only the essential global fixtures and configuration
that must be at the root level for pytest.
"""

from collections.abc import Generator
import logging as stdlib_logging
import os
import sys

import pytest

# Set DEBUG log level for all tests
os.environ.setdefault("PROVIDE_LOG_LEVEL", "DEBUG")

# Temporarily suppress testing warnings only for the import
with_suppression = os.environ.get("FOUNDATION_SUPPRESS_TESTING_WARNINGS")
os.environ["FOUNDATION_SUPPRESS_TESTING_WARNINGS"] = "true"

from provide.testkit import (
    reset_foundation_setup_for_testing,
    set_log_stream_for_testing,
)

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
    conftest_diag_logger.debug("⚙️➡️🔍 Conftest loaded.")


@pytest.fixture(autouse=True)
def manage_telemetry_reset_for_each_test() -> Generator[None]:
    """Autouse fixture to reset Foundation Telemetry before and after each test.
    Ensures test isolation by calling `reset_foundation_setup_for_testing()`.
    """
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug(
            "🔄 (Pre-test) Calling reset_foundation_setup_for_testing()",
        )
    reset_foundation_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    yield
    if not os.getenv("PYTEST_WORKER_ID") or os.getenv("PYTEST_WORKER_ID") == "gw0":
        conftest_diag_logger.debug(
            "🔄 (Post-test) Calling reset_foundation_setup_for_testing()",
        )
    reset_foundation_setup_for_testing()
    # ensure_config_warnings_logger_configured call removed
    set_log_stream_for_testing(None)  # Ensure stream is reset to default stderr


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
    "malformed_cert_pem",
    "mock_async_process",
    "mock_cache",
    # New mock fixtures
    "mock_http_config",
    # Logger exports
    "mock_logger",
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
    "valid_cert_pem",
    "valid_key_pem",
]
