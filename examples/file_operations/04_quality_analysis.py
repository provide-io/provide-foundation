#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Example: File Operation Quality Analysis

This example demonstrates how to use the quality analysis tools to measure
and evaluate the effectiveness of file operation detection algorithms."""

from __future__ import annotations

from pathlib import Path
import sys

# Add src to path for example
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from provide.foundation.file.quality import (
    AnalysisMetric,
    QualityAnalyzer,
    create_scenarios_from_patterns,
)


def main() -> None:
    """Demonstrate quality analysis functionality."""
    print("🔍 File Operation Quality Analysis Example")
    print("=" * 50)

    # Create a quality analyzer
    analyzer = QualityAnalyzer()

    # Add standard test cases for common patterns
    print("\n📋 Creating test cases for common patterns...")
    test_cases = create_scenarios_from_patterns()

    for test_case in test_cases:
        analyzer.add_scenario(test_case)
        print(f"  ✓ Added: {test_case.name} ({len(test_case.events)} events)")

    print(f"\nTotal test cases: {len(analyzer.scenarios)}")

    # Run comprehensive analysis
    metrics = [
        AnalysisMetric.ACCURACY,
        AnalysisMetric.PRECISION,
        AnalysisMetric.RECALL,
        AnalysisMetric.F1_SCORE,
        AnalysisMetric.CONFIDENCE_DISTRIBUTION,
        AnalysisMetric.DETECTION_TIME,
    ]

    results = analyzer.run_analysis(metrics)

    # Display results
    print("\n📊 Analysis Results:")
    print("-" * 30)

    for metric, result in results.items():
        print(f"\n{metric.value.replace('_', ' ').title()}:")
        print(f"  Value: {result.value:.4f}")

        # Show additional details for key metrics
        if metric == AnalysisMetric.ACCURACY:
            correct = result.details.get("correct_detections", 0)
            total = result.details.get("total_detections", 0)
            percentage = result.details.get("percentage", 0)
            print(f"  Details: {correct}/{total} correct ({percentage:.1f}%)")

        elif metric == AnalysisMetric.PRECISION:
            tp = result.details.get("true_positives", 0)
            fp = result.details.get("false_positives", 0)
            print(f"  Details: {tp} true positives, {fp} false positives")

        elif metric == AnalysisMetric.RECALL:
            tp = result.details.get("true_positives", 0)
            fn = result.details.get("false_negatives", 0)
            print(f"  Details: {tp} true positives, {fn} false negatives")

        elif metric == AnalysisMetric.DETECTION_TIME:
            avg_time = result.details.get("average_ms", 0)
            p95_time = result.details.get("p95_ms", 0)
            print(f"  Details: {avg_time:.2f}ms avg, {p95_time:.2f}ms p95")

        elif metric == AnalysisMetric.CONFIDENCE_DISTRIBUTION:
            total_ops = result.details.get("total_operations", 0)
            min_conf = result.details.get("min", 0)
            max_conf = result.details.get("max", 0)
            print(f"  Details: {total_ops} operations, range {min_conf:.3f}-{max_conf:.3f}")

    # Generate and display comprehensive report
    print("=" * 50)
    report = analyzer.generate_report(results)
    print(report)

    # Demonstrate custom test case creation
    print("\n🎯 Custom Test Case Example:")
    print("-" * 30)

    from datetime import datetime, timedelta

    from provide.foundation.file.operations import FileEvent, FileEventMetadata
    from provide.foundation.file.quality import OperationScenario

    # Create a custom test case for a specific scenario
    base_time = datetime.now()
    custom_events = [
        FileEvent(
            path=Path("custom_test.txt.tmp.custom"),
            event_type="created",
            metadata=FileEventMetadata(timestamp=base_time, sequence_number=1, size_after=512),
        ),
        FileEvent(
            path=Path("custom_test.txt.tmp.custom"),
            event_type="moved",
            metadata=FileEventMetadata(timestamp=base_time + timedelta(milliseconds=25), sequence_number=2),
            dest_path=Path("custom_test.txt"),
        ),
    ]

    custom_test_case = OperationScenario(
        name="custom_atomic_save",
        events=custom_events,
        expected_operations=[{"type": "atomic_save", "confidence_min": 0.85}],
        description="Custom atomic save test",
        tags=["custom", "atomic"],
    )

    # Test the custom case
    custom_analyzer = QualityAnalyzer()
    custom_analyzer.add_scenario(custom_test_case)

    custom_results = custom_analyzer.run_analysis([AnalysisMetric.ACCURACY])
    accuracy = custom_results[AnalysisMetric.ACCURACY]

    print(f"Custom test accuracy: {accuracy.value:.3f}")
    print(f"Details: {accuracy.details}")

    print("\n✨ Quality analysis complete!")
    print("💡 Tip: Use these metrics to tune detector parameters and improve accuracy.")


if __name__ == "__main__":
    main()

# 🧱🏗️🔚
