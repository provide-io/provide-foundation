#
# __init__.py
#
"""
Foundation Testing Module.

Unified testing utilities for Foundation with automatic context detection and warnings.
This module consolidates all testing helpers in one place with clear warnings when active.
"""

import os
import sys
from typing import Any
import warnings


# Context detection functions
def _is_testing_context() -> bool:
    """Detect if we're running in a testing context."""
    return (
        "pytest" in sys.modules
        or os.getenv("PYTEST_CURRENT_TEST") is not None
        or "unittest" in sys.modules
        or os.getenv("TESTING") == "true"
        or any(arg.endswith(("pytest", "py.test")) for arg in sys.argv)
    )


def _warn_testing_active() -> None:
    """Issue warning that testing helpers are active."""
    if not os.getenv("FOUNDATION_SUPPRESS_TESTING_WARNINGS"):
        warnings.warn(
            "🚨 Foundation testing helpers are active - production behavior may differ",
            UserWarning,
            stacklevel=3,
        )


def _should_warn() -> bool:
    """Check if we should issue testing warnings."""
    # Don't warn if explicitly suppressed
    if os.getenv("FOUNDATION_SUPPRESS_TESTING_WARNINGS"):
        return False

    # Don't warn if we're not in a testing context
    if not _is_testing_context():
        return False

    # Don't warn if already warned (module-level state)
    return not getattr(_should_warn, "_warned", False)


# Issue warning on import if in testing context
if _should_warn():
    _warn_testing_active()
    _should_warn._warned = True


# Lazy imports to avoid importing testing utilities in production
def __getattr__(name: str) -> Any:
    """Lazy import testing utilities only when accessed."""

    # CLI testing utilities
    if name in [
        "MockContext",
        "isolated_cli_runner",
        "temp_config_file",
        "create_test_cli",
        "mock_logger",
        "CliTestCase",
    ]:
        import provide.foundation.testing.cli as cli_module

        return getattr(cli_module, name)

    # Logger testing utilities
    elif name in ["reset_foundation_setup_for_testing", "reset_foundation_state"]:
        import provide.foundation.testing.logger as logger_module

        return getattr(logger_module, name)

    # Stream testing utilities
    elif name in ["set_log_stream_for_testing"]:
        import provide.foundation.testing.streams as streams_module

        return getattr(streams_module, name)

    # Fixture utilities
    elif name in [
        "captured_stderr_for_foundation",
        "setup_foundation_telemetry_for_test",
    ]:
        import provide.foundation.testing.fixtures as fixtures_module

        return getattr(fixtures_module, name)

    # Crypto fixtures (many fixtures)
    elif name in [
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
    ]:
        import provide.foundation.testing.crypto as crypto_module

        return getattr(crypto_module, name)

    # Hub fixtures
    elif name in ["default_container_directory"]:
        import provide.foundation.testing.hub as hub_module

        return getattr(hub_module, name)

    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Public API - these will be available for import but loaded lazily
__all__ = [
    # Context detection
    "_is_testing_context",
    # CLI testing
    "MockContext",
    "isolated_cli_runner",
    "temp_config_file",
    "create_test_cli",
    "mock_logger",
    "CliTestCase",
    # Logger testing
    "reset_foundation_setup_for_testing",
    "reset_foundation_state",
    # Stream testing
    "set_log_stream_for_testing",
    # Common fixtures
    "captured_stderr_for_foundation",
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
    # Hub fixtures
    "default_container_directory",
]
