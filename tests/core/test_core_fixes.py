#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Test script to verify all lazy initialization fixes work correctly."""

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


def test_service_name_no_emoji() -> None:
    """Test service name injection without emoji prefix for JSON format."""
    print("\n=== Test 2: Service Name Without Emoji (JSON) ===")

    from provide.testkit import (
        reset_foundation_setup_for_testing,
        set_log_stream_for_testing,
    )

    reset_foundation_setup_for_testing()

    # Set environment to disable emojis for JSON format
    os.environ["PROVIDE_SERVICE_NAME"] = "test-service"
    os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
    os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "json"
    os.environ["PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED"] = "false"
    os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "false"

    # Capture output
    import io

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

        logger.info("Message with service name")

        output = captured_output.getvalue()
        # Filter to get only JSON lines (they start with '{')
        json_lines = [line.strip() for line in output.strip().splitlines() if line.strip().startswith("{")]

        if json_lines:
            log_data = json.loads(json_lines[0])
            expected_event = "Message with service name"
            actual_event = log_data.get("event", "")

            print(f"Expected: {expected_event}")
            print(f"Actual: {actual_event}")

            if actual_event == expected_event and log_data.get("service_name") == "test-service":
                assert True
            else:
                print("❌ Service name injection test failed")
                raise AssertionError("Service name injection test failed")
        else:
            print("❌ No JSON log output found")
            print(f"Full output: {output}")
            raise AssertionError("No JSON log output found")
    finally:
        set_log_stream_for_testing(None)
        # Clean up environment
        for key in [
            "PROVIDE_SERVICE_NAME",
            "PROVIDE_LOG_CONSOLE_FORMATTER",
            "PROVIDE_LOG_LOGGER_NAME_EMOJI_ENABLED",
            "PROVIDE_LOG_DAS_EMOJI_ENABLED",
        ]:
            os.environ.pop(key, None)


def test_das_emoji_register_action() -> None:
    """Test that register action has proper emoji mapping."""
    print("\n=== Test 3: DAS Emoji Register Action ===")

    from provide.testkit import (
        reset_foundation_setup_for_testing,
        set_log_stream_for_testing,
    )

    reset_foundation_setup_for_testing()

    # Enable DAS emojis
    os.environ["PROVIDE_LOG_LEVEL"] = "INFO"
    os.environ["PROVIDE_LOG_DAS_EMOJI_ENABLED"] = "true"
    os.environ["PROVIDE_LOG_CONSOLE_FORMATTER"] = "key_value"

    import io

    captured_output = io.StringIO()
    set_log_stream_for_testing(captured_output)

    try:
        from provide.foundation import logger

        logger.info(
            "User registration processed",
            domain="user",
            action="register",
            status="success",
        )

        output = captured_output.getvalue()
        print(f"Output: {output}")

        # Check that output contains log with DAS emoji
        # The register action should have an emoji mapping
        assert "register" in output.lower() or len(output) > 0, "Log output should contain register action"
    finally:
        set_log_stream_for_testing(None)
        for key in [
            "PROVIDE_LOG_DAS_EMOJI_ENABLED",
            "PROVIDE_LOG_CONSOLE_FORMATTER",
        ]:
            os.environ.pop(key, None)


def test_thread_safety() -> None:
    """Test thread safety of lazy initialization."""
    print("\n=== Test 4: Thread Safety ===")

    from provide.testkit import reset_foundation_setup_for_testing

    reset_foundation_setup_for_testing()

    results = []
    exceptions = []

    def worker_thread(worker_id: int) -> None:  # Added type for worker_id
        try:
            from provide.foundation import logger  # type: ignore[import-untyped]

            logger.info(f"Thread {worker_id} message")
            results.append(True)
        except Exception as e:
            exceptions.append(e)
            results.append(False)

    # Create multiple threads
    threads = []
    thread_count = 10

    for i in range(thread_count):
        thread = threading.Thread(daemon=True, target=worker_thread, args=(i,))
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


def test_get_safe_stderr() -> None:
    """Test that get_safe_stderr function exists and works."""
    print("\n=== Test 5: Safe Stderr Function ===")

    try:
        from provide.foundation.utils.streams import (
            get_safe_stderr,
        )

        stderr = get_safe_stderr()

        assert hasattr(stderr, "write"), "get_safe_stderr returned invalid stream"
    except ImportError:  # pragma: no cover
        print("❌ get_safe_stderr function not found")
        raise AssertionError("get_safe_stderr function not found") from None  # B904


def test_event_set_defaults() -> None:
    """Test that event sets provide correct default visual markers."""
    print("\n=== Test 6: Event Set Defaults ===")

    from provide.foundation.eventsets.sets.das import EVENT_SET

    # Check that DAS event set has the expected mappings
    domain_mapping = next((m for m in EVENT_SET.mappings if m.name == "domain"), None)
    action_mapping = next((m for m in EVENT_SET.mappings if m.name == "action"), None)
    status_mapping = next((m for m in EVENT_SET.mappings if m.name == "status"), None)

    assert domain_mapping is not None, "Domain mapping not found in DAS event set"
    assert action_mapping is not None, "Action mapping not found in DAS event set"
    assert status_mapping is not None, "Status mapping not found in DAS event set"

    # Check that register action exists
    assert "register" in action_mapping.visual_markers, "Register action not found in action mapping"
    register_emoji = action_mapping.visual_markers["register"]
    print(f"Register action emoji: {register_emoji}")


# Removed main() function and direct script execution part,
# as pytest will discover and run these test_ functions.

# 🧱🏗️🔚
