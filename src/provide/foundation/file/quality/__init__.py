"""Quality analysis tools for file operation detection.

This package provides utilities to analyze and measure the quality,
accuracy, and performance of file operation detection algorithms.
"""

from __future__ import annotations

from provide.foundation.file.quality.analyzer import QualityAnalyzer
from provide.foundation.file.quality.metrics import AnalysisMetric, QualityResult
from provide.foundation.file.quality.operation_scenarios import (
    OperationScenario,
    create_scenarios_from_patterns,
)

__all__ = [
    "AnalysisMetric",
    "OperationScenario",
    "QualityAnalyzer",
    "QualityResult",
    "create_scenarios_from_patterns",
]
