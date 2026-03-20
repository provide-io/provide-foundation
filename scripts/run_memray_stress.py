#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Orchestrator: runs all memray stress scripts and prints analysis commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "memray-output"

STRESS_SCRIPTS = [
    ("logging", SCRIPTS_DIR / "memray_logging_stress.py"),
    ("serialization", SCRIPTS_DIR / "memray_serialization_stress.py"),
    ("config", SCRIPTS_DIR / "memray_config_stress.py"),
]


def run_stress_script(name: str, script_path: Path) -> Path:
    """Run a single stress script under memray."""
    output_file = OUTPUT_DIR / f"{name}_stress.bin"
    cmd = [
        sys.executable,
        "-m",
        "memray",
        "run",
        "--output",
        str(output_file),
        "--force",
        str(script_path),
    ]
    print(f"\n{'=' * 60}")
    print(f"Running: {name} stress test")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'=' * 60}")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"FAILED: {name} stress test exited with code {result.returncode}", file=sys.stderr)
        sys.exit(1)

    return output_file


def main() -> None:
    """Run all stress scripts and print analysis commands."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_files = []
    for name, script_path in STRESS_SCRIPTS:
        output_file = run_stress_script(name, script_path)
        output_files.append((name, output_file))

    print(f"\n{'=' * 60}")
    print("All stress tests completed successfully!")
    print(f"{'=' * 60}")
    print("\nAnalysis commands:")
    print("-" * 40)

    for name, output_file in output_files:
        print(f"\n# {name}")
        print(f"  uv run memray stats {output_file}")
        print(f"  uv run memray flamegraph {output_file} -o memray-output/{name}_flamegraph.html")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    main()
