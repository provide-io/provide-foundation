"""File operation detectors.

This package provides specialized detectors for different file operation patterns:
- OperationDetector: Main orchestrator that coordinates all specialized detectors
- AtomicOperationDetector: Detects atomic saves and safe writes
- TempPatternDetector: Detects temporary file patterns (VSCode, Vim, etc.)
- BatchOperationDetector: Detects batch operations and rename sequences
- SimpleOperationDetector: Detects simple/direct file operations

The main OperationDetector orchestrates these specialized detectors to identify
the best match for a given set of file events.
"""

from __future__ import annotations

from provide.foundation.file.operations.detectors.atomic import AtomicOperationDetector
from provide.foundation.file.operations.detectors.batch import BatchOperationDetector
from provide.foundation.file.operations.detectors.orchestrator import OperationDetector
from provide.foundation.file.operations.detectors.simple import SimpleOperationDetector
from provide.foundation.file.operations.detectors.temp import TempPatternDetector

__all__ = [
    "AtomicOperationDetector",
    "BatchOperationDetector",
    "OperationDetector",
    "SimpleOperationDetector",
    "TempPatternDetector",
]
