"""Pattern-specific tests using testkit file operations fixtures."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from tests.file_operations_fixtures import (
    FileOperationSimulator,
    FileOperationValidator,
    file_operation_pattern,
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
class TestEditorSpecificPatterns:
    """Test editor-specific file operation patterns."""

    @file_operation_pattern("vscode")
    def test_vscode_atomic_save_pattern(self, simulator, validator):
        """Test VSCode atomic save pattern detection."""
        events = simulator.simulate_vscode_save("document.txt", 2048)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1

        # Validate the detected atomic save
        atomic_operations = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_operations) >= 1

        operation = atomic_operations[0]
        result = validator.validate_operation(
            operation,
            expected_type="atomic_save",
            expected_confidence_min=0.9,
            expected_atomic=True,
            expected_safe=True,
        )

        assert result["valid"] is True
        assert result["confidence"] >= 0.9
        assert result["is_atomic"] is True

    @file_operation_pattern("vim")
    def test_vim_atomic_save_pattern(self, simulator, validator):
        """Test Vim atomic save pattern with backup."""
        events = simulator.simulate_vim_save("config.py", 1536)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1

        # Should detect atomic save
        atomic_operations = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_operations) >= 1

        operation = atomic_operations[0]
        result = validator.validate_operation(
            operation,
            expected_type="atomic_save",
            expected_confidence_min=0.8,
            expected_atomic=True,
        )

        assert result["valid"] is True

    @file_operation_pattern("safe_write")
    def test_safe_write_with_backup_pattern(self, simulator, validator):
        """Test safe write pattern with backup creation."""
        events = simulator.simulate_safe_write("important.data", 4096)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1

        # Should detect safe write
        safe_operations = [op for op in operations if op.operation_type.value == "safe_write"]
        assert len(safe_operations) >= 1

        operation = safe_operations[0]
        result = validator.validate_operation(
            operation,
            expected_type="safe_write",
            expected_confidence_min=0.8,
            expected_safe=True,
            expected_backup=True,
        )

        assert result["valid"] is True
        assert result["has_backup"] is True

    @file_operation_pattern("batch")
    def test_batch_formatting_pattern(self, simulator, validator):
        """Test batch file formatting operation."""
        events = simulator.simulate_batch_operation(10, "module", ".py", 800)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1

        # Should detect batch update
        batch_operations = [op for op in operations if op.operation_type.value == "batch_update"]
        assert len(batch_operations) >= 1

        operation = batch_operations[0]
        result = validator.validate_operation(
            operation,
            expected_type="batch_update",
            expected_confidence_min=0.7,
        )

        assert result["valid"] is True

    def test_mixed_editor_patterns(self, simulator, validator):
        """Test mixed patterns from different editors."""
        all_events = []

        # VSCode save
        all_events.extend(simulator.simulate_vscode_save("vscode_file.js", 1024))

        # Vim save
        all_events.extend(simulator.simulate_vim_save("vim_file.py", 1200))

        # Safe write
        all_events.extend(simulator.simulate_safe_write("safe_file.txt", 800))

        # Batch operation
        all_events.extend(simulator.simulate_batch_operation(5, "batch", ".ts", 600))

        operations = simulator.detect_operations(all_events)

        # Should detect multiple different operation types
        operation_types = {op.operation_type.value for op in operations}
        assert len(operation_types) >= 2  # At least 2 different types

        # Validate each operation
        for operation in operations:
            if operation.operation_type.value == "atomic_save":
                result = validator.validate_operation(
                    operation, expected_type="atomic_save", expected_confidence_min=0.8
                )
                assert result["valid"] is True
            elif operation.operation_type.value == "safe_write":
                result = validator.validate_operation(
                    operation, expected_type="safe_write", expected_confidence_min=0.8
                )
                assert result["valid"] is True
            elif operation.operation_type.value == "batch_update":
                result = validator.validate_operation(
                    operation, expected_type="batch_update", expected_confidence_min=0.7
                )
                assert result["valid"] is True


@requires_file_operations
class TestFileTypeSpecificPatterns:
    """Test patterns specific to different file types."""

    def test_python_file_patterns(self, simulator, validator):
        """Test patterns specific to Python files."""
        # Python files often get formatted with black/autopep8
        events = simulator.simulate_batch_operation(8, "python_module", ".py", 1200)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        batch_ops = [op for op in operations if op.operation_type.value == "batch_update"]
        assert len(batch_ops) >= 1

        # Validate Python-specific operation
        operation = batch_ops[0]
        result = validator.validate_operation(
            operation,
            expected_type="batch_update",
            expected_confidence_min=0.7,
        )
        assert result["valid"] is True

    def test_javascript_file_patterns(self, simulator, validator):
        """Test patterns specific to JavaScript files."""
        # JavaScript files with VSCode/Prettier
        events = simulator.simulate_vscode_save("app.js", 2048)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        atomic_ops = [op for op in operations if op.operation_type.value == "atomic_save"]
        assert len(atomic_ops) >= 1

    def test_config_file_patterns(self, simulator, validator):
        """Test patterns for configuration files."""
        # Config files often use safe write
        events = simulator.simulate_safe_write("config.json", 512)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        safe_ops = [op for op in operations if op.operation_type.value == "safe_write"]
        assert len(safe_ops) >= 1

    def test_large_file_patterns(self, simulator, validator):
        """Test patterns for large files."""
        # Large files might use different save strategies
        events = simulator.simulate_safe_write("large_dataset.csv", 50 * 1024 * 1024)  # 50MB
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        # Should handle large files without issues
        for operation in operations:
            assert operation.confidence >= 0.0


@requires_file_operations
class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_developer_workflow_scenario(self, simulator, validator):
        """Test a complete developer workflow."""
        # Test each operation separately to ensure they're detected properly

        # 1. Developer opens and edits a file in VSCode
        vscode_events = simulator.simulate_vscode_save("main.py", 1024)
        vscode_operations = simulator.detect_operations(vscode_events)
        assert len(vscode_operations) >= 1

        # 2. Makes a backup before major refactoring
        safe_events = simulator.simulate_safe_write("config.py", 1024)  # Different file
        safe_operations = simulator.detect_operations(safe_events)
        assert len(safe_operations) >= 1

        # 3. Code formatter runs on multiple files
        batch_events = simulator.simulate_batch_operation(15, "src_file", ".py", 800)
        batch_operations = simulator.detect_operations(batch_events)
        assert len(batch_operations) >= 1

        # Combine all operations for analysis
        all_operations = vscode_operations + safe_operations + batch_operations

        # Should detect multiple operations
        assert len(all_operations) >= 3

        # Should include different operation types
        operation_types = {op.operation_type.value for op in all_operations}
        assert "atomic_save" in operation_types
        expected_types = {"safe_write", "batch_update"}
        assert len(operation_types.intersection(expected_types)) >= 1

        # All operations should have reasonable confidence
        for operation in all_operations:
            assert operation.confidence >= 0.7

    def test_concurrent_editor_scenario(self, simulator, validator):
        """Test scenario with multiple editors working simultaneously."""
        all_events = []

        # VSCode editing one file
        all_events.extend(simulator.simulate_vscode_save("frontend.js", 2048))

        # Vim editing another file (interleaved timing)
        all_events.extend(simulator.simulate_vim_save("backend.py", 1536))

        # Batch operation (could be from IDE or external tool)
        all_events.extend(simulator.simulate_batch_operation(6, "component", ".tsx", 1200))

        operations = simulator.detect_operations(all_events)

        # Should handle concurrent operations
        assert len(operations) >= 2

        # Each operation should be valid
        for operation in operations:
            result = validator.validate_operation(
                operation,
                expected_type=operation.operation_type.value,
                expected_confidence_min=0.6,  # Lower threshold for complex scenario
            )
            assert result["valid"] is True

    def test_error_recovery_scenario(self, simulator, validator):
        """Test error recovery and backup scenarios."""
        all_events = []

        # Initial safe write with backup
        all_events.extend(simulator.simulate_safe_write("critical.data", 8192))

        # Multiple backup operations (recovery scenario)
        for i in range(3):
            all_events.extend(simulator.simulate_safe_write(f"critical.data.backup{i}", 8192))

        operations = simulator.detect_operations(all_events)

        # Should detect safe write operations
        safe_operations = [op for op in operations if op.operation_type.value == "safe_write"]
        assert len(safe_operations) >= 2

        # All should have backup flag
        for operation in safe_operations:
            assert operation.has_backup is True

    def test_performance_critical_scenario(self, simulator, validator):
        """Test scenario with many rapid operations."""
        all_events = []

        # Rapid sequence of saves (auto-save scenario)
        for i in range(20):
            all_events.extend(simulator.simulate_vscode_save(f"autosave_{i}.tmp", 512))

        operations = simulator.detect_operations(all_events)

        # Should handle rapid operations efficiently
        assert len(operations) >= 10  # Should detect most saves

        # Performance should be reasonable (this is implicit in the test passing quickly)
        operation_types = {op.operation_type.value for op in operations}
        assert "atomic_save" in operation_types


@requires_file_operations
class TestValidationScenarios:
    """Test validation scenarios with different expectations."""

    def test_validation_summary_comprehensive(self, simulator, validator):
        """Test comprehensive validation summary."""
        # Generate varied patterns
        patterns = simulator.simulate_all_patterns()

        all_operations = []
        for pattern_name, events in patterns.items():
            operations = simulator.detect_operations(events)
            all_operations.extend(operations)

        # Validate each operation
        for operation in all_operations:
            validator.validate_operation(
                operation,
                expected_type=operation.operation_type.value,
                expected_confidence_min=0.5,  # Liberal threshold
            )

        # Check summary
        summary = validator.get_summary()
        assert summary["total"] > 0
        assert summary["success_rate"] >= 0.8  # Should have high success rate
        assert summary["average_confidence"] >= 0.7

    def test_strict_validation_scenario(self, simulator, validator):
        """Test strict validation requirements."""
        # Generate high-quality VSCode save
        events = simulator.simulate_vscode_save("strict_test.txt", 1024)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        operation = operations[0]

        # Very strict validation
        result = validator.validate_operation(
            operation,
            expected_type="atomic_save",
            expected_confidence_min=0.95,  # Very high threshold
            expected_atomic=True,
            expected_safe=True,
        )

        # Should pass strict validation for VSCode pattern
        assert result["valid"] is True
        assert result["confidence"] >= 0.95

    def test_failure_case_validation(self, simulator, validator):
        """Test validation failure cases."""
        events = simulator.simulate_vscode_save("test.txt", 1024)
        operations = simulator.detect_operations(events)

        assert len(operations) >= 1
        operation = operations[0]

        # Validate with wrong expectations (should fail)
        result = validator.validate_operation(
            operation,
            expected_type="batch_update",  # Wrong type
            expected_confidence_min=0.99,  # Unrealistic threshold
            expected_atomic=False,  # Wrong atomic flag
        )

        # Should fail validation
        assert result["valid"] is False
        assert len(result["errors"]) >= 2  # Multiple validation errors


if __name__ == "__main__":
    pytest.main([__file__])