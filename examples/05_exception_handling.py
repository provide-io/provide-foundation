#!/usr/bin/env python3
# examples/pyvider_telemetry/05_exception_handling.py
"""Demonstrates exception logging with automatic traceback inclusion."""

from pathlib import Path
import sys

# Add src to path for examples
example_dir = Path(__file__).resolve().parent.parent  # Go up one level to `examples`
project_root = example_dir.parent
src_path = project_root / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from typing import Never  # noqa: E402

from pyvider.telemetry import logger, setup_telemetry  # noqa: E402


def example_5_exception_handling() -> None:
    """
    Example 5: Demonstrates logging exceptions with tracebacks.

    The `logger.exception()` method automatically captures and logs the current
    exception's traceback information along with the error message.
    """
    print("\n" + "=" * 60)
    print("💥 Example 5: Exception Handling")
    print(" Demonstrates: Using logger.exception() to log errors with tracebacks.")
    print("=" * 60)

    setup_telemetry()  # Default configuration

    def risky_operation() -> Never:
        """A function that is expected to raise an exception."""
        sub_operation_data = {"sub_key": "sub_value"}
        raise ValueError(
            f"Something went wrong in the operation with data: {sub_operation_data}"
        )

    def another_risky_operation() -> Never:
        """Another function that raises a different exception."""
        raise ConnectionError("Failed to connect to external service 'alpha'.")

    # Exception logging with full traceback
    try:
        risky_operation()
    except Exception:  # Catches ValueError
        logger.exception(
            "Operation failed unexpectedly",
            operation_name="risky_operation",
            user_id="user_xyz",
        )

    try:
        another_risky_operation()
    except Exception:  # Catches ConnectionError
        logger.exception(
            "Connection error occurred while contacting external API",
            domain="network",
            action="connect",
            status="error",
            target_service="external_api_alpha",
        )


if __name__ == "__main__":
    example_5_exception_handling()
    print("\n✅ Example 5 completed.")
