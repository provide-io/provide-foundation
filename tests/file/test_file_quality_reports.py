#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for QualityAnalyzer report generation and edge case handling."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from provide.testkit import FoundationTestCase

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
)
from provide.foundation.file.quality import (
    AnalysisMetric,
    OperationScenario,
    QualityAnalyzer,
)


class TestQualityAnalyzerReports(FoundationTestCase):
    """Test QualityAnalyzer report generation and edge cases."""

    def test_generate_report(self) -> None:
        """Test report generation."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Add a simple test case
        events = [
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        scenario = OperationScenario(
            name="simple_test",
            events=events,
            expected_operations=[],
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.DETECTION_TIME])

        report = analyzer.generate_report(results)

        assert "File Operation Detection Quality Report" in report
        assert "Accuracy" in report
        assert "Detection Time" in report
        assert "Scenarios: 1" in report

    def test_generate_report_without_results(self) -> None:
        """Test report generation without results."""
        analyzer = QualityAnalyzer()
        report = analyzer.generate_report()
        assert "No analysis results available" in report

    def test_report_with_confidence_distribution_details(self) -> None:
        """Test report generation includes confidence distribution details."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create multiple scenarios
        for i in range(2):
            events = [
                FileEvent(
                    path=Path(f"test{i}.txt.tmp"),
                    event_type="created",
                    metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
                ),
                FileEvent(
                    path=Path(f"test{i}.txt.tmp"),
                    event_type="moved",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                    ),
                    dest_path=Path(f"test{i}.txt"),
                ),
            ]

            scenario = OperationScenario(
                name=f"test{i}", events=events, expected_operations=[{"type": "atomic_save"}]
            )
            analyzer.add_scenario(scenario)

        results = analyzer.run_analysis(
            [AnalysisMetric.CONFIDENCE_DISTRIBUTION, AnalysisMetric.DETECTION_TIME, AnalysisMetric.ACCURACY]
        )
        report = analyzer.generate_report(results)

        # Check for confidence distribution details
        assert "Confidence Distribution" in report
        assert "By operation type:" in report

        # Check for detection time details
        assert "Detection Time" in report
        assert "avg:" in report
        assert "p95:" in report

        # Check for accuracy details
        assert "Accuracy" in report

    def test_generate_report_without_results_parameter(self) -> None:
        """Test report generation uses latest results when no results provided."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a simple scenario
        events = [
            FileEvent(
                path=Path("test.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
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

        scenario = OperationScenario(name="test", events=events, expected_operations=[{"type": "atomic_save"}])

        analyzer.add_scenario(scenario)

        # Run analysis (stores results internally)
        analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.PRECISION])

        # Generate report without providing results - should use latest
        report = analyzer.generate_report()

        assert "File Operation Detection Quality Report" in report
        assert "Scenarios: 1" in report


class TestQualityAnalyzerFalseRates(FoundationTestCase):
    """Test false positive and false negative rate calculations."""

    def test_false_positive_false_negative_metrics(self) -> None:
        """Test false positive and false negative rate metrics."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Scenario with no expected operations (to test false positive rate)
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        scenario = OperationScenario(
            name="no_operations",
            events=events,
            expected_operations=[],
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis(
            [AnalysisMetric.FALSE_POSITIVE_RATE, AnalysisMetric.FALSE_NEGATIVE_RATE]
        )

        fpr = results[AnalysisMetric.FALSE_POSITIVE_RATE]
        assert 0.0 <= fpr.value <= 1.0
        assert "false_positives" in fpr.details
        assert "total_negative_cases" in fpr.details

        fnr = results[AnalysisMetric.FALSE_NEGATIVE_RATE]
        assert 0.0 <= fnr.value <= 1.0
        assert "false_negatives" in fnr.details
        assert "total_positive_cases" in fnr.details

    def test_false_positive_rate_with_no_expected_no_detected(self) -> None:
        """Test FPR when there are no expected and no detected operations."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Single event that won't trigger detection
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        scenario = OperationScenario(name="no_ops", events=events, expected_operations=[])

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.FALSE_POSITIVE_RATE])

        fpr = results[AnalysisMetric.FALSE_POSITIVE_RATE]
        assert "total_negative_cases" in fpr.details
        assert fpr.details["total_negative_cases"] > 0

    def test_false_negative_rate_calculation(self) -> None:
        """Test false negative rate with expected operations not detected."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Simple event that won't match complex expected operation
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        # Expect an operation that won't be detected
        scenario = OperationScenario(
            name="fnr_test",
            events=events,
            expected_operations=[{"type": "batch_format"}],
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.FALSE_NEGATIVE_RATE])

        fnr = results[AnalysisMetric.FALSE_NEGATIVE_RATE]
        assert "false_negatives" in fnr.details
        assert "total_positive_cases" in fnr.details


# 🧱🏗️🔚
