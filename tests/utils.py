"""Shared test utilities to reduce code duplication across test files."""

import os
from pathlib import Path
from typing import Any

from provide.foundation.testing import reset_foundation_setup_for_testing


class TestEnvironment:
    """Context manager for test environment setup with proper cleanup."""

    def __init__(self, env_vars: dict[str, str] | None = None):
        self.env_vars = env_vars or {}
        self.original_env: dict[str, str | None] = {}

    def __enter__(self) -> "TestEnvironment":
        # Save original environment variables
        for key in self.env_vars:
            self.original_env[key] = os.environ.get(key)
            os.environ[key] = self.env_vars[key]

        # Reset foundation setup
        reset_foundation_setup_for_testing()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        # Restore original environment variables
        for key, original_value in self.original_env.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value

        # Reset foundation setup again for cleanup
        reset_foundation_setup_for_testing()


def get_example_dir() -> Path:
    """Get the examples directory path consistently across examples."""
    return Path(__file__).resolve().parent.parent / "examples"


def add_src_to_path() -> Path:
    """Add src directory to Python path for examples. Returns project root path."""
    import sys

    example_dir = get_example_dir()
    project_root = example_dir.parent
    src_path = project_root / "src"

    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    return project_root


def reset_test_environment() -> None:
    """Reset the test environment to a clean state."""
    reset_foundation_setup_for_testing()
