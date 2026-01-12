#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for CLI error classes."""

from __future__ import annotations

from provide.testkit import FoundationTestCase

from provide.foundation.cli.errors import (
    CLIAdapterNotFoundError,
    CLIBuildError,
    CLIError,
    InvalidCLIHintError,
)


class TestCLIErrors(FoundationTestCase):
    """Test CLI error hierarchy."""

    def test_cli_error_base(self) -> None:
        """Test CLIError base class."""
        error = CLIError("Test error")
        assert str(error) == "Test error"
        assert error.code == "CLI_ERROR"

    def test_cli_error_with_context(self) -> None:
        """Test CLIError with context."""
        error = CLIError("Test error", custom_key="custom_value")
        assert error.context["custom_key"] == "custom_value"

    def test_invalid_cli_hint_error(self) -> None:
        """Test InvalidCLIHintError initialization and attributes."""
        error = InvalidCLIHintError("invalid", "username")

        assert error.hint == "invalid"
        assert error.param_name == "username"
        assert error.code == "CLI_INVALID_HINT"
        assert "Invalid CLI hint 'invalid'" in str(error)
        assert "parameter 'username'" in str(error)
        assert "Must be 'option' or 'argument'" in str(error)

    def test_invalid_cli_hint_error_context(self) -> None:
        """Test InvalidCLIHintError context dict."""
        error = InvalidCLIHintError("bad_hint", "param1")

        assert error.context["hint"] == "bad_hint"
        assert error.context["param_name"] == "param1"

    def test_cli_adapter_not_found_error(self) -> None:
        """Test CLIAdapterNotFoundError."""
        error = CLIAdapterNotFoundError("click", "cli")

        assert error.framework == "click"
        assert error.package == "cli"
        assert error.code == "CLI_ADAPTER_NOT_FOUND"
        assert "uv add 'provide-foundation[cli]'" in str(error)

    def test_cli_adapter_not_found_default_package(self) -> None:
        """Test CLIAdapterNotFoundError with default package."""
        error = CLIAdapterNotFoundError("typer")

        assert error.framework == "typer"
        assert error.package == "typer"
        assert "'typer'" in str(error)

    def test_cli_build_error(self) -> None:
        """Test CLIBuildError."""
        error = CLIBuildError("Build failed", command_name="test")

        assert error.code == "CLI_BUILD_ERROR"
        assert error.context["command_name"] == "test"
        assert "Build failed" in str(error)

    def test_cli_build_error_with_cause(self) -> None:
        """Test CLIBuildError with underlying cause."""
        cause = ValueError("Type error")
        error = CLIBuildError("Build failed", cause=cause)

        assert error.cause is cause
        assert error.__cause__ is cause


# 🧱🏗️🔚
