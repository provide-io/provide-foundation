#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Core integration tests for the Foundation library."""

from __future__ import annotations

from collections.abc import Callable
import io
import os

from provide.testkit import TestEnvironment, isolated_cli_runner
from provide.testkit.mocking import patch
import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger,
)
from provide.foundation.errors import FoundationError
from provide.foundation.hub import register_command
from provide.foundation.hub.registry import Registry


def setup_json_logging(setup_func: Callable[[TelemetryConfig | None], None]) -> None:
    """Use JSON formatter at DEBUG level for deterministic test output."""
    config = TelemetryConfig(
        logging=LoggingConfig(console_formatter="json", default_level="DEBUG"),
    )
    setup_func(config)


# Mark all tests in this file to run serially to avoid global state pollution
pytestmark = pytest.mark.serial


# Foundation state is automatically managed by FoundationTestCase base class


def test_basic_initialization_and_logging(captured_stderr_for_foundation: io.StringIO) -> None:
    """Test basic initialization and logging."""
    import json

    logger.info("Test message", key="value")
    log_output = captured_stderr_for_foundation.getvalue()

    # The output should contain our test message
    assert "Test message" in log_output

    # Parse JSON output to verify key-value pairs
    # Find the JSON line containing our test message
    json_line = None
    for line in log_output.strip().split("\n"):
        if line.strip() and "Test message" in line and line.startswith("{"):
            json_line = line.strip()
            break

    if json_line:
        # JSON format - parse and verify fields
        log_record = json.loads(json_line)
        assert "Test message" in log_record["event"]
        assert log_record["key"] == "value"
    else:
        # Fallback to key=value format check for backwards compatibility
        assert "key=value" in log_output


def test_hub_and_registry_integration() -> None:
    """Test Hub and Registry integration."""
    hub = get_hub()
    assert hub is not None
    assert isinstance(hub._command_registry, Registry)

    hub._command_registry.register("test_cmd", lambda: "success")
    cmd = hub._command_registry.get("test_cmd")
    assert cmd() == "success"


def test_cli_integration() -> None:
    """Test CLI integration."""
    with isolated_cli_runner() as runner:
        hub = get_hub()

        @register_command("test-cli")
        def test_cli_cmd() -> None:
            """A test CLI command."""
            print("CLI command executed")

        cli = hub.create_cli()
        result = runner.invoke(cli, ["test-cli"])
    assert result.exit_code == 0
    assert "CLI command executed" in result.output


def test_configuration_from_environment(captured_stderr_for_foundation: io.StringIO) -> None:
    """Test configuration loading from environment variables."""
    with TestEnvironment(
        {
            "PROVIDE_SERVICE_NAME": "test-service",
            "PROVIDE_LOG_LEVEL": "DEBUG",
        }
    ):
        hub = get_hub()
        assert hub.get_foundation_config().service_name == "test-service"

        logger.debug("Debug message should be visible")
        log_output = captured_stderr_for_foundation.getvalue()
        assert "Debug message should be visible" in log_output


def test_explicit_configuration_override(captured_stderr_for_foundation: io.StringIO) -> None:
    """Test explicit configuration overrides environment variables."""
    with TestEnvironment({"PROVIDE_SERVICE_NAME": "env-service"}):
        config = TelemetryConfig(
            service_name="explicit-service",
            logging=LoggingConfig(default_level="WARNING"),
        )
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        assert hub.get_foundation_config().service_name == "explicit-service"

        logger.info("Info message should be hidden")
        logger.warning("Warning message should be visible")
        log_output = captured_stderr_for_foundation.getvalue()

        assert "Info message should be hidden" not in log_output
        assert "Warning message should be visible" in log_output


def test_error_handling_integration(captured_stderr_for_foundation: io.StringIO) -> None:
    """Test error handling integration."""
    with pytest.raises(FoundationError, match="Test error"):
        raise FoundationError("Test error", code="TEST_001")

    try:
        raise FoundationError("Another test error")
    except FoundationError:
        logger.exception("Caught expected error")

    log_output = captured_stderr_for_foundation.getvalue()
    assert "Caught expected error" in log_output
    assert "FoundationError: Another test error" in log_output


def test_component_loading_and_usage() -> None:
    """Test component loading and usage."""
    hub = get_hub()

    class TestComponent:
        def __init__(self) -> None:
            self.value = "test"

    hub.add_component(TestComponent, name="test_component")
    component_class = hub.get_component("test_component")
    assert component_class == TestComponent
    component = component_class()
    assert component.value == "test"


def test_foundation_testbed_integration(captured_stderr_for_foundation: io.StringIO) -> None:
    """Test integration with test environment utilities."""
    with TestEnvironment({"PROVIDE_SERVICE_NAME": "testbed-service"}):
        hub = get_hub()
        hub.initialize_foundation(
            TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")),
            force=True,
        )
        assert hub.get_foundation_config().service_name == "testbed-service"

        logger.debug("Testbed debug message")
        assert "Testbed debug message" in captured_stderr_for_foundation.getvalue()


def test_context_propagation_in_logs(
    captured_stderr_for_foundation: io.StringIO,
    setup_foundation_telemetry_for_test: Callable[[TelemetryConfig | None], None],
) -> None:
    """Test context propagation in logs."""
    setup_json_logging(setup_foundation_telemetry_for_test)
    bound_logger = logger.bind(request_id="req-123")
    bound_logger.info("Processing request")

    log_output = captured_stderr_for_foundation.getvalue()
    assert log_output, "Expected log output to be emitted"
    # Check for request_id in both key-value and JSON formats
    assert "request_id=req-123" in log_output or '"request_id": "req-123"' in log_output, (
        f"request_id not found in output: {log_output}"
    )


def test_configuration_edge_cases() -> None:
    """Test configuration edge cases."""
    # Test that re-initialization without force does nothing
    with TestEnvironment({"PROVIDE_SERVICE_NAME": "first-service"}):
        hub = get_hub()
        assert hub.get_foundation_config().service_name == "first-service"

        # Try to re-init without force
        config = TelemetryConfig(service_name="second-service")
        hub.initialize_foundation(config, force=False)
        assert hub.get_foundation_config().service_name == "first-service"

    # Test re-initialization with force
    with TestEnvironment({"PROVIDE_SERVICE_NAME": "first-service"}):
        hub = get_hub()
        hub.initialize_foundation(force=True)  # Re-init with env var
        assert hub.get_foundation_config().service_name == "first-service"

        # Force re-init with new config
        config = TelemetryConfig(service_name="second-service")
        hub.initialize_foundation(config, force=True)
        assert hub.get_foundation_config().service_name == "second-service"

    # Test empty environment
    with patch.dict(os.environ, {}, clear=True):
        hub = get_hub()
        assert hub.get_foundation_config().service_name is None


# 🧱🏗️🔚
