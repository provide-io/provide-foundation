"""File operations testing utilities."""

from __future__ import annotations

try:
    from .operations_fixtures import (
        FileOperationSimulator,
        FileOperationValidator,
        file_operation_test,
        requires_file_operations,
    )

    __all__ = [
        "FileOperationSimulator",
        "FileOperationValidator",
        "file_operation_test",
        "requires_file_operations",
    ]
except ImportError:
    # Operations module not available
    __all__ = []