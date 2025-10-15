# provide/foundation/file/quality/__init__.py
#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""File operation quality analysis tools.

This package provides utilities to analyze and measure the quality,
accuracy, and performance of file operation detection algorithms.
"""

from __future__ import annotations

from provide.foundation.file.quality.analyzer import (
    AnalysisMetric,
    QualityAnalyzer,
    QualityResult,
)
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


# <3 🧱🤝📄🪄
