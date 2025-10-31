#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Quality analyzer for file operation detection."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
import time
from typing import Any

try:
    from provide.foundation.file.operations import OperationDetector

    HAS_OPERATIONS_MODULE = True
except ImportError:
    HAS_OPERATIONS_MODULE = False

from provide.foundation.file.quality.metrics import AnalysisMetric, QualityResult
from provide.foundation.file.quality.operation_scenarios import OperationScenario


class QualityAnalyzer:
    """Analyzer for measuring file operation detection quality."""

    def __init__(self, detector: OperationDetector | None = None) -> None:
        """Initialize the quality analyzer.

        Args:
            detector: Operation detector to analyze. If None, creates default.
        """
        if not HAS_OPERATIONS_MODULE:
            raise ImportError("File operations module not available")

        self.detector = detector or OperationDetector()
        self.scenarios: list[OperationScenario] = []
        self.results: list[QualityResult] = []

    def add_scenario(self, scenario: OperationScenario) -> None:
        """Add a scenario for analysis.

        Args:
            scenario: Scenario to add
        """
        self.scenarios.append(scenario)

    def run_analysis(self, metrics: list[AnalysisMetric] | None = None) -> dict[AnalysisMetric, QualityResult]:
        """Run quality analysis on all scenarios.

        Args:
            metrics: Metrics to analyze. If None, runs all metrics.

        Returns:
            Dictionary mapping metrics to their results
        """
        if not self.scenarios:
            raise ValueError("No scenarios available for analysis")

        if metrics is None:
            metrics = list(AnalysisMetric)

        # Collect detection results and timing data
        detection_results, timing_results = self._collect_detection_data()

        # Calculate all requested metrics
        results = self._calculate_metrics(metrics, detection_results, timing_results)

        self.results.extend(results.values())
        return results

    def _collect_detection_data(self) -> tuple[list[dict[str, Any]], list[float]]:
        """Collect detection results and timing data from scenarios."""
        detection_results = []
        timing_results = []

        for scenario in self.scenarios:
            start_time = time.perf_counter()
            detected_operations = self.detector.detect(scenario.events)
            end_time = time.perf_counter()

            detection_time = (end_time - start_time) * 1000  # milliseconds
            timing_results.append(detection_time)

            detection_results.append(
                {
                    "scenario": scenario,
                    "detected": detected_operations,
                    "detection_time": detection_time,
                }
            )

        return detection_results, timing_results

    def _calculate_metrics(
        self,
        metrics: list[AnalysisMetric],
        detection_results: list[dict[str, Any]],
        timing_results: list[float],
    ) -> dict[AnalysisMetric, QualityResult]:
        """Calculate all requested metrics."""
        results: dict[AnalysisMetric, QualityResult] = {}

        for metric in metrics:
            if metric == AnalysisMetric.ACCURACY:
                results[metric] = self._calculate_accuracy(detection_results)
            elif metric == AnalysisMetric.PRECISION:
                results[metric] = self._calculate_precision(detection_results)
            elif metric == AnalysisMetric.RECALL:
                results[metric] = self._calculate_recall(detection_results)
            elif metric == AnalysisMetric.F1_SCORE:
                precision = self._calculate_precision(detection_results)
                recall = self._calculate_recall(detection_results)
                results[metric] = self._calculate_f1_score(precision.value, recall.value)
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
                results[metric] = self._analyze_confidence_distribution(detection_results)
            elif metric == AnalysisMetric.DETECTION_TIME:
                results[metric] = self._analyze_detection_time(timing_results)
            elif metric == AnalysisMetric.FALSE_POSITIVE_RATE:
                results[metric] = self._calculate_false_positive_rate(detection_results)
            elif metric == AnalysisMetric.FALSE_NEGATIVE_RATE:
                results[metric] = self._calculate_false_negative_rate(detection_results)

        return results

    def _calculate_accuracy(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Calculate overall accuracy."""
        correct_detections = 0
        total_detections = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # Simple accuracy: correct type detection
            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            # Count matches
            detected_counter = Counter(detected_types)
            expected_counter = Counter(expected_types)

            # Calculate overlap
            for op_type, expected_count in expected_counter.items():
                detected_count = detected_counter.get(op_type, 0)
                correct_detections += min(expected_count, detected_count)

            total_detections += max(len(detected_types), len(expected_types))

        accuracy = correct_detections / total_detections if total_detections > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.ACCURACY,
            value=accuracy,
            details={
                "correct_detections": correct_detections,
                "total_detections": total_detections,
                "percentage": accuracy * 100,
            },
        )

    def _calculate_precision(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Calculate precision (true positives / (true positives + false positives))."""
        true_positives = 0
        false_positives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            expected_counter = Counter(expected_types)

            for detected_type in detected_types:
                if expected_counter.get(detected_type, 0) > 0:
                    true_positives += 1
                    expected_counter[detected_type] -= 1
                else:
                    false_positives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.PRECISION,
            value=precision,
            details={
                "true_positives": true_positives,
                "false_positives": false_positives,
                "percentage": precision * 100,
            },
        )

    def _calculate_recall(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Calculate recall (true positives / (true positives + false negatives))."""
        true_positives = 0
        false_negatives = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            detected_types = [op.operation_type.value for op in detected]
            expected_types = [exp["type"] for exp in expected]

            detected_counter = Counter(detected_types)

            for expected_type in expected_types:
                if detected_counter.get(expected_type, 0) > 0:
                    true_positives += 1
                    detected_counter[expected_type] -= 1
                else:
                    false_negatives += 1

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0.0
        )

        return QualityResult(
            metric=AnalysisMetric.RECALL,
            value=recall,
            details={
                "true_positives": true_positives,
                "false_negatives": false_negatives,
                "percentage": recall * 100,
            },
        )

    def _calculate_f1_score(self, precision: float, recall: float) -> QualityResult:
        """Calculate F1 score (harmonic mean of precision and recall)."""
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.F1_SCORE,
            value=f1,
            details={
                "precision": precision,
                "recall": recall,
                "percentage": f1 * 100,
            },
        )

    def _analyze_confidence_distribution(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Analyze confidence score distribution."""
        confidences = []
        confidence_by_type = defaultdict(list)

        for result in detection_results:
            detected = result["detected"]

            for operation in detected:
                confidence = operation.confidence
                confidences.append(confidence)
                confidence_by_type[operation.operation_type.value].append(confidence)

        if not confidences:
            return QualityResult(
                metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
                value=0.0,
                details={"error": "No confidence scores available"},
            )

        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)

        # Calculate distribution stats by type
        type_stats = {}
        for op_type, type_confidences in confidence_by_type.items():
            type_stats[op_type] = {
                "count": len(type_confidences),
                "average": sum(type_confidences) / len(type_confidences),
                "min": min(type_confidences),
                "max": max(type_confidences),
            }

        return QualityResult(
            metric=AnalysisMetric.CONFIDENCE_DISTRIBUTION,
            value=avg_confidence,
            details={
                "total_operations": len(confidences),
                "average": avg_confidence,
                "min": min_confidence,
                "max": max_confidence,
                "by_type": type_stats,
            },
        )

    def _analyze_detection_time(self, timing_results: list[float]) -> QualityResult:
        """Analyze detection time performance."""
        if not timing_results:
            return QualityResult(
                metric=AnalysisMetric.DETECTION_TIME, value=0.0, details={"error": "No timing data available"}
            )

        avg_time = sum(timing_results) / len(timing_results)
        min_time = min(timing_results)
        max_time = max(timing_results)

        # Calculate percentiles
        sorted_times = sorted(timing_results)
        n = len(sorted_times)
        p50 = sorted_times[n // 2]
        p95 = sorted_times[int(n * 0.95)]
        p99 = sorted_times[int(n * 0.99)]

        return QualityResult(
            metric=AnalysisMetric.DETECTION_TIME,
            value=avg_time,
            details={
                "total_tests": len(timing_results),
                "average_ms": avg_time,
                "min_ms": min_time,
                "max_ms": max_time,
                "p50_ms": p50,
                "p95_ms": p95,
                "p99_ms": p99,
            },
        )

    def _calculate_false_positive_rate(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Calculate false positive rate."""
        false_positives = 0
        total_negative_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            # If no operations were expected but some were detected
            if not expected and detected:
                false_positives += len(detected)
                total_negative_cases += 1
            elif not expected:
                total_negative_cases += 1

        fpr = false_positives / total_negative_cases if total_negative_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_POSITIVE_RATE,
            value=fpr,
            details={
                "false_positives": false_positives,
                "total_negative_cases": total_negative_cases,
                "percentage": fpr * 100,
            },
        )

    def _calculate_false_negative_rate(self, detection_results: list[dict[str, Any]]) -> QualityResult:
        """Calculate false negative rate."""
        false_negatives = 0
        total_positive_cases = 0

        for result in detection_results:
            scenario = result["scenario"]
            detected = result["detected"]
            expected = scenario.expected_operations

            if expected:
                total_positive_cases += len(expected)
                detected_types = [op.operation_type.value for op in detected]
                expected_types = [exp["type"] for exp in expected]

                detected_counter = Counter(detected_types)

                for expected_type in expected_types:
                    if detected_counter.get(expected_type, 0) > 0:
                        detected_counter[expected_type] -= 1
                    else:
                        false_negatives += 1

        fnr = false_negatives / total_positive_cases if total_positive_cases > 0 else 0.0

        return QualityResult(
            metric=AnalysisMetric.FALSE_NEGATIVE_RATE,
            value=fnr,
            details={
                "false_negatives": false_negatives,
                "total_positive_cases": total_positive_cases,
                "percentage": fnr * 100,
            },
        )

    def generate_report(self, results: dict[AnalysisMetric, QualityResult] | None = None) -> str:
        """Generate a quality analysis report.

        Args:
            results: Results to include in report. If None, uses latest results.

        Returns:
            Formatted report string
        """
        if results is None:
            # Group latest results by metric
            latest_results = {}
            for result in reversed(self.results):
                if result.metric not in latest_results:
                    latest_results[result.metric] = result
            results = latest_results

        if not results:
            return "No analysis results available."

        report_lines = [
            "File Operation Detection Quality Report",
            "=" * 45,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Scenarios: {len(self.scenarios)}",
            "",
            "Metrics:",
        ]

        for metric, result in results.items():
            report_lines.append(f"  {metric.value.replace('_', ' ').title()}: {result.value:.3f}")

            # Add details for key metrics
            if metric == AnalysisMetric.ACCURACY and "percentage" in result.details:
                report_lines.append(f"    ({result.details['percentage']:.1f}%)")
            elif metric == AnalysisMetric.DETECTION_TIME and "average_ms" in result.details:
                report_lines.append(
                    f"    (avg: {result.details['average_ms']:.2f}ms, p95: {result.details.get('p95_ms', 0):.2f}ms)"
                )
            elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION and "by_type" in result.details:
                report_lines.append("    By operation type:")
                for op_type, stats in result.details["by_type"].items():
                    report_lines.append(f"      {op_type}: {stats['average']:.3f} (count: {stats['count']})")

        return "\n".join(report_lines)


# 🧱🏗️🔚
