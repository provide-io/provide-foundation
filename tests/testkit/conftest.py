"""Conftest for testkit tests."""

from __future__ import annotations

# Import fixtures from file_operations_fixtures
from tests.file.file_operations_fixtures import (
    file_operation_simulator,
    file_operation_validator,
    operation_detector,
    temp_workspace,
)

# Load testkit Hub fixtures plugin
pytest_plugins = ["provide.testkit.hub.fixtures"]

# Make fixtures available to tests in this directory
__all__ = [
    "file_operation_simulator",
    "file_operation_validator",
    "operation_detector",
    "temp_workspace",
]
