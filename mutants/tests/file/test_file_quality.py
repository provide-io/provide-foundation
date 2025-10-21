"""Tests for file operation quality analysis."""

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

    def test_accuracy_calculation(self) -> None:
        """Test accuracy calculation with perfect match."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a test case that should be detected correctly
        events = [
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

        scenario = OperationScenario(
            name="safe_write",
            events=events,
            expected_operations=[{"type": "safe_write"}],
            description="Safe write operation",
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY])

        accuracy = results[AnalysisMetric.ACCURACY]
        # Should have reasonable accuracy
        assert accuracy.value > 0.0
        assert accuracy.details["total_detections"] > 0

    def test_confidence_distribution_analysis(self) -> None:
        """Test confidence distribution analysis."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Add multiple test cases
        for i in range(3):
            events = [
                FileEvent(
                    path=Path(f"test{i}.txt.tmp.{i}"),
                    event_type="created",
                    metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
                ),
                FileEvent(
                    path=Path(f"test{i}.txt.tmp.{i}"),
                    event_type="moved",
                    metadata=FileEventMetadata(
                        timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                    ),
                    dest_path=Path(f"test{i}.txt"),
                ),
            ]

            scenario = OperationScenario(
                name=f"atomic_save_{i}",
                events=events,
                expected_operations=[{"type": "atomic_save"}],
            )
            analyzer.add_scenario(scenario)

        results = analyzer.run_analysis([AnalysisMetric.CONFIDENCE_DISTRIBUTION])

        confidence_result = results[AnalysisMetric.CONFIDENCE_DISTRIBUTION]
        assert "total_operations" in confidence_result.details
        assert "by_type" in confidence_result.details
        assert confidence_result.value >= 0.0
        assert confidence_result.value <= 1.0

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

    def test_precision_recall_f1_metrics(self) -> None:
        """Test precision, recall, and F1 score metrics."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a scenario with expected atomic save
        events = [
            FileEvent(
                path=Path("doc.txt.tmp"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=Path("doc.txt.tmp"),
                event_type="moved",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=50), sequence_number=2
                ),
                dest_path=Path("doc.txt"),
            ),
        ]

        scenario = OperationScenario(
            name="test",
            events=events,
            expected_operations=[{"type": "atomic_save"}],
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis(
            [AnalysisMetric.PRECISION, AnalysisMetric.RECALL, AnalysisMetric.F1_SCORE]
        )

        precision = results[AnalysisMetric.PRECISION]
        assert 0.0 <= precision.value <= 1.0
        assert "true_positives" in precision.details
        assert "false_positives" in precision.details

        recall = results[AnalysisMetric.RECALL]
        assert 0.0 <= recall.value <= 1.0
        assert "true_positives" in recall.details
        assert "false_negatives" in recall.details

        f1 = results[AnalysisMetric.F1_SCORE]
        assert 0.0 <= f1.value <= 1.0
        assert "precision" in f1.details
        assert "recall" in f1.details

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

    def test_precision_with_false_positives(self) -> None:
        """Test precision calculation when detector reports false positives."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Scenario: Expect one operation but detector finds different operation
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt"),
                event_type="modified",
                metadata=FileEventMetadata(
                    timestamp=base_time + timedelta(milliseconds=100), sequence_number=2
                ),
            ),
        ]

        # Expect no operations, but detector will likely find some
        scenario = OperationScenario(name="false_positive_test", events=events, expected_operations=[])

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.PRECISION])

        precision = results[AnalysisMetric.PRECISION]
        assert "false_positives" in precision.details

    def test_recall_with_false_negatives(self) -> None:
        """Test recall calculation when detector misses expected operations."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a scenario where we expect an operation but detector might miss it
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        # Expect an operation that won't be detected from a simple create event
        scenario = OperationScenario(
            name="false_negative_test",
            events=events,
            expected_operations=[{"type": "batch_format"}],  # Won't be detected
        )

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.RECALL])

        recall = results[AnalysisMetric.RECALL]
        assert "false_negatives" in recall.details
        assert recall.details["false_negatives"] > 0

    def test_confidence_distribution_with_no_detections(self) -> None:
        """Test confidence distribution when no operations are detected."""
        analyzer = QualityAnalyzer()
        base_time = datetime.now()

        # Create a scenario with minimal events that won't trigger detection
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
        ]

        scenario = OperationScenario(name="no_detection", events=events, expected_operations=[])

        analyzer.add_scenario(scenario)
        results = analyzer.run_analysis([AnalysisMetric.CONFIDENCE_DISTRIBUTION])

        confidence = results[AnalysisMetric.CONFIDENCE_DISTRIBUTION]
        # Should handle empty results gracefully
        assert confidence.value >= 0.0

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
