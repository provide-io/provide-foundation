#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for file operations quality analysis module."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations import FileEvent, FileEventMetadata
from provide.foundation.file.quality import (
    AnalysisMetric,
    OperationScenario,
    QualityAnalyzer,
    QualityResult,
    create_scenarios_from_patterns,
)


class TestQualityAnalyzer(FoundationTestCase):
    """Test the quality analyzer functionality."""

    def test_analyzer_initialization(self) -> None:
        """Test analyzer initialization."""
        analyzer = QualityAnalyzer()
        assert analyzer.detector is not None
        assert len(analyzer.scenarios) == 0
        assert len(analyzer.results) == 0

    def test_analyzer_with_custom_detector(self) -> None:
        """Test analyzer with custom detector."""
        from provide.foundation.file.operations import OperationDetector

        detector = OperationDetector()
        analyzer = QualityAnalyzer(detector)
        assert analyzer.detector is detector

    def test_add_scenario(self) -> None:
        """Test adding scenarios."""
        analyzer = QualityAnalyzer()
        scenarios = create_scenarios_from_patterns()
        for scenario in scenarios:
            analyzer.add_scenario(scenario)
        assert len(analyzer.scenarios) == len(scenarios)

    def test_run_analysis_without_scenarios(self) -> None:
        """Test running analysis without scenarios raises error."""
        analyzer = QualityAnalyzer()
        with pytest.raises(ValueError, match="No scenarios available for analysis"):
            analyzer.run_analysis()

    def test_run_analysis_with_vscode_scenario(self) -> None:
        """Test running analysis with VSCode atomic save scenario."""
        analyzer = QualityAnalyzer()
        scenarios = create_scenarios_from_patterns()
        vscode_scenario = next(s for s in scenarios if s.name == "vscode_atomic_save")
        analyzer.add_scenario(vscode_scenario)
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.DETECTION_TIME])
        assert len(results) == 2
        assert AnalysisMetric.ACCURACY in results
        accuracy_result = results[AnalysisMetric.ACCURACY]
        assert 0.0 <= accuracy_result.value <= 1.0

    def test_generate_report(self) -> None:
        """Test report generation."""
        analyzer = QualityAnalyzer()
        scenarios = create_scenarios_from_patterns()
        analyzer.add_scenario(scenarios[0])
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.DETECTION_TIME])
        report = analyzer.generate_report(results)
        assert "File Operation Detection Quality Report" in report
        assert "Accuracy" in report
        assert "Detection Time" in report

    def test_generate_report_without_results(self) -> None:
        """Test report generation without results."""
        analyzer = QualityAnalyzer()
        report = analyzer.generate_report()
        assert "No analysis results available" in report


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
        assert isinstance(result.timestamp, datetime)


class TestOperationScenario(FoundationTestCase):
    """Test the operation scenario functionality."""

    def test_scenario_creation(self) -> None:
        """Test creating scenarios."""
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
            description="Test scenario",
            tags=["test", "atomic"],
        )
        assert scenario.name == "test"
        assert len(scenario.events) == 1
        assert "test" in scenario.tags


class TestCreateScenariosFromPatterns(FoundationTestCase):
    """Test the standard scenario creation."""

    def test_create_standard_scenarios(self) -> None:
        """Test creating standard scenarios."""
        scenarios = create_scenarios_from_patterns()
        assert len(scenarios) >= 3
        names = [sc.name for sc in scenarios]
        assert "vscode_atomic_save" in names
        assert "safe_write_with_backup" in names
        assert "batch_format_operation" in names


# 🧱🏗️🔚
