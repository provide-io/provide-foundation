"""Shared pytest fixtures for testing."""

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

__all__ = [
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
]
