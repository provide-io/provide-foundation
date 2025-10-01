"""File operation detector - Compatibility shim.

This module provides backward compatibility by re-exporting from the detectors package.
The actual implementation is in detectors/orchestrator.py.
"""

from __future__ import annotations

from provide.foundation.file.operations.detectors import OperationDetector

__all__ = ["OperationDetector"]
