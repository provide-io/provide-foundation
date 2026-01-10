#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for basic QualityAnalyzer functionality - initialization and scenario management."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase
import pytest

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)
from provide.foundation.file.quality import (
    AnalysisMetric,
    OperationScenario,
    QualityAnalyzer,
)


class TestQualityAnalyzerBasic(FoundationTestCase):
    """Test basic QualityAnalyzer functionality."""

    def test_analyzer_initialization(self) -> None:
        """Test analyzer initialization."""
        analyzer = QualityAnalyzer()
        assert analyzer.detector is not None
        assert len(analyzer.scenarios) == 0
        assert len(analyzer.results) == 0

    def test_analyzer_with_custom_detector(self) -> None:
        """Test analyzer with custom detector."""
        detector = OperationDetector()
        analyzer = QualityAnalyzer(detector)
        assert analyzer.detector is detector

    def test_add_scenario(self) -> None:
        """Test adding test cases."""
        analyzer = QualityAnalyzer()

        scenario = OperationScenario(
            name="scenario",
            events=[],
            expected_operations=[],
            description="Test case",
        )

        analyzer.add_scenario(scenario)
        assert len(analyzer.scenarios) == 1
        assert analyzer.scenarios[0] == scenario

    def test_run_analysis_without_scenarios(self) -> None:
        """Test running analysis without test cases raises error."""
        analyzer = QualityAnalyzer()

        with pytest.raises(ValueError, match="No scenarios available"):
            analyzer.run_analysis()

    def test_run_analysis_with_vscode_scenario(self) -> None:
        """Test running analysis with VSCode atomic save test case."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create VSCode atomic save test case
        events = [
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=1024),
            ),
            FileEvent(
                path=Path("test.txt.tmp.12345"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                ),
                dest_path=Path("test.txt"),
            ),
        ]

        scenario = OperationScenario(
            name="vscode_save",
            events=events,
            expected_operations=[{"type": "atomic_save", "confidence_min": 0.9}],
            description="VSCode atomic save",
        )

        analyzer.add_scenario(scenario)

        # Run analysis with specific metrics
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.DETECTION_TIME])

        assert len(results) == 2
        assert AnalysisMetric.ACCURACY in results
        assert AnalysisMetric.DETECTION_TIME in results

        accuracy_result = results[AnalysisMetric.ACCURACY]
        assert accuracy_result.value >= 0.0
        assert accuracy_result.value <= 1.0
        assert "correct_detections" in accuracy_result.details

        timing_result = results[AnalysisMetric.DETECTION_TIME]
        assert timing_result.value >= 0.0
        assert "average_ms" in timing_result.details

    def test_run_analysis_all_metrics(self) -> None:
        """Test running analysis with all metrics."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a scenario
        events = [
            FileEvent(
                path=Path("test.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=1024),
            ),
            FileEvent(
                path=Path("test.txt.tmp"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                ),
                dest_path=Path("test.txt"),
            ),
        ]

        scenario = OperationScenario(
            name="atomic_save",
            events=events,
            expected_operations=[{"type": "atomic_save"}],
        )

        analyzer.add_scenario(scenario)

        # Run analysis without specifying metrics (should run all)
        results = analyzer.run_analysis()

        # Should have all metrics
        assert len(results) == len(AnalysisMetric)
        assert AnalysisMetric.PRECISION in results
        assert AnalysisMetric.RECALL in results
        assert AnalysisMetric.F1_SCORE in results
        assert AnalysisMetric.FALSE_POSITIVE_RATE in results
        assert AnalysisMetric.FALSE_NEGATIVE_RATE in results


# 🧱🏗️🔚
