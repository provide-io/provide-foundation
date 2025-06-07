#
# test_verification.py
#
"""
Quick verification script to test the lazy initialization fixes.
"""
import os
from pathlib import Path
import sys

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

def test_basic_lazy_init() -> None:
    """Test basic lazy initialization works."""
    print("=== Test 1: Basic Lazy Initialization ===")

    # Reset any existing configuration
    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Clear environment
    env_vars_to_clear = [
        "PYVIDER_SERVICE_NAME", "PYVIDER_LOG_CONSOLE_FORMATTER",
        "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "PYVIDER_LOG_DAS_EMOJI_ENABLED"
    ]
    for var in env_vars_to_clear:
        os.environ.pop(var, None)

    from pyvider.telemetry import logger
    logger.info("Basic lazy initialization test")
    print("✅ Basic lazy initialization works")


def test_service_name_injection() -> None:
    """Test service name injection with JSON format."""
    print("\n=== Test 2: Service Name Injection (JSON) ===")

    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Set environment like the failing test
    os.environ["PYVIDER_SERVICE_NAME"] = "test-service"
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = "json"

    from pyvider.telemetry import logger
    logger.info("Message with service name")
    print("✅ Service name injection test works")


def test_lazy_setup_flags() -> None:
    """Test that lazy setup flags are set correctly."""
    print("\n=== Test 3: Lazy Setup Flags ===")

    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    from pyvider.telemetry.logger.base import _LAZY_SETUP_STATE  # Changed
    print(f"Initial state - _LAZY_SETUP_STATE: {_LAZY_SETUP_STATE}")

    from pyvider.telemetry import logger
    logger.info("Trigger lazy setup")

    # _LAZY_SETUP_STATE is a mutable dict, check its current content
    print(f"After logging - _LAZY_SETUP_STATE: {_LAZY_SETUP_STATE}")

    assert _LAZY_SETUP_STATE["done"] is True, "Lazy setup 'done' flag should be True"
    assert _LAZY_SETUP_STATE["error"] is None, "Lazy setup 'error' flag should be None"
    print("✅ Lazy setup flags work correctly")


def test_emergency_fallback() -> None:
    """Test emergency fallback doesn't crash."""
    print("\n=== Test 4: Emergency Fallback ===")

    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    from pyvider.telemetry.logger.base import PyviderLogger
    test_logger = PyviderLogger()

    # Trigger emergency fallback by setting error state
    from pyvider.telemetry.logger.base import (
        _LAZY_SETUP_STATE,  # Ensure we use the state dict
    )
    _LAZY_SETUP_STATE["error"] = Exception("Test error") # Set error state
    _LAZY_SETUP_STATE["done"] = False # Ensure done is false so error path is taken

    try:
        test_logger.info("Emergency fallback test")
        print("✅ Emergency fallback works (no crash)")
        # Further assertions could be made if _setup_emergency_fallback was mocked
        # or if there was discernible output from emergency logger.
        # For now, just ensuring it doesn't crash is the main goal of this test.
    except Exception as e: # pragma: no cover
        print(f"❌ Emergency fallback failed: {e}")
        raise AssertionError(f"Emergency fallback test failed: {e}") from e # B904
    finally:
        # Clean up state
        reset_pyvider_setup_for_testing()

# Removed __main__ block

# 🧪✅
