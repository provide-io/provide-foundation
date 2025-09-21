"""Test cases and utilities for file operation quality analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from provide.foundation.file.operations import FileEvent, FileEventMetadata

    HAS_OPERATIONS_MODULE = True
except ImportError:
    HAS_OPERATIONS_MODULE = False


@dataclass
class OperationTestCase:
    """Test case for operation detection validation."""

    name: str
    events: list[FileEvent]
    expected_operations: list[dict[str, Any]]  # Expected operation specs
    description: str = ""
    tags: list[str] = field(default_factory=list)


def create_test_cases_from_patterns() -> list[OperationTestCase]:
    """Create standard test cases for common operation patterns.

    Returns:
        List of test cases covering common patterns
    """
    if not HAS_OPERATIONS_MODULE:
        return []

    test_cases = []
    base_time = datetime.now()

    # VSCode atomic save test case
    vscode_events = [
        FileEvent(
            path=Path("test.txt.tmp.12345"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=1024),
        ),
        FileEvent(
            path=Path("test.txt.tmp.12345"),
            event_type="moved",
            metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=50), sequence_number=2),
            dest_path=Path("test.txt"),
        ),
    ]

    test_cases.append(
        OperationTestCase(
            name="vscode_atomic_save",
            events=vscode_events,
            expected_operations=[{"type": "atomic_save", "confidence_min": 0.9}],
            description="VSCode atomic save pattern",
            tags=["atomic", "editor", "vscode"],
        )
    )

    # Safe write test case
    safe_write_events = [
        FileEvent(
            path=Path("document.bak"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=1000),
        ),
        FileEvent(
            path=Path("document"),
            event_type="modified",
            metadata=FileEventMetadata(
                timestamp=base_time + timedelta(milliseconds=100),
                sequence_number=2,
                size_before=1000,
                size_after=1024,
            ),
        ),
    ]

    test_cases.append(
        OperationTestCase(
            name="safe_write_with_backup",
            events=safe_write_events,
            expected_operations=[{"type": "safe_write", "confidence_min": 0.8}],
            description="Safe write with backup creation",
            tags=["safe", "backup"],
        )
    )

    # Batch update test case
    batch_events = []
    for i in range(5):
        batch_events.append(
            FileEvent(
                path=Path(f"src/file{i}.py"),
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=i * 10),
                    sequence_number=i + 1,
                    size_before=500,
                    size_after=520,
                ),
            )
        )

    test_cases.append(
        OperationTestCase(
            name="batch_format_operation",
            events=batch_events,
            expected_operations=[{"type": "batch_update", "confidence_min": 0.7}],
            description="Batch formatting operation",
            tags=["batch", "formatting"],
        )
    )

    return test_cases
