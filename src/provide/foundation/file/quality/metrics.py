"""Metrics and result types for quality analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class AnalysisMetric(Enum):
    """Metrics for quality analysis."""

    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1_SCORE = "f1_score"
    CONFIDENCE_DISTRIBUTION = "confidence_distribution"
    DETECTION_TIME = "detection_time"
    FALSE_POSITIVE_RATE = "false_positive_rate"
    FALSE_NEGATIVE_RATE = "false_negative_rate"


@dataclass
class QualityResult:
    """Result of quality analysis."""

    metric: AnalysisMetric
    value: float
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
