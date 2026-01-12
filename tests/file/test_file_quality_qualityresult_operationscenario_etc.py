#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operation quality analysis."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
)
from provide.foundation.file.quality import (
    AnalysisMetric,
    OperationScenario,
    QualityResult,
    create_scenarios_from_patterns,
)


class TestQualityResult(FoundationTestCase):
    """Test the quality result functionality."""

    def test_quality_result_creation(self) -> None:
        """Test creating quality results."""
        result = QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=0.95,
            details={"test": "value"},
        )

        assert result.metric == AnalysisMetric.ACCURACY
        assert result.value == 0.95
        assert result.details["test"] == "value"
        assert isinstance(result.timestamp, datetime)


class TestOperationScenario(FoundationTestCase):
    """Test the operation test case functionality."""

    def test_scenario_creation(self) -> None:
        """Test creating test cases."""
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
            )
        ]

        scenario = OperationScenario(
            name="test",
            events=events,
            expected_operations=[{"type": "atomic_save"}],
            description="Test case",
            tags=["test", "atomic"],
        )

        assert scenario.name == "test"
        assert len(scenario.events) == 1
        assert len(scenario.expected_operations) == 1
        assert scenario.description == "Test case"
        assert "test" in scenario.tags


class TestCreateTestCasesFromPatterns(FoundationTestCase):
    """Test the standard test case creation."""

    def test_create_standard_scenarios(self) -> None:
        """Test creating standard test cases."""
        scenarios = create_scenarios_from_patterns()

        assert len(scenarios) >= 3  # Should have at least VSCode, safe write, and batch

        # Check test case names
        names = [tc.name for tc in scenarios]
        assert "vscode_atomic_save" in names
        assert "safe_write_with_backup" in names
        assert "batch_format_operation" in names

        # Check that each test case has events and expected operations
        for scenario in scenarios:
            assert len(scenario.events) > 0
            assert len(scenario.expected_operations) > 0
            assert scenario.description
            assert len(scenario.tags) > 0

    def test_vscode_scenario_structure(self) -> None:
        """Test VSCode test case has correct structure."""
        scenarios = create_scenarios_from_patterns()
        vscode_case = next(tc for tc in scenarios if tc.name == "vscode_atomic_save")

        assert len(vscode_case.events) == 2
        assert vscode_case.events[0].event_type == "created"
        assert vscode_case.events[1].event_type == "moved"
        assert "tmp" in str(vscode_case.events[0].path)
        assert vscode_case.expected_operations[0]["type"] == "atomic_save"


if __name__ == "__main__":
    pytest.main([__file__])

# 🧱🏗️🔚
