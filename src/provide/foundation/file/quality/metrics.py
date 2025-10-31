#
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Metrics and result types for quality analysis."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from attrs import define, field


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


@define(slots=True, kw_only=True)
class QualityResult:
    """Result of quality analysis."""

    metric: AnalysisMetric
    value: float
    details: dict[str, Any] = field(factory=dict)
    timestamp: datetime = field(factory=datetime.now)


# 🧱🏗️🔚
