#
# test_fixes.py
#
"""
Test script to verify all lazy initialization fixes work correctly.
"""
import json
import os
from pathlib import Path
import sys
import threading

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))


def test_lazy_setup_flags() -> None:
    """Test that lazy setup flags are set correctly."""
    print("=== Test 1: Lazy Setup Flags ===")

    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Use the new _LAZY_SETUP_STATE dictionary
    from pyvider.telemetry.logger.base import _LAZY_SETUP_STATE
    print(f"Initial state - STATE: {_LAZY_SETUP_STATE}")

    from pyvider.telemetry import logger
    logger.info("Trigger lazy setup")

    # Re-check the same _LAZY_SETUP_STATE dictionary
    print(f"After logging - STATE: {_LAZY_SETUP_STATE}")

    assert _LAZY_SETUP_STATE["done"] is True, "Flag 'done' should be True"
    assert _LAZY_SETUP_STATE["error"] is None, "Flag 'error' should be None"
    assert _LAZY_SETUP_STATE["in_progress"] is False, "Flag 'in_progress' should be False"
    print("✅ Lazy setup flags work correctly")


def test_service_name_no_emoji() -> None:
    """Test service name injection without emoji prefix for JSON format."""
    print("\n=== Test 2: Service Name Without Emoji (JSON) ===")

    from pyvider.telemetry.core import (
        _set_log_stream_for_testing,
        reset_pyvider_setup_for_testing,
    )
    reset_pyvider_setup_for_testing()

    # Set environment to disable emojis for JSON format
    os.environ["PYVIDER_SERVICE_NAME"] = "test-service"
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = "json"
    os.environ["PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED"] = "false"
    os.environ["PYVIDER_LOG_DAS_EMOJI_ENABLED"] = "false"

    # Capture output
    import io
    captured_output = io.StringIO()
    _set_log_stream_for_testing(captured_output)

    try:
        from pyvider.telemetry import logger
        logger.info("Message with service name")

        output = captured_output.getvalue()
        lines = [line for line in output.strip().splitlines() if line.strip() and not line.startswith("[")]

        if lines:
            log_data = json.loads(lines[0])
            expected_event = "Message with service name"
            actual_event = log_data.get("event", "")

            print(f"Expected: {expected_event}")
            print(f"Actual: {actual_event}")

            if actual_event == expected_event and log_data.get("service_name") == "test-service":
                print("✅ Service name injection without emoji works")
                assert True
            else:
                print("❌ Service name injection test failed")
                raise AssertionError("Service name injection test failed")
        else:
            print("❌ No log output found")
            raise AssertionError("No log output found")
    finally:
        _set_log_stream_for_testing(None)
        # Clean up environment
        for key in ["PYVIDER_SERVICE_NAME", "PYVIDER_LOG_CONSOLE_FORMATTER",
                   "PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "PYVIDER_LOG_DAS_EMOJI_ENABLED"]:
            os.environ.pop(key, None)


def test_das_emoji_register_action() -> None:
    """Test that register action has proper emoji mapping."""
    print("\n=== Test 3: DAS Emoji Register Action ===")

    from pyvider.telemetry.core import (
        _set_log_stream_for_testing,
        reset_pyvider_setup_for_testing,
    )
    reset_pyvider_setup_for_testing()

    # Enable DAS emojis
    os.environ["PYVIDER_LOG_DAS_EMOJI_ENABLED"] = "true"
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = "key_value"

    import io
    captured_output = io.StringIO()
    _set_log_stream_for_testing(captured_output)

    try:
        from pyvider.telemetry import logger
        logger.info(
            "User registration processed",
            domain="user",
            action="register",
            status="success"
        )

        output = captured_output.getvalue()
        print(f"Output: {output}")

        # Should contain [👤][⚙️][✅] - user, register (⚙️), success
        if "[👤][⚙️][✅]" in output: # User '👤', Register '⚙️', Success '✅'
            print("✅ DAS emoji register action works")
            assert True
        else:
            print("❌ DAS emoji register action failed")
            print("Expected [👤][⚙️][✅] in output") # Note: This relies on SECONDARY_EMOJI default being ⚙️. If it's ❓, this test needs to change.
                                                  # Based on previous changes, SECONDARY_EMOJI default is now '❓'.
                                                  # So, if "register" is not in the map, it should be [👤][❓][✅].
                                                  # The map currently has "register": "⚙️", so this is correct.
            raise AssertionError("DAS emoji for register action is incorrect.")
    finally:
        _set_log_stream_for_testing(None)
        for key in ["PYVIDER_LOG_DAS_EMOJI_ENABLED", "PYVIDER_LOG_CONSOLE_FORMATTER"]:
            os.environ.pop(key, None)


def test_thread_safety() -> None:
    """Test thread safety of lazy initialization."""
    print("\n=== Test 4: Thread Safety ===")

    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    results = []
    exceptions = []

    def worker_thread(worker_id: int) -> None: # Added type for worker_id
        try:
            from pyvider.telemetry import logger  # type: ignore[import-untyped]
            logger.info(f"Thread {worker_id} message")
            results.append(True)
        except Exception as e:
            exceptions.append(e)
            results.append(False)

    # Create multiple threads
    threads = []
    thread_count = 10

    for i in range(thread_count):
        thread = threading.Thread(target=worker_thread, args=(i,))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for completion
    for thread in threads:
        thread.join(timeout=5.0)

    assert len(exceptions) == 0, f"Thread safety test encountered exceptions: {exceptions}"
    assert len(results) == thread_count, "Not all threads completed in thread safety test"
    assert all(results), "Some threads failed in thread safety test"
    print("✅ Thread safety test passed")


def test_get_safe_stderr() -> None:
    """Test that _get_safe_stderr function exists and works."""
    print("\n=== Test 5: Safe Stderr Function ===")

    try:
        from pyvider.telemetry.logger.base import (
            _get_safe_stderr,  # type: ignore[import-untyped]
        )
        stderr = _get_safe_stderr()

        assert hasattr(stderr, 'write'), "_get_safe_stderr returned invalid stream"
        print("✅ _get_safe_stderr function works")
    except ImportError: # pragma: no cover
        print("❌ _get_safe_stderr function not found")
        raise AssertionError("_get_safe_stderr function not found") from None # B904


def test_emoji_matrix_defaults() -> None:
    """Test emoji matrix has correct default mappings."""
    print("\n=== Test 6: Emoji Matrix Defaults ===")

    from pyvider.telemetry.logger.emoji_matrix import (
        PRIMARY_EMOJI,
        SECONDARY_EMOJI,
        TERTIARY_EMOJI,
    )

    # Check that register action exists
    if "register" in SECONDARY_EMOJI:
        register_emoji = SECONDARY_EMOJI["register"]
        print(f"Register action emoji: {register_emoji}")

        # Check default emojis match test expectations
        expected_defaults = {
            "domain_default": PRIMARY_EMOJI.get("default", "❓"), # Default should be ❓
            "action_default": SECONDARY_EMOJI.get("default", "❓"), # Default is now ❓
            "status_default": TERTIARY_EMOJI.get("default", "➡️")  # Default is ➡️
        }

        print(f"Default emojis: {expected_defaults}")

        assert PRIMARY_EMOJI.get("default") == "❓", "Primary default emoji mismatch"
        assert SECONDARY_EMOJI.get("default") == "❓", "Secondary default emoji mismatch - should be ❓"
        assert TERTIARY_EMOJI.get("default") == "➡️", "Tertiary default emoji mismatch"
        print("✅ Emoji matrix defaults are correct")
    else: # pragma: no cover
        print("❌ Register action not found in emoji matrix")
        raise AssertionError("Register action not found in emoji matrix")

# Removed main() function and direct script execution part,
# as pytest will discover and run these test_ functions.

# 🧪✅
