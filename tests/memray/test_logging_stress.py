#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Pytest wrapper for logging memray stress test."""

from __future__ import annotations

from pathlib import Path

import pytest
from wrknv.memray.runner import run_memray_stress

SCRIPTS_DIR = Path(__file__).parent.parent.parent / "scripts"

pytestmark = [pytest.mark.memray, pytest.mark.slow]


def test_logging_allocations(memray_output_dir, memray_baseline, memray_baselines_path):
    """Run logging stress test under memray and check allocations against baseline."""
    run_memray_stress(
        script=SCRIPTS_DIR / "memray_logging_stress.py",
        baseline_key="logging_total_allocations",
        output_dir=memray_output_dir,
        baselines=memray_baseline,
        baselines_path=memray_baselines_path,
    )
