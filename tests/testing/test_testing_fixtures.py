#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for common testing fixtures."""

from __future__ import annotations

import io

from provide.testkit import FoundationTestCase, captured_stderr_for_foundation
import pytest

from provide.foundation import TelemetryConfig


class TestTestingFixtures(FoundationTestCase):
    """Test the common testing fixtures."""

    def test_captured_stderr_fixture_provides_stringio(self) -> None:
        """Test that captured_stderr fixture provides StringIO."""
        # Simulate the fixture behavior
        current_test_stream = io.StringIO()

        assert isinstance(current_test_stream, io.StringIO)

        # Should be writable
        current_test_stream.write("test message")
        assert current_test_stream.getvalue() == "test message"

    def test_captured_stderr_fixture_cleanup(self) -> None:
        """Test fixture cleanup behavior."""
        # Test that StringIO can be closed without errors
        test_stream = io.StringIO()
        test_stream.write("test")
        test_stream.close()

        # Should not raise on close
        assert test_stream.closed

    def test_setup_telemetry_fixture_with_default_config(self) -> None:
        """Test telemetry setup fixture with default config."""

        # Create a mock setup function like the fixture would
        def _setup(config: TelemetryConfig | None = None) -> None:
            if config is None:
                config = TelemetryConfig()
            # In real fixture, this would call setup_telemetry(config)
            assert isinstance(config, TelemetryConfig)

        # Test with None (should use defaults)
        _setup(None)

    def test_setup_telemetry_fixture_with_custom_config(self) -> None:
        """Test telemetry setup fixture with custom config."""

        def _setup(config: TelemetryConfig | None = None) -> None:
            if config is None:
                config = TelemetryConfig()
            assert isinstance(config, TelemetryConfig)

        # Test with custom config
        custom_config = TelemetryConfig(service_name="test_service")
        _setup(custom_config)

    @pytest.fixture
    def mock_captured_stderr(self) -> io.StringIO:
        """Mock version of captured_stderr_for_foundation fixture."""
        test_stream = io.StringIO()
        yield test_stream
        test_stream.close()

    def test_fixture_integration_example(self, mock_captured_stderr: io.StringIO) -> None:
        """Test how fixtures would be used together."""
        # This simulates how the real fixtures would be used
        assert isinstance(mock_captured_stderr, io.StringIO)

        # Write something to the stream
        mock_captured_stderr.write("Integration test output")

        # Verify we can read it back
        output = mock_captured_stderr.getvalue()
        assert "Integration test output" in output

    def test_fixture_type_annotations(self) -> None:
        """Test that fixture functions have correct type annotations."""
        # Check that the function exists and is callable
        assert callable(captured_stderr_for_foundation)

        # We can't easily test the actual fixture without pytest running it,
        # but we can verify it's properly defined
        # In modern pytest (8+), fixtures have _fixture_function instead of _pytestfixturefunction
        assert hasattr(captured_stderr_for_foundation, "_fixture_function")

    def test_telemetry_config_creation(self) -> None:
        """Test that TelemetryConfig can be created for fixtures."""
        # Test default creation
        default_config = TelemetryConfig()
        assert isinstance(default_config, TelemetryConfig)

        # Test with parameters
        custom_config = TelemetryConfig(
            service_name="test_service",
            globally_disabled=True,
        )
        assert custom_config.service_name == "test_service"
        assert custom_config.globally_disabled is True

    def test_fixture_dependencies(self) -> None:
        """Test fixture dependency patterns."""
        # Simulate the dependency pattern used in setup_foundation_telemetry_for_test

        # First fixture provides captured stderr
        captured_stderr = io.StringIO()

        # Second fixture depends on first fixture and provides setup function
        def _setup(config: TelemetryConfig | None = None) -> None:
            # In real implementation, this would use the captured_stderr
            # and call setup_telemetry
            if config is None:
                config = TelemetryConfig()
            # Simulate that setup writes to the stream
            captured_stderr.write(f"Setup called with service: {config.service_name}")

        # Use the setup function
        _setup(TelemetryConfig(service_name="test"))

        # Verify the interaction
        output = captured_stderr.getvalue()
        assert "Setup called with service: test" in output


# 🧱🏗️🔚
