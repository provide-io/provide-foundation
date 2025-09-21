"""Simple tests for file operations fixtures."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from tests.file_operations_fixtures import (
    FileOperationSimulator,
    FileOperationValidator,
    requires_file_operations,
)


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def simulator(temp_workspace):
    """Create a file operation simulator."""
    return FileOperationSimulator(temp_workspace)


@pytest.fixture
def validator():
    """Create a file operation validator."""
    return FileOperationValidator()


@requires_file_operations
class TestFileOperationFixtures:
    """Test the file operation fixtures work correctly."""

    def test_simulator_basic_functionality(self, simulator):
        """Test basic simulator functionality."""
        assert simulator.base_path.exists()
        assert simulator.sequence_counter == 0

    def test_vscode_save_simulation(self, simulator):
        """Test VSCode save simulation."""
        events = simulator.simulate_vscode_save("test.txt", 1024)
        assert len(events) == 2
        assert events[0].event_type == "created"
        assert "tmp.vscode" in str(events[0].path)
        assert events[1].event_type == "moved"
        assert events[1].dest_path.name == "test.txt"

    def test_operation_detection(self, simulator):
        """Test operation detection works."""
        events = simulator.simulate_vscode_save("test.txt")
        operations = simulator.detect_operations(events)
        assert len(operations) >= 1

        # Should detect atomic save
        atomic_saves = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_saves) >= 1

    def test_validation_works(self, simulator, validator):
        """Test validation functionality."""
        events = simulator.simulate_vscode_save("test.txt")
        operations = simulator.detect_operations(events)
        assert len(operations) >= 1

        operation = operations[0]
        result = validator.validate_operation(
            operation,
            expected_type="atomic_save",
            expected_confidence_min=0.8,
            expected_atomic=True,
        )

        assert result["valid"] is True
        assert result["operation_type"] == "atomic_save"
        assert result["confidence"] >= 0.8

    def test_validation_summary(self, validator):
        """Test validation summary functionality."""
        # Initially empty
        summary = validator.get_summary()
        assert summary["total"] == 0
        assert summary["success_rate"] == 0.0

        # Add mock results
        validator.validation_results = [
            {"valid": True, "confidence": 0.95},
            {"valid": False, "confidence": 0.60},
        ]

        summary = validator.get_summary()
        assert summary["total"] == 2
        assert summary["valid"] == 1
        assert summary["success_rate"] == 0.5