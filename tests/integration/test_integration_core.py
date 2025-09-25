"""Core integration tests for the Foundation library."""

import os
from unittest.mock import patch

import pytest

from provide.foundation import (
    LoggingConfig,
    TelemetryConfig,
    get_hub,
    logger,
)
from provide.foundation.cli import get_cli
from provide.foundation.errors import FoundationError
from provide.foundation.hub.registry import Registry
from provide.testkit import (
    FoundationTestbed,
    TestEnvironment,
    Testkit,
    reset_foundation_setup_for_testing,
)

# Mark all tests in this file to run serially to avoid global state pollution
pytestmark = pytest.mark.serial


@pytest.fixture(autouse=True)
def manage_environment() -> None:
    """Ensure Foundation state is reset for each test."""
    reset_foundation_setup_for_testing()


def test_basic_initialization_and_logging(testkit: Testkit) -> None:
    """Test basic initialization and logging."""
    logger.info("Test message", key="value")
    log_output = testkit.caplog.text
    assert "Test message" in log_output
    assert "key=value" in log_output


def test_hub_and_registry_integration(testkit: Testkit) -> None:
    """Test Hub and Registry integration."""
    hub = get_hub()
    assert hub is not None
    assert isinstance(hub._command_registry, Registry)

    hub._command_registry.register("test_cmd", lambda: "success")
    cmd = hub._command_registry.get("test_cmd")
    assert cmd() == "success"


def test_cli_integration(testkit: Testkit) -> None:
    """Test CLI integration."""
    hub = get_hub()

    @hub.command("test-cli")
    def test_cli_cmd() -> None:
        """A test CLI command."""
        print("CLI command executed")

    cli = get_cli()
    result = testkit.invoke_cli(cli, ["test-cli"])
    assert result.exit_code == 0
    assert "CLI command executed" in result.output


def test_configuration_from_environment(testkit: Testkit) -> None:
    """Test configuration loading from environment variables."""
    with TestEnvironment(
        PROVIDE_SERVICE_NAME="test-service",
        PROVIDE_LOG_LEVEL="DEBUG",
    ):
        reset_foundation_setup_for_testing()  # Re-init with new env vars
        hub = get_hub()
        assert hub.get_service_name() == "test-service"

        logger.debug("Debug message should be visible")
        log_output = testkit.caplog.text
        assert "Debug message should be visible" in log_output


def test_explicit_configuration_override(testkit: Testkit) -> None:
    """Test explicit configuration overrides environment variables."""
    with TestEnvironment(PROVIDE_SERVICE_NAME="env-service"):
        config = TelemetryConfig(
            service_name="explicit-service",
            logging=LoggingConfig(default_level="WARNING"),
        )
        hub = get_hub()
        hub.initialize_foundation(config, force=True)

        assert hub.get_service_name() == "explicit-service"

        logger.info("Info message should be hidden")
        logger.warning("Warning message should be visible")
        log_output = testkit.caplog.text

        assert "Info message should be hidden" not in log_output
        assert "Warning message should be visible" in log_output


def test_error_handling_integration(testkit: Testkit) -> None:
    """Test error handling integration."""
    with pytest.raises(FoundationError, match="Test error"):
        raise FoundationError("Test error", code="TEST_001")

    try:
        raise FoundationError("Another test error")
    except FoundationError:
        logger.exception("Caught expected error")

    log_output = testkit.caplog.text
    assert "Caught expected error" in log_output
    assert "FoundationError: Another test error" in log_output


def test_component_loading_and_usage(testkit: Testkit) -> None:
    """Test component loading and usage."""
    hub = get_hub()

    class TestComponent:
        def __init__(self) -> None:
            self.value = "test"

    hub.register_component("test_component", TestComponent)
    component = hub.get_component("test_component")
    assert isinstance(component, TestComponent)
    assert component.value == "test"


def test_foundation_testbed_integration(testkit: Testkit) -> None:
    """Test integration with FoundationTestbed."""
    with FoundationTestbed() as testbed:
        testbed.set_env("PROVIDE_SERVICE_NAME", "testbed-service")
        testbed.set_config(
            TelemetryConfig(logging=LoggingConfig(default_level="DEBUG")),
        )

        hub = get_hub()
        assert hub.get_service_name() == "testbed-service"

        logger.debug("Testbed debug message")
        assert "Testbed debug message" in testbed.caplog.text


def test_context_propagation_in_logs(testkit: Testkit) -> None:
    """Test context propagation in logs."""
    with logger.context_provider({"request_id": "req-123"}):
        logger.info("Processing request")

    log_output = testkit.caplog.text
    assert "request_id=req-123" in log_output


def test_configuration_edge_cases(testkit: Testkit) -> None:
    """Test configuration edge cases."""
    # Test that re-initialization without force does nothing
    with TestEnvironment(PROVIDE_SERVICE_NAME="first-service"):
        reset_foundation_setup_for_testing()
        hub = get_hub()
        assert hub.get_service_name() == "first-service"

        # Try to re-init without force
        config = TelemetryConfig(service_name="second-service")
        hub.initialize_foundation(config, force=False)
        assert hub.get_service_name() == "first-service"

    # Test re-initialization with force
    reset_foundation_setup_for_testing()
    with TestEnvironment(PROVIDE_SERVICE_NAME="first-service"):
        hub = get_hub()
        hub.initialize_foundation(force=True)  # Re-init with env var
        assert hub.get_service_name() == "first-service"

        # Force re-init with new config
        config = TelemetryConfig(service_name="second-service")
        hub.initialize_foundation(config, force=True)
        assert hub.get_service_name() == "second-service"

    # Test empty environment
    with patch.dict(os.environ, {}, clear=True):
        reset_foundation_setup_for_testing()
        hub = get_hub()
        assert hub.get_service_name() is None
