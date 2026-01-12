#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test file operation detector registry extensibility.

Verifies that custom detectors can be registered and used alongside built-in detectors."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations.detectors import (
    clear_detector_registry,
    get_all_detectors,
    register_detector,
)
from provide.foundation.file.operations.detectors.orchestrator import (
    OperationDetector,
)
from provide.foundation.file.operations.types import (
    FileEvent,
    FileEventMetadata,
    FileOperation,
    OperationType,
)


class TestDetectorRegistryExtensibility(FoundationTestCase):
    """Test custom detector registration and priority ordering."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Clear registry before each test
        clear_detector_registry()

    def teardown_method(self) -> None:
        """Clean up after test."""
        # Clear registry after each test
        clear_detector_registry()
        super().teardown_method()

    def test_custom_detector_registration(self) -> None:
        """Test that custom detectors can be registered."""

        def detect_custom_pattern(events: list[FileEvent]) -> FileOperation | None:
            """Custom detector for testing."""
            if len(events) == 1 and events[0].path.suffix == ".custom":
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=events[0].path,
                    events=events,
                    confidence=0.99,
                    description="Custom file operation",
                    start_time=events[0].timestamp,
                    end_time=events[0].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[events[0].path],
                    metadata={"pattern": "custom"},
                )
            return None

        # Register custom detector
        register_detector(
            name="detect_custom",
            func=detect_custom_pattern,
            priority=80,
            description="Detects custom file pattern",
        )

        # Verify registration
        detectors = get_all_detectors()
        detector_names = [name for name, _, _ in detectors]
        assert "detect_custom" in detector_names

    def test_custom_detector_priority_ordering(self) -> None:
        """Test that detectors are ordered by priority."""

        def high_priority_detector(events: list[FileEvent]) -> FileOperation | None:
            return None

        def medium_priority_detector(events: list[FileEvent]) -> FileOperation | None:
            return None

        def low_priority_detector(events: list[FileEvent]) -> FileOperation | None:
            return None

        # Register in non-priority order
        register_detector(name="medium_priority", func=medium_priority_detector, priority=50)
        register_detector(name="high_priority", func=high_priority_detector, priority=90)
        register_detector("low_priority", func=low_priority_detector, priority=20)

        # Get all detectors and verify they're sorted by priority
        detectors = get_all_detectors()
        priorities = [priority for _, _, priority in detectors]

        # Should be sorted highest to lowest
        assert priorities == sorted(priorities, reverse=True)

        # Verify our custom detectors are in the right order
        detector_list = [(name, priority) for name, _, priority in detectors]
        high_idx = next(i for i, (n, _) in enumerate(detector_list) if n == "high_priority")
        medium_idx = next(i for i, (n, _) in enumerate(detector_list) if n == "medium_priority")
        low_idx = next(i for i, (n, _) in enumerate(detector_list) if n == "low_priority")

        assert high_idx < medium_idx < low_idx

    def test_custom_detector_execution(self) -> None:
        """Test that custom detectors are executed by OperationDetector."""

        def detect_json_operations(events: list[FileEvent]) -> FileOperation | None:
            """Detector specifically for JSON files."""
            json_events = [e for e in events if e.path.suffix == ".json"]
            if json_events:
                return FileOperation(
                    operation_type=OperationType.ATOMIC_SAVE,
                    primary_path=json_events[0].path,
                    events=json_events,
                    confidence=0.98,
                    description="JSON file operation",
                    start_time=json_events[0].timestamp,
                    end_time=json_events[-1].timestamp,
                    is_atomic=True,
                    is_safe=True,
                    files_affected=[e.path for e in json_events],
                    metadata={"file_type": "json"},
                )
            return None

        # Register custom JSON detector with high priority
        register_detector(
            name="detect_json",
            func=detect_json_operations,
            priority=88,
            description="Detects JSON file operations",
        )

        # Create test events
        now = datetime.now()
        events = [
            FileEvent(
                path=Path("/tmp/config.json"),
                event_type="modified",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
        ]

        # Use OperationDetector to detect operation
        detector = OperationDetector()
        operations = detector.detect(events)

        # Should detect our custom JSON operation
        assert len(operations) == 1
        assert operations[0].description == "JSON file operation"
        assert operations[0].metadata.get("file_type") == "json"

    def test_custom_detector_override_builtin(self) -> None:
        """Test that higher priority custom detector overrides built-in detector."""

        def detect_temp_override(events: list[FileEvent]) -> FileOperation | None:
            """Higher priority detector that overrides built-in temp detection."""
            for event in events:
                if ".tmp" in event.path.name:
                    return FileOperation(
                        operation_type=OperationType.ATOMIC_SAVE,
                        primary_path=event.path,
                        events=events,
                        confidence=0.99,  # Very high confidence
                        description="Custom temp file handling",
                        start_time=events[0].timestamp,
                        end_time=events[-1].timestamp,
                        is_atomic=True,
                        is_safe=True,
                        files_affected=[event.path],
                        metadata={"custom": True, "pattern": "temp_override"},
                    )
            return None

        # Register custom detector with higher priority than built-in temp detectors (95-92)
        register_detector(
            name="detect_temp_override",
            func=detect_temp_override,
            priority=96,
            description="Override built-in temp detection",
        )

        # Create temp file event
        now = datetime.now()
        events = [
            FileEvent(
                path=Path("/tmp/file.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
        ]

        # Use OperationDetector
        detector = OperationDetector()
        operations = detector.detect(events)

        # Should use our custom detector due to higher priority
        assert len(operations) == 1
        assert operations[0].description == "Custom temp file handling"
        assert operations[0].metadata.get("custom") is True

    def test_registry_clear_removes_detectors(self) -> None:
        """Test that clearing registry removes all detectors."""

        def custom_detector(events: list[FileEvent]) -> FileOperation | None:
            return None

        # Register detector
        register_detector(name="test_detector", func=custom_detector, priority=50)

        # Verify it exists
        detectors_before = get_all_detectors()
        assert any(name == "test_detector" for name, _, _ in detectors_before)

        # Clear registry
        clear_detector_registry()

        # Verify it's gone
        detectors_after = get_all_detectors()
        assert not any(name == "test_detector" for name, _, _ in detectors_after)

    def test_detector_with_metadata(self) -> None:
        """Test that detector metadata is preserved."""

        def custom_detector(events: list[FileEvent]) -> FileOperation | None:
            return None

        # Register with description
        register_detector(
            name="documented_detector",
            func=custom_detector,
            priority=75,
            description="This is a well-documented detector",
        )

        # Get registry entry
        from provide.foundation.file.operations.detectors.registry import (
            get_detector_registry,
        )

        registry = get_detector_registry()
        entry = registry.get_entry("documented_detector", "file_operation_detector")

        assert entry is not None
        assert entry.metadata.get("priority") == 75
        assert entry.metadata.get("description") == "This is a well-documented detector"

    def test_multiple_custom_detectors_execution_order(self) -> None:
        """Test that multiple custom detectors execute in priority order."""
        execution_order = []

        def detector_a(events: list[FileEvent]) -> FileOperation | None:
            execution_order.append("A")
            return None

        def detector_b(events: list[FileEvent]) -> FileOperation | None:
            execution_order.append("B")
            return None

        def detector_c(events: list[FileEvent]) -> FileOperation | None:
            execution_order.append("C")
            return None

        # Register in reverse priority order
        register_detector(name="detector_c", func=detector_c, priority=30)
        register_detector(name="detector_a", func=detector_a, priority=90)
        register_detector(name="detector_b", func=detector_b, priority=60)

        # Create test event
        now = datetime.now()
        events = [
            FileEvent(
                path=Path("/tmp/test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
        ]

        # Execute detection
        detector = OperationDetector()
        detector.detect(events)

        # Verify execution order matches priority (A=90, B=60, C=30)
        # Note: execution_order will contain A, B, C based on priority, not registration order
        assert "A" in execution_order
        assert "B" in execution_order
        assert "C" in execution_order
        # A should execute before B and C
        assert execution_order.index("A") < execution_order.index("B")
        assert execution_order.index("B") < execution_order.index("C")

    def test_custom_detector_early_termination(self) -> None:
        """Test that high confidence custom detector triggers early termination."""
        execution_count = []

        def high_confidence_detector(
            events: list[FileEvent],
        ) -> FileOperation | None:
            execution_count.append("high")
            return FileOperation(
                operation_type=OperationType.ATOMIC_SAVE,
                primary_path=events[0].path,
                events=events,
                confidence=0.96,  # Above early termination threshold (0.95)
                description="High confidence match",
                start_time=events[0].timestamp,
                end_time=events[0].timestamp,
                is_atomic=True,
                is_safe=True,
                files_affected=[events[0].path],
            )

        def lower_priority_detector(events: list[FileEvent]) -> FileOperation | None:
            execution_count.append("low")
            return None

        # Register detectors
        register_detector(name="high_confidence", func=high_confidence_detector, priority=95)
        register_detector(name="lower_priority", func=lower_priority_detector, priority=80)

        # Create test event
        now = datetime.now()
        events = [
            FileEvent(
                path=Path("/tmp/test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=now, sequence_number=1),
            ),
        ]

        # Execute detection
        detector = OperationDetector()
        operations = detector.detect(events)

        # High confidence detector should match
        assert len(operations) == 1
        assert operations[0].confidence == 0.96

        # Lower priority detector should NOT execute due to early termination
        assert "high" in execution_count
        assert "low" not in execution_count


class TestDetectorRegistryBuiltins(FoundationTestCase):
    """Test that built-in detectors are auto-registered."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        # Re-register built-in detectors if they were cleared
        from provide.foundation.file.operations.detectors import (
            _auto_register_builtin_detectors,
        )

        _auto_register_builtin_detectors()

    def test_builtin_detectors_auto_registered(self) -> None:
        """Test that built-in detectors are automatically registered on import."""
        # Import the module (auto-registration happens)
        from provide.foundation.file.operations.detectors import get_all_detectors

        detectors = get_all_detectors()
        detector_names = [name for name, _, _ in detectors]

        # Verify all expected built-in detectors are present
        expected_detectors = [
            "detect_temp_rename_pattern",
            "detect_delete_temp_pattern",
            "detect_temp_modify_pattern",
            "detect_temp_create_delete_pattern",
            "detect_atomic_save",
            "detect_safe_write",
            "detect_rename_sequence",
            "detect_backup_create",
            "detect_batch_update",
            "detect_same_file_delete_create_pattern",
            "detect_direct_modification",
            "detect_simple_operation",
        ]

        for expected in expected_detectors:
            assert expected in detector_names, f"Expected detector {expected} not found"

    def test_builtin_detector_priorities(self) -> None:
        """Test that built-in detectors have correct priority ordering."""
        from provide.foundation.file.operations.detectors import get_all_detectors

        detectors = get_all_detectors()
        detector_map = {name: priority for name, _, priority in detectors}

        # Temp patterns should have highest priority (90-100)
        assert detector_map["detect_temp_rename_pattern"] == 95
        assert detector_map["detect_delete_temp_pattern"] == 94
        assert detector_map["detect_temp_modify_pattern"] == 93
        assert detector_map["detect_temp_create_delete_pattern"] == 92

        # Atomic save patterns (80-89)
        assert detector_map["detect_atomic_save"] == 85
        assert detector_map["detect_safe_write"] == 84

        # Batch and sequence patterns (70-79)
        assert detector_map["detect_rename_sequence"] == 75
        assert detector_map["detect_backup_create"] == 74
        assert detector_map["detect_batch_update"] == 73

        # Simple patterns (60-69)
        assert detector_map["detect_same_file_delete_create_pattern"] == 65
        assert detector_map["detect_direct_modification"] == 64

        # Fallback (0-9)
        assert detector_map["detect_simple_operation"] == 10


# 🧱🏗️🔚
