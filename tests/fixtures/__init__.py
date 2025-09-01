"""Shared pytest fixtures for testing."""

from tests.fixtures.logger import (
    captured_stderr_for_foundation,
    setup_foundation_telemetry_for_test,
)

__all__ = [
    "captured_stderr_for_foundation",
    "setup_foundation_telemetry_for_test",
]