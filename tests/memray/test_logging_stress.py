#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pytest wrapper for logging memray stress test."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from tests.memray.conftest import assert_allocation_within_threshold, parse_total_allocations

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"

pytestmark = [pytest.mark.memray, pytest.mark.slow]


def test_logging_allocations(memray_output_dir, memray_baseline):
    """Run logging stress test under memray and check allocations against baseline."""
    script = SCRIPTS_DIR / "memray_logging_stress.py"
    output_file = memray_output_dir / "logging_stress.bin"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "memray",
            "run",
            "--output",
            str(output_file),
            "--force",
            str(script),
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert result.returncode == 0, f"Stress script failed:\n{result.stderr}"

    stats_result = subprocess.run(
        [sys.executable, "-m", "memray", "stats", str(output_file)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert stats_result.returncode == 0, f"memray stats failed:\n{stats_result.stderr}"

    total_allocs = parse_total_allocations(stats_result.stdout)
    assert total_allocs > 0, f"Could not parse allocations from memray stats:\n{stats_result.stdout}"

    assert_allocation_within_threshold("logging_total_allocations", total_allocs, memray_baseline)
