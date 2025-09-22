"""Tests for file operation quality analysis."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from provide.foundation.file.operations import (
    FileEvent,
    FileEventMetadata,
    OperationDetector,
)
from provide.foundation.file.quality import (
    AnalysisMetric,
    OperationTestCase,
    QualityAnalyzer,
    QualityResult,
    create_test_cases_from_patterns,
)


class TestQualityAnalyzer:
    """Test the quality analyzer functionality."""

    def test_analyzer_initialization(self) -> None:
        """Test analyzer initialization."""
        analyzer = QualityAnalyzer()
        assert analyzer.detector is not None
        assert len(analyzer.test_cases) == 0
        assert len(analyzer.results) == 0

    def test_analyzer_with_custom_detector(self) -> None:
        """Test analyzer with custom detector."""
        detector = OperationDetector()
        analyzer = QualityAnalyzer(detector)
        assert analyzer.detector is detector

    def test_add_test_case(self) -> None:
        """Test adding test cases."""
        analyzer = QualityAnalyzer()

        test_case = OperationTestCase(
            name="test_case",
            events=[],
            expected_operations=[],
            description="Test case",
        )

        analyzer.add_test_case(test_case)
        assert len(analyzer.test_cases) == 1
        assert analyzer.test_cases[0] == test_case

    def test_run_analysis_without_test_cases(self) -> None:
        """Test running analysis without test cases raises error."""
        analyzer = QualityAnalyzer()

        with pytest.raises(ValueError, match="No test cases available"):
            analyzer.run_analysis()

    def test_run_analysis_with_vscode_test_case(self) -> None:
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
                metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=50), sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        test_case = OperationTestCase(
            name="vscode_save",
            events=events,
            expected_operations=[{"type": "atomic_save", "confidence_min": 0.9}],
            description="VSCode atomic save",
        )

        analyzer.add_test_case(test_case)

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

        test_case = OperationTestCase(
            name="safe_write",
            events=events,
            expected_operations=[{"type": "safe_write"}],
            description="Safe write operation",
        )

        analyzer.add_test_case(test_case)
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
                    metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=50), sequence_number=2),
                    dest_path=Path(f"test{i}.txt"),
                ),
            ]

            test_case = OperationTestCase(
                name=f"atomic_save_{i}",
                events=events,
                expected_operations=[{"type": "atomic_save"}],
            )
            analyzer.add_test_case(test_case)

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

        test_case = OperationTestCase(
            name="simple_test",
            events=events,
            expected_operations=[],
        )

        analyzer.add_test_case(test_case)
        results = analyzer.run_analysis([AnalysisMetric.ACCURACY, AnalysisMetric.DETECTION_TIME])

        report = analyzer.generate_report(results)

        assert "File Operation Detection Quality Report" in report
        assert "Accuracy" in report
        assert "Detection Time" in report
        assert "Test Cases: 1" in report

    def test_generate_report_without_results(self) -> None:
        """Test report generation without results."""
        analyzer = QualityAnalyzer()
        report = analyzer.generate_report()
        assert "No analysis results available" in report


class TestQualityResult:
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


class TestOperationTestCase:
    """Test the operation test case functionality."""

    def test_test_case_creation(self) -> None:
        """Test creating test cases."""
        events = [
            FileEvent(
                path=Path("test.txt"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=datetime.now(), sequence_number=1),
            )
        ]

        test_case = OperationTestCase(
            name="test",
            events=events,
            expected_operations=[{"type": "atomic_save"}],
            description="Test case",
            tags=["test", "atomic"],
        )

        assert test_case.name == "test"
        assert len(test_case.events) == 1
        assert len(test_case.expected_operations) == 1
        assert test_case.description == "Test case"
        assert "test" in test_case.tags


class TestCreateTestCasesFromPatterns:
    """Test the standard test case creation."""

    def test_create_standard_test_cases(self) -> None:
        """Test creating standard test cases."""
        test_cases = create_test_cases_from_patterns()

        assert len(test_cases) >= 3  # Should have at least VSCode, safe write, and batch

        # Check test case names
        names = [tc.name for tc in test_cases]
        assert "vscode_atomic_save" in names
        assert "safe_write_with_backup" in names
        assert "batch_format_operation" in names

        # Check that each test case has events and expected operations
        for test_case in test_cases:
            assert len(test_case.events) > 0
            assert len(test_case.expected_operations) > 0
            assert test_case.description
            assert len(test_case.tags) > 0

    def test_vscode_test_case_structure(self) -> None:
        """Test VSCode test case has correct structure."""
        test_cases = create_test_cases_from_patterns()
        vscode_case = next(tc for tc in test_cases if tc.name == "vscode_atomic_save")

        assert len(vscode_case.events) == 2
        assert vscode_case.events[0].event_type == "created"
        assert vscode_case.events[1].event_type == "moved"
        assert "tmp" in str(vscode_case.events[0].path)
        assert vscode_case.expected_operations[0]["type"] == "atomic_save"


if __name__ == "__main__":
    pytest.main([__file__])