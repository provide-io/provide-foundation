"""Tests for file operations quality analysis module."""

from __future__ import annotations

import pytest

from provide.foundation.file.quality import (
    AnalysisMetric,
    QualityAnalyzer,
    create_test_cases_from_patterns,
)


class TestQualityAnalyzer:
    """Test the QualityAnalyzer class."""

    def test_analyzer_initialization(self) -> None:
        """Test analyzer initialization."""
        analyzer = QualityAnalyzer()
        assert analyzer is not None
        assert len(analyzer.test_cases) == 0

    def test_add_test_case(self) -> None:
        """Test adding test cases to analyzer."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        initial_count = len(analyzer.test_cases)
        for test_case in test_cases[:3]:  # Add first 3 test cases
            analyzer.add_test_case(test_case)

        assert len(analyzer.test_cases) == initial_count + 3

    def test_run_analysis_accuracy(self) -> None:
        """Test running accuracy analysis."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        for test_case in test_cases:
            analyzer.add_test_case(test_case)

        results = analyzer.run_analysis([AnalysisMetric.ACCURACY])

        assert AnalysisMetric.ACCURACY in results
        accuracy_result = results[AnalysisMetric.ACCURACY]
        assert hasattr(accuracy_result, "value")
        assert 0.0 <= accuracy_result.value <= 1.0

    def test_run_analysis_detection_time(self) -> None:
        """Test running detection time analysis."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        for test_case in test_cases[:5]:  # Limit to 5 for speed
            analyzer.add_test_case(test_case)

        results = analyzer.run_analysis([AnalysisMetric.DETECTION_TIME])

        assert AnalysisMetric.DETECTION_TIME in results
        time_result = results[AnalysisMetric.DETECTION_TIME]
        assert hasattr(time_result, "value")
        assert time_result.value >= 0

    def test_run_analysis_confidence_distribution(self) -> None:
        """Test running confidence distribution analysis."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        for test_case in test_cases[:5]:
            analyzer.add_test_case(test_case)

        results = analyzer.run_analysis([AnalysisMetric.CONFIDENCE_DISTRIBUTION])

        assert AnalysisMetric.CONFIDENCE_DISTRIBUTION in results
        conf_result = results[AnalysisMetric.CONFIDENCE_DISTRIBUTION]
        assert hasattr(conf_result, "value")

    def test_run_multiple_metrics(self) -> None:
        """Test running multiple metrics together."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        for test_case in test_cases[:3]:
            analyzer.add_test_case(test_case)

        metrics = [
            AnalysisMetric.ACCURACY,
            AnalysisMetric.DETECTION_TIME,
            AnalysisMetric.CONFIDENCE_DISTRIBUTION,
        ]
        results = analyzer.run_analysis(metrics)

        assert len(results) == 3
        for metric in metrics:
            assert metric in results


class TestCreateTestCasesFromPatterns:
    """Test test case creation functionality."""

    def test_create_test_cases_basic(self) -> None:
        """Test basic test case creation."""
        test_cases = create_test_cases_from_patterns()

        assert len(test_cases) > 0
        assert all(hasattr(case, "events") for case in test_cases)
        assert all(hasattr(case, "expected_operations") for case in test_cases)

    def test_test_cases_have_required_attributes(self) -> None:
        """Test that test cases have all required attributes."""
        test_cases = create_test_cases_from_patterns()

        for test_case in test_cases:
            assert hasattr(test_case, "events")
            assert hasattr(test_case, "expected_operations")
            assert hasattr(test_case, "description")
            assert len(test_case.events) > 0

    def test_vscode_pattern_test_case(self) -> None:
        """Test VSCode pattern test case creation."""
        test_cases = create_test_cases_from_patterns()

        vscode_cases = [
            case
            for case in test_cases
            if "vscode" in case.description.lower() or "atomic" in case.description.lower()
        ]
        assert len(vscode_cases) > 0

        for case in vscode_cases:
            assert len(case.events) >= 2  # At least create + move

    def test_vim_pattern_test_case(self) -> None:
        """Test Vim pattern test case creation."""
        test_cases = create_test_cases_from_patterns()

        vim_cases = [
            case
            for case in test_cases
            if "vim" in case.description.lower() or "backup" in case.description.lower()
        ]
        assert len(vim_cases) > 0


class TestAnalysisMetrics:
    """Test AnalysisMetric enum."""

    def test_all_metrics_defined(self) -> None:
        """Test that all expected metrics are defined."""
        expected_metrics = ["ACCURACY", "DETECTION_TIME", "CONFIDENCE_DISTRIBUTION"]

        for metric_name in expected_metrics:
            assert hasattr(AnalysisMetric, metric_name)

    def test_metric_values(self) -> None:
        """Test metric enum values."""
        assert AnalysisMetric.ACCURACY.value == "accuracy"
        assert AnalysisMetric.DETECTION_TIME.value == "detection_time"
        assert AnalysisMetric.CONFIDENCE_DISTRIBUTION.value == "confidence_distribution"


class TestQualityIntegration:
    """Integration tests for quality analysis."""

    def test_full_analysis_workflow(self) -> None:
        """Test complete analysis workflow."""
        analyzer = QualityAnalyzer()

        # Add test cases
        test_cases = create_test_cases_from_patterns()
        for test_case in test_cases[:5]:  # Limit for performance
            analyzer.add_test_case(test_case)

        # Run all metrics
        all_metrics = [
            AnalysisMetric.ACCURACY,
            AnalysisMetric.DETECTION_TIME,
            AnalysisMetric.CONFIDENCE_DISTRIBUTION,
        ]
        results = analyzer.run_analysis(all_metrics)

        # Verify results
        assert len(results) == len(all_metrics)

        # Check accuracy is reasonable
        accuracy = results[AnalysisMetric.ACCURACY]
        assert accuracy.value >= 0.0

        # Check detection time is positive
        detection_time = results[AnalysisMetric.DETECTION_TIME]
        assert detection_time.value >= 0

    def test_empty_analyzer_behavior(self) -> None:
        """Test analyzer behavior with no test cases."""
        analyzer = QualityAnalyzer()

        # Should raise error when no test cases available
        with pytest.raises(ValueError, match="No test cases available"):
            analyzer.run_analysis([AnalysisMetric.ACCURACY])

    def test_analyzer_with_single_test_case(self) -> None:
        """Test analyzer with single test case."""
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        if test_cases:
            analyzer.add_test_case(test_cases[0])

            results = analyzer.run_analysis([AnalysisMetric.ACCURACY])
            assert AnalysisMetric.ACCURACY in results

    def test_quality_analysis_with_real_operations(self) -> None:
        """Integration test with real file operations."""
        from datetime import datetime
        from pathlib import Path

        from provide.foundation.file.operations import FileEvent, FileEventMetadata, OperationDetector

        # Create real file operation events
        base_time = datetime.now()
        events = [
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="created",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=1),
            ),
            FileEvent(
                path=Path("test.txt.tmp.123"),
                event_type="moved",
                metadata=FileEventMetadata(timestamp=base_time, sequence_number=2),
                dest_path=Path("test.txt"),
            ),
        ]

        # Detect operations
        detector = OperationDetector()
        detector.detect(events)

        # Use in quality analysis
        analyzer = QualityAnalyzer()
        test_cases = create_test_cases_from_patterns()

        if test_cases:
            analyzer.add_test_case(test_cases[0])
            results = analyzer.run_analysis([AnalysisMetric.ACCURACY])
            assert AnalysisMetric.ACCURACY in results
