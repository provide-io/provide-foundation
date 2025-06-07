#
# test_lazy_setup_flag.py
#
"""
Test to verify the lazy setup done flag is set correctly.
"""
from pathlib import Path
import sys
from typing import Any  # For F821

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

def test_lazy_setup_done_flag() -> None:
    """Test that the lazy setup done flag is set correctly."""
    print("=== Testing Lazy Setup Done Flag ===")

    # Reset state
    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Check initial state
    from pyvider.telemetry.logger.base import _LAZY_SETUP_STATE  # Changed
    print("Initial state:")
    print(f"  _LAZY_SETUP_STATE: {_LAZY_SETUP_STATE}")

    # Trigger lazy setup
    from pyvider.telemetry import logger
    print("\nLogging message to trigger lazy setup...")
    logger.info("Test message to trigger lazy setup")

    # Check state after logging
    # _LAZY_SETUP_STATE is the same dict, its content would have changed
    print("After logging:")
    print(f"  _LAZY_SETUP_STATE: {_LAZY_SETUP_STATE}")

    # Verify expected state
    assert _LAZY_SETUP_STATE["done"] is True, "Flag 'done' should be True"
    assert _LAZY_SETUP_STATE["error"] is None, "Flag 'error' should be None"
    assert _LAZY_SETUP_STATE["in_progress"] is False, "Flag 'in_progress' should be False"
    print("✅ Lazy setup flags are correct!")

def test_recursive_logging_protection() -> None:
    """Test that recursive logging doesn't cause infinite loops."""
    print("\n=== Testing Recursive Logging Protection ===")

    # Reset state
    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Create a custom setup function that logs during setup
    def recursive_setup(self: Any) -> None: # Added type for self
        print("In recursive setup - this should trigger emergency fallback")
        from pyvider.telemetry import (
            logger as global_logger,  # type: ignore[import-untyped]
        )
        global_logger.debug("Logging during setup - should use emergency fallback")
        # Don't call the original setup to avoid actual recursion
        return

    # Patch the setup method
    from unittest.mock import patch

    from pyvider.telemetry.logger.base import (
        PyviderLogger,  # type: ignore[import-untyped]
    )

    with patch.object(PyviderLogger, '_perform_lazy_setup', recursive_setup): # type: ignore[assignment]
        from pyvider.telemetry import logger  # type: ignore[import-untyped]
        print("Triggering recursive logging scenario...")

        try:
            logger.info("This should trigger recursive setup scenario")
            print("✅ Recursive logging handled without infinite loop!")
            # No specific assertion needed if it completes without error
        except Exception as e: # pragma: no cover
            print(f"❌ Recursive logging failed: {e}")
            raise AssertionError(f"Recursive logging failed: {e}") from e # B904

# Removed __main__ block, pytest will run tests

# 🧪🔄
