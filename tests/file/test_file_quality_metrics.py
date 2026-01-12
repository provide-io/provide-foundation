#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for QualityAnalyzer metric calculations - accuracy, precision, recall, F1, confidence."""

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


class TestQualityAnalyzerMetrics(FoundationTestCase):
    """Test QualityAnalyzer metric calculation functionality."""

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


# 🧱🏗️🔚
