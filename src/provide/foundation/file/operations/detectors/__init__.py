"""File operation detectors.

This package provides specialized detectors for different file operation patterns:
- AtomicOperationDetector: Detects atomic saves and safe writes
- TempPatternDetector: Detects temporary file patterns (VSCode, Vim, etc.)
- BatchOperationDetector: Detects batch operations and rename sequences
- SimpleOperationDetector: Detects simple/direct file operations

The main OperationDetector orchestrates these specialized detectors to identify
the best match for a given set of file events.
"""

from __future__ import annotations

from .atomic import AtomicOperationDetector
from .batch import BatchOperationDetector
from .simple import SimpleOperationDetector
from .temp import TempPatternDetector

__all__ = [
    "AtomicOperationDetector",
    "BatchOperationDetector",
    "SimpleOperationDetector",
    "TempPatternDetector",
]
