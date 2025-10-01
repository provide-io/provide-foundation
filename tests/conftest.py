#
# tests/conftest.py
#
"""Pytest configuration and global fixtures for provide-foundation tests.

This file contains only the essential global fixtures and configuration
that must be at the root level for pytest.

All tests should inherit from FoundationTestCase which handles
Foundation reset automatically.
"""

from __future__ import annotations

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

from provide.testkit import set_log_stream_for_testing  # noqa: E402 # type: ignore

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
    import sys

    try:
        yield
    finally:
        # ALWAYS reset Foundation after each test, regardless of test type
        # This ensures clean state for the next test in the worker
        reset_foundation_setup_for_testing()

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
from provide.testkit import (  # noqa: E402
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
    # Time fixtures
    time_machine,
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
    "time_machine",
    "valid_cert_pem",
    "valid_key_pem",
]
