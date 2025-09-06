"""Shared utilities for Foundation Telemetry examples."""

import sys
from pathlib import Path


def setup_example_environment() -> Path:
    """
    Set up the example environment by adding src to path.
    
    Returns:
        Path to the project root directory.
    """
    # Get paths relative to this utils.py file
    examples_dir = Path(__file__).resolve().parent
    project_root = examples_dir.parent
    src_path = project_root / "src"
    
    # Add src to path if it exists and isn't already there
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    return project_root


def print_example_header(example_num: int, title: str, description: str) -> None:
    """Print a standardized example header."""
    print(f"\n{'=' * 60}")
    print(f"🔢 Example {example_num}: {title}")
    print(f" Demonstrates: {description}")
    print("=" * 60)


def print_example_completion(example_num: int) -> None:
    """Print a standardized example completion message."""
    print(f"\n✅ Example {example_num} completed.")