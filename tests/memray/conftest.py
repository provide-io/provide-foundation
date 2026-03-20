#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Fixtures and helpers for memray memory profiling tests."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

BASELINES_PATH = Path(__file__).parent / "baselines.json"
PROJECT_ROOT = Path(__file__).parent.parent.parent
MEMRAY_OUTPUT_DIR = PROJECT_ROOT / "memray-output"

# Tolerance for allocation regression checks (15%)
ALLOCATION_THRESHOLD = 0.15


@pytest.fixture
def memray_output_dir() -> Path:
    """Return the memray output directory, creating it if needed."""
    MEMRAY_OUTPUT_DIR.mkdir(exist_ok=True)
    return MEMRAY_OUTPUT_DIR


@pytest.fixture
def memray_baseline() -> dict:
    """Load the current baselines from baselines.json."""
    if BASELINES_PATH.exists():
        return json.loads(BASELINES_PATH.read_text())
    return {}


def _update_baseline(key: str, value: int) -> None:
    """Update a single baseline value in baselines.json."""
    baselines = {}
    if BASELINES_PATH.exists():
        baselines = json.loads(BASELINES_PATH.read_text())
    baselines[key] = value
    BASELINES_PATH.write_text(json.dumps(baselines, indent=2, sort_keys=True) + "\n")


def assert_allocation_within_threshold(
    baseline_key: str,
    measured_allocations: int,
    baselines: dict,
) -> None:
    """Assert that measured allocations are within threshold of baseline.

    On first run (no baseline exists), records the baseline.
    If MEMRAY_UPDATE_BASELINE=1 is set, updates the baseline.

    Args:
        baseline_key: Key to look up/store in baselines.json
        measured_allocations: Current allocation count
        baselines: Current baselines dict

    """
    should_update = os.environ.get("MEMRAY_UPDATE_BASELINE") == "1"

    if should_update or baseline_key not in baselines:
        _update_baseline(baseline_key, measured_allocations)
        if baseline_key not in baselines:
            pytest.skip(f"First run — recorded baseline for {baseline_key}: {measured_allocations}")
        return

    expected = baselines[baseline_key]
    max_allowed = int(expected * (1 + ALLOCATION_THRESHOLD))

    assert measured_allocations <= max_allowed, (
        f"Allocation regression for {baseline_key}: "
        f"measured {measured_allocations:,} > allowed {max_allowed:,} "
        f"(baseline {expected:,} + {ALLOCATION_THRESHOLD:.0%} threshold)"
    )


def parse_total_allocations(stats_output: str) -> int:
    """Extract total allocation count from memray stats output.

    Memray stats format uses label on one line, value on the next:
        Total allocations:
            3878431
    """
    lines = stats_output.splitlines()
    for i, line in enumerate(lines):
        if "total allocations" in line.lower() and i + 1 < len(lines):
            match = re.search(r"(\d[\d,]*)", lines[i + 1])
            if match:
                return int(match.group(1).replace(",", ""))
    return 0
