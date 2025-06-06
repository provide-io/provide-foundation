#
# test_service_name_fix.py
#
"""
Test to verify the service name injection fix works correctly.
"""
import json
import os
from pathlib import Path
import sys

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

def test_service_name_injection_fix() -> None:
    """Test that service name injection works with JSON format and no emoji prefix."""
    print("=== Testing Service Name Injection Fix ===")

    # Reset state
    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Set environment like the failing test
    os.environ["PYVIDER_SERVICE_NAME"] = "lazy-service-test"
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = "json"

    # Clear any existing emoji settings
    for key in ["PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "PYVIDER_LOG_DAS_EMOJI_ENABLED"]:
        os.environ.pop(key, None)

    # Capture output
    import io

    from pyvider.telemetry.core import _set_log_stream_for_testing
    captured_output = io.StringIO()
    _set_log_stream_for_testing(captured_output)

    try:
        # Test logging
        from pyvider.telemetry import logger
        logger.info("Message with service name")

        # Get output
        output = captured_output.getvalue()
        print(f"Raw output: {output!r}")

        # Parse JSON
        lines = [line for line in output.strip().splitlines()
                if line.strip() and not line.startswith("[")]

        if lines:
            log_data = json.loads(lines[0])
            print(f"Parsed JSON: {json.dumps(log_data, indent=2)}")

            # Check expectations
            expected_event = "Message with service name"
            actual_event = log_data.get("event", "")

            print(f"Expected event: {expected_event!r}")
            print(f"Actual event: {actual_event!r}")

            assert actual_event == expected_event, f"Event message mismatch. Expected: '{expected_event}', Got: '{actual_event}'"
            assert log_data.get("service_name") == "lazy-service-test", "Service name mismatch or missing"
            print("✅ Service name injection test PASSED!")

        else:
            print("❌ No log output found!")
            raise AssertionError("No log output found")

    finally:
        _set_log_stream_for_testing(None)
        # Clean up env vars used in this test
        os.environ.pop("PYVIDER_SERVICE_NAME", None)
        os.environ.pop("PYVIDER_LOG_CONSOLE_FORMATTER", None)

def test_key_value_still_has_emojis() -> None:
    """Test that key-value format still has emoji prefixes."""
    print("\n=== Testing Key-Value Format Still Has Emojis ===")

    # Reset state
    from pyvider.telemetry.core import reset_pyvider_setup_for_testing
    reset_pyvider_setup_for_testing()

    # Set environment for key-value format
    os.environ.pop("PYVIDER_SERVICE_NAME", None)
    os.environ["PYVIDER_LOG_CONSOLE_FORMATTER"] = "key_value"

    # Clear any existing emoji settings
    for key in ["PYVIDER_LOG_LOGGER_NAME_EMOJI_ENABLED", "PYVIDER_LOG_DAS_EMOJI_ENABLED"]:
        os.environ.pop(key, None)

    # Capture output
    import io

    from pyvider.telemetry.core import _set_log_stream_for_testing
    captured_output = io.StringIO()
    _set_log_stream_for_testing(captured_output)

    try:
        from pyvider.telemetry import logger
        logger.info("Test message for key-value format")

        output = captured_output.getvalue()
        print(f"Key-value output: {output!r}")

        assert "🗣️" in output, "Default emoji missing in key-value format"
        print("✅ Key-value format still has emojis!")

    finally:
        _set_log_stream_for_testing(None)
        # Clean up env vars used in this test
        os.environ.pop("PYVIDER_LOG_CONSOLE_FORMATTER", None)

# Removed __main__ block

# 🧪✅
