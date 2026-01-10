#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for Annotated type hint support in CLI building."""

from __future__ import annotations

from typing import Annotated

from click.testing import CliRunner
from provide.testkit import FoundationTestCase

from provide.foundation.cli import get_cli_adapter
from provide.foundation.hub.commands import register_command
from provide.foundation.hub.manager import clear_hub, get_hub


class TestAnnotatedCLISupport(FoundationTestCase):
    """Test Annotated type hints for explicit arg/option control."""

    def setup_method(self) -> None:
        """Clear hub before each test."""
        super().setup_method()
        clear_hub()

    def test_required_option_with_annotated(self) -> None:
        """Test Annotated[str, 'option'] creates optional option."""

        @register_command("create-user")
        def create_user(username: Annotated[str, "option"]) -> str:
            """Create user."""
            return f"Created user: {username}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Should succeed without --username (option is optional)
        result = runner.invoke(cli, ["create-user"])
        assert result.exit_code == 0

        # Should succeed with --username
        result = runner.invoke(cli, ["create-user", "--username", "alice"])
        assert result.exit_code == 0

    def test_optional_argument_with_annotated(self) -> None:
        """Test Annotated[str, 'argument'] with default creates optional argument."""

        @register_command("deploy")
        def deploy(env: Annotated[str, "argument"] = "staging") -> str:
            """Deploy to environment."""
            return f"Deploying to {env}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Should work without argument (uses default)
        result = runner.invoke(cli, ["deploy"])
        assert result.exit_code == 0

        # Should work with argument
        result = runner.invoke(cli, ["deploy", "production"])
        assert result.exit_code == 0

    def test_mixed_annotated_and_regular_params(self) -> None:
        """Test function with both Annotated and regular parameters."""

        @register_command("process")
        def process(
            file: Annotated[str, "option"],  # Explicit option
            format: str = "json",  # Option (Position-Based Hybrid: subsequent param with default)
            verbose: bool = False,  # Flag (booleans always flags)
        ) -> str:
            """Process file."""
            return f"Processing {file} as {format}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Test with required option
        result = runner.invoke(cli, ["process", "--file", "data.txt"])
        assert result.exit_code == 0

        # Test with all options
        result = runner.invoke(
            cli,
            ["process", "--file", "data.txt", "--format", "xml", "--verbose"],
        )
        assert result.exit_code == 0

    def test_cli_adapter_get_click(self) -> None:
        """Test get_cli_adapter returns ClickAdapter."""
        adapter = get_cli_adapter("click")

        assert adapter is not None
        # Verify it implements the protocol methods
        assert hasattr(adapter, "build_command")
        assert hasattr(adapter, "build_group")
        assert hasattr(adapter, "ensure_parent_groups")

    def test_backward_compatibility_without_annotated(self) -> None:
        """Test that functions without Annotated still work with Position-Based Hybrid."""

        @register_command("old-style")
        def old_style(name: str, greeting: str = "Hello") -> str:
            """Old-style command."""
            return f"{greeting}, {name}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # name (no default) → argument
        # greeting (has default, but comes after required arg) → option
        result = runner.invoke(cli, ["old-style", "Alice", "--greeting", "Hi"])
        assert result.exit_code == 0

    def test_argument_hint_overrides_default_behavior(self) -> None:
        """Test that 'argument' hint works even with a default."""

        @register_command("config")
        def config(profile: Annotated[str, "argument"] = "default") -> str:
            """Set config profile."""
            return f"Using profile: {profile}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Should work as positional argument
        result = runner.invoke(cli, ["config", "production"])
        assert result.exit_code == 0

        # Should work without argument (uses default)
        result = runner.invoke(cli, ["config"])
        assert result.exit_code == 0

    def test_option_hint_overrides_required_behavior(self) -> None:
        """Test that 'option' hint creates optional option without default."""

        @register_command("auth")
        def auth(token: Annotated[str, "option"]) -> str:
            """Authenticate with token."""
            return f"Authenticated with token: {token}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Should succeed without --token (option is optional)
        result = runner.invoke(cli, ["auth"])
        assert result.exit_code == 0

        # Should succeed with --token
        result = runner.invoke(cli, ["auth", "--token", "abc123"])
        assert result.exit_code == 0

    def test_position_based_hybrid_behavior(self) -> None:
        """Test Position-Based Hybrid: first param with default becomes optional argument."""

        @register_command("send")
        def send(message: str | None = None, level: str = "INFO", verbose: bool = False) -> str:
            """Send a message."""
            return f"Sending {message or 'empty'} at {level}"

        hub = get_hub()
        cli = hub.create_cli()
        runner = CliRunner()

        # Position-Based Hybrid:
        # - message (first param with default, non-bool) → optional argument
        # - level (subsequent param with default) → option
        # - verbose (bool) → flag

        # Test with positional message
        result = runner.invoke(cli, ["send", "Hello"])
        assert result.exit_code == 0

        # Test with positional message and options
        result = runner.invoke(cli, ["send", "Hello", "--level", "DEBUG", "--verbose"])
        assert result.exit_code == 0

        # Test without message (uses default None)
        result = runner.invoke(cli, ["send", "--level", "ERROR"])
        assert result.exit_code == 0


# 🧱🏗️🔚
