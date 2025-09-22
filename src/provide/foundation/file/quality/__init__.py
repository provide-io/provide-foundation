"""Quality analysis tools for file operation detection.

This package provides utilities to analyze and measure the quality,
accuracy, and performance of file operation detection algorithms.
"""

from __future__ import annotations

from provide.foundation.file.quality.analyzer import QualityAnalyzer
from provide.foundation.file.quality.metrics import AnalysisMetric, QualityResult
from provide.foundation.file.quality.test_cases import OperationTestCase, create_test_cases_from_patterns

__all__ = [
    "AnalysisMetric",
    "OperationTestCase",
    "QualityAnalyzer",
    "QualityResult",
    "create_test_cases_from_patterns",
]
