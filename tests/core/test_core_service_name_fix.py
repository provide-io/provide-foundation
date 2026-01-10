#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test to verify the service name injection fix works correctly."""

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
    from provide.testkit import reset_foundation_setup_for_testing

    reset_foundation_setup_for_testing()

    # Set environment like the failing test
    os.environ["PROVIDE_SERVICE_NAME"] = "lazy-service-test"
    os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
    os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "json"

    # Explicitly disable emoji settings for JSON output
    os.environ["PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"] = "false"
    os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "false"

    # Capture output
    import io

    from provide.testkit import set_log_stream_for_testing

    captured_output = io.StringIO()
    set_log_stream_for_testing(captured_output)

    try:
        # Force re-initialization with new environment variables
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.logger.config import TelemetryConfig

        hub = get_hub()
        config = TelemetryConfig.from_env()
        hub.initialize_foundation(config, force=True)

        # Test logging
        from provide.foundation import logger

        logger.info("Message with service name")

        # Get output
        output = captured_output.getvalue()
        print(f"Raw output: {output!r}")

        # Parse JSON
        # Filter to get only JSON lines (they start with '{')
        json_lines = [line.strip() for line in output.strip().splitlines() if line.strip().startswith("{")]

        if json_lines:
            log_data = json.loads(json_lines[0])
            print(f"Parsed JSON: {json.dumps(log_data, indent=2)}")

            # Check expectations
            expected_event = "Message with service name"
            actual_event = log_data.get("event", "")

            print(f"Expected event: {expected_event!r}")
            print(f"Actual event: {actual_event!r}")

            assert actual_event == expected_event, (
                f"Event message mismatch. Expected: '{expected_event}', Got: '{actual_event}'"
            )
            assert log_data.get("service_name") == "lazy-service-test", "Service name mismatch or missing"

        else:
            print("❌ No JSON log output found!")
            print(f"Full output: {output}")
            raise AssertionError("No JSON log output found")

    finally:
        set_log_stream_for_testing(None)
        # Clean up env vars used in this test
        os.environ.pop("PROVIDE_SERVICE_NAME", None)
        os.environ.pop("PROVIDE_LOG_CONSOLE_FORMATTER", None)


def test_key_value_still_has_emojis() -> None:
    """Test that key-value format still has emoji prefixes."""
    print("\n=== Testing Key-Value Format Still Has Emojis ===")

    # Reset state
    from provide.testkit import reset_foundation_setup_for_testing

    reset_foundation_setup_for_testing()

    # Set environment for key-value format
    os.environ.pop("PROVIDE_SERVICE_NAME", None)
    os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
    os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "key_value"

    # Enable emojis for key-value format (the test expects emojis)
    os.environ["PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"] = "true"
    os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "true"

    # Capture output
    import io

    from provide.testkit import set_log_stream_for_testing

    captured_output = io.StringIO()
    set_log_stream_for_testing(captured_output)

    try:
        # Force re-initialization with new environment variables
        from provide.foundation.hub.manager import get_hub
        from provide.foundation.logger.config import TelemetryConfig

        hub = get_hub()
        config = TelemetryConfig.from_env()
        hub.initialize_foundation(config, force=True)

        from provide.foundation import logger

        logger.info("Test message for key-value format")

        output = captured_output.getvalue()
        print(f"Key-value output: {output!r}")

        assert "🔹" in output, "Default emoji missing in key-value format"

    finally:
        set_log_stream_for_testing(None)
        # Clean up env vars used in this test
        os.environ.pop("PROVIDE_LOG_CONSOLE_FORMATTER", None)


# Removed __main__ block

# 🧱🏗️🔚
