#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for testkit file operations fixtures."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase

from tests.file.file_operations_fixtures import (
    FileOperationSimulator,
    FileOperationValidator,
    file_operation_pattern,
    requires_file_operations,  # Import the fixture
)


@requires_file_operations
class TestFileOperationSimulator(FoundationTestCase):
    """Test the file operation simulator."""

    def test_simulator_initialization(self, temp_workspace: Path) -> None:
        """Test simulator initialization."""
        simulator = FileOperationSimulator(temp_workspace)
        assert simulator.base_path == temp_workspace
        assert simulator.sequence_counter == 0
        assert len(simulator.operations_detected) == 0

    def test_vscode_save_simulation(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test VSCode atomic save simulation."""
        events = file_operation_simulator.simulate_vscode_save("test.txt", 1024)

        assert len(events) == 2

        # First event: temp file creation
        assert events[0].event_type == "created"
        assert "tmp.vscode" in str(events[0].path)
        assert events[0].metadata.size_after == 1024
        assert events[0].metadata.process_name == "Code"

        # Second event: rename to final
        assert events[1].event_type == "moved"
        assert events[1].dest_path is not None
        assert events[1].dest_path.name == "test.txt"

    def test_vim_save_simulation(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test Vim atomic save simulation."""
        events = file_operation_simulator.simulate_vim_save("test.txt", 1024)

        assert len(events) == 3

        # First event: delete original
        assert events[0].event_type == "deleted"
        assert events[0].path.name == "test.txt"
        assert events[0].metadata.size_before == 1024
        assert events[0].metadata.process_name == "vim"

        # Second event: create backup
        assert events[1].event_type == "created"
        assert events[1].path.name == "test.txt~"
        assert events[1].metadata.size_after == 1024

        # Third event: create new version
        assert events[2].event_type == "created"
        assert events[2].path.name == "test.txt"
        assert events[2].metadata.size_after == 1074  # Slightly larger

    def test_safe_write_simulation(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test safe write simulation."""
        events = file_operation_simulator.simulate_safe_write("test.txt", 1024)

        assert len(events) == 2

        # First event: create backup
        assert events[0].event_type == "created"
        assert events[0].path.name == "test.txt.bak"
        assert events[0].metadata.size_after == 1024

        # Second event: modify original
        assert events[1].event_type == "modified"
        assert events[1].path.name == "test.txt"
        assert events[1].metadata.size_before == 1024
        assert events[1].metadata.size_after == 1124

    def test_batch_operation_simulation(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test batch operation simulation."""
        events = file_operation_simulator.simulate_batch_operation(3, "module", ".py", 500)

        assert len(events) == 3

        for i, event in enumerate(events):
            assert event.event_type == "modified"
            assert event.path.name == f"module_{i}.py"
            assert event.metadata.size_before == 500
            assert event.metadata.size_after == 520
            assert event.metadata.process_name == "black"

    def test_all_patterns_simulation(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test simulation of all patterns."""
        all_patterns = file_operation_simulator.simulate_all_patterns()

        assert "vscode_save" in all_patterns
        assert "vim_save" in all_patterns
        assert "safe_write" in all_patterns
        assert "batch_operation" in all_patterns

        # Verify each pattern has events
        for pattern_name, events in all_patterns.items():
            assert len(events) > 0, f"Pattern {pattern_name} has no events"

    def test_operation_detection(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test operation detection from events."""
        # Generate VSCode save events
        events = file_operation_simulator.simulate_vscode_save("test.txt")

        # Detect operations
        operations = file_operation_simulator.detect_operations(events)

        assert len(operations) >= 1
        # Should detect atomic save
        atomic_saves = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_saves) >= 1


@requires_file_operations
class TestFileOperationValidator(FoundationTestCase):
    """Test the file operation validator."""

    def test_validator_initialization(self, file_operation_validator: FileOperationValidator) -> None:
        """Test validator initialization."""
        assert len(file_operation_validator.validation_results) == 0

    def test_operation_validation_success(
        self,
        file_operation_simulator: FileOperationSimulator,
        file_operation_validator: FileOperationValidator,
    ) -> None:
        """Test successful operation validation."""
        # Generate and detect VSCode save
        events = file_operation_simulator.simulate_vscode_save("test.txt")
        operations = file_operation_simulator.detect_operations(events)

        assert len(operations) >= 1
        operation = operations[0]

        # Validate the operation
        result = file_operation_validator.validate_operation(
            operation,
            expected_type="atomic_save",
            expected_confidence_min=0.8,
            expected_atomic=True,
            expected_safe=True,
        )

        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert result["operation_type"] == "atomic_save"
        assert result["confidence"] >= 0.8

    def test_operation_validation_failure(
        self,
        file_operation_simulator: FileOperationSimulator,
        file_operation_validator: FileOperationValidator,
    ) -> None:
        """Test operation validation failure."""
        # Generate and detect VSCode save
        events = file_operation_simulator.simulate_vscode_save("test.txt")
        operations = file_operation_simulator.detect_operations(events)

        assert len(operations) >= 1
        operation = operations[0]

        # Validate with wrong expectations
        result = file_operation_validator.validate_operation(
            operation,
            expected_type="batch_update",  # Wrong type
            expected_confidence_min=0.99,  # Too high confidence
            expected_atomic=False,  # Wrong atomic flag
        )

        assert result["valid"] is False
        assert len(result["errors"]) >= 2  # Type and confidence errors

    def test_validation_summary(self, file_operation_validator: FileOperationValidator) -> None:
        """Test validation summary generation."""
        # Initially empty
        summary = file_operation_validator.get_summary()
        assert summary["total"] == 0
        assert summary["success_rate"] == 0.0

        # Add some mock validation results
        file_operation_validator.validation_results = [
            {"valid": True, "confidence": 0.95},
            {"valid": False, "confidence": 0.60},
            {"valid": True, "confidence": 0.85},
        ]

        summary = file_operation_validator.get_summary()
        assert summary["total"] == 3
        assert summary["valid"] == 2
        assert summary["invalid"] == 1
        assert summary["success_rate"] == 2 / 3
        assert summary["average_confidence"] == (0.95 + 0.60 + 0.85) / 3


@file_operation_pattern("vscode", "vim")
def test_file_operation_decorator(file_operation_simulator: FileOperationSimulator) -> None:
    """Test the file operation pattern decorator."""
    # Test that the decorator is applied
    assert hasattr(test_file_operation_decorator, "_file_operation_patterns")
    assert test_file_operation_decorator._file_operation_patterns == ("vscode", "vim")

    # Test functionality
    vscode_events = file_operation_simulator.simulate_vscode_save()
    vim_events = file_operation_simulator.simulate_vim_save()

    assert len(vscode_events) > 0
    assert len(vim_events) > 0


@requires_file_operations
class TestIntegrationScenarios(FoundationTestCase):
    """Integration tests for complex file operation scenarios."""

    def test_editor_workflow_simulation(
        self,
        file_operation_simulator: FileOperationSimulator,
        file_operation_validator: FileOperationValidator,
    ) -> None:
        """Test simulation of complete editor workflow."""
        # Simulate a complex workflow
        all_events = []

        # Developer saves file in VSCode
        all_events.extend(file_operation_simulator.simulate_vscode_save("main.py"))

        # Developer creates backup before risky changes
        all_events.extend(file_operation_simulator.simulate_safe_write("main.py"))

        # Code formatter runs on multiple files
        all_events.extend(file_operation_simulator.simulate_batch_operation(5))

        # Detect all operations
        operations = file_operation_simulator.detect_operations(all_events)

        # Should detect multiple operation types
        operation_types = {op.operation_type.value for op in operations}
        assert len(operation_types) >= 2  # At least atomic_save and safe_write or batch_update

        # Validate each operation
        for operation in operations:
            if operation.operation_type.value == "atomic_save":
                result = file_operation_validator.validate_operation(
                    operation,
                    expected_type="atomic_save",
                    expected_confidence_min=0.85,
                    expected_atomic=True,
                )
                assert result["valid"]

            elif operation.operation_type.value == "safe_write":
                result = file_operation_validator.validate_operation(
                    operation,
                    expected_type="safe_write",
                    expected_confidence_min=0.80,
                    expected_safe=True,
                    expected_backup=True,
                )
                assert result["valid"]

    def test_performance_scenario(self, file_operation_simulator: FileOperationSimulator) -> None:
        """Test performance with large number of operations."""
        # Generate many batch operations
        all_events = []
        for i in range(10):  # 10 batches of 5 files each
            batch_events = file_operation_simulator.simulate_batch_operation(5, f"batch_{i}_file", ".py")
            all_events.extend(batch_events)

        # Should handle 50 events efficiently
        operations = file_operation_simulator.detect_operations(all_events)

        # Should detect batch operations
        batch_ops = [op for op in operations if op.operation_type.value == "batch_update"]
        assert len(batch_ops) >= 1

    def test_confidence_validation(
        self,
        file_operation_simulator: FileOperationSimulator,
        file_operation_validator: FileOperationValidator,
    ) -> None:
        """Test confidence scoring validation across patterns."""
        patterns = file_operation_simulator.simulate_all_patterns()

        for pattern_name, events in patterns.items():
            operations = file_operation_simulator.detect_operations(events)

            # Each pattern should produce at least one operation
            assert len(operations) >= 1, f"Pattern {pattern_name} produced no operations"

            # Each operation should have reasonable confidence
            for operation in operations:
                assert operation.confidence >= 0.5, f"Low confidence in {pattern_name}: {operation.confidence}"
                assert operation.confidence <= 1.0, (
                    f"Invalid confidence in {pattern_name}: {operation.confidence}"
                )


# 🧱🏗️🔚
