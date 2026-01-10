#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for Click CLI adapter."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch

from provide.foundation.cli.click.adapter import ClickAdapter
from provide.foundation.hub.info import CommandInfo


class TestClickAdapterBuildCommand(FoundationTestCase):
    """Tests for ClickAdapter.build_command method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.adapter = ClickAdapter()

    def test_build_command_delegates_to_builder(self) -> None:
        """Test build_command delegates to build_click_command_from_info."""
        # Create mock CommandInfo
        mock_func = Mock()
        command_info = CommandInfo(
            name="test-command",
            func=mock_func,
            description="Test command",
        )

        # Mock the build_click_command_from_info function
        mock_command = Mock()
        with patch(
            "provide.foundation.cli.click.adapter.build_click_command_from_info",
            return_value=mock_command,
        ) as mock_builder:
            result = self.adapter.build_command(command_info)

            # Verify delegation
            mock_builder.assert_called_once_with(command_info)
            assert result == mock_command

    def test_build_command_with_complex_command_info(self) -> None:
        """Test build_command with fully populated CommandInfo."""
        mock_func = Mock()
        command_info = CommandInfo(
            name="complex-cmd",
            func=mock_func,
            description="Complex command with metadata",
            aliases=["cc", "cplx"],
            hidden=True,
            category="advanced",
            metadata={"author": "test", "version": "1.0"},
            parent="db.migrate",
        )

        mock_command = Mock()
        with patch(
            "provide.foundation.cli.click.adapter.build_click_command_from_info",
            return_value=mock_command,
        ) as mock_builder:
            result = self.adapter.build_command(command_info)

            # Verify the CommandInfo object was passed correctly
            mock_builder.assert_called_once_with(command_info)
            assert result == mock_command


class TestClickAdapterBuildGroup(FoundationTestCase):
    """Tests for ClickAdapter.build_group method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.adapter = ClickAdapter()

    def test_build_group_with_command_list(self) -> None:
        """Test build_group extracts command names from CommandInfo list."""
        # Create mock CommandInfo objects
        mock_func1 = Mock()
        mock_func2 = Mock()
        mock_func3 = Mock()

        commands = [
            CommandInfo(name="cmd1", func=mock_func1),
            CommandInfo(name="cmd2", func=mock_func2),
            CommandInfo(name="cmd3", func=mock_func3),
        ]

        mock_group = Mock()
        mock_registry = Mock()

        with patch(
            "provide.foundation.cli.click.adapter.create_command_group",
            return_value=mock_group,
        ) as mock_creator:
            result = self.adapter.build_group(
                name="test-group",
                commands=commands,
                registry=mock_registry,
            )

            # Verify command names were extracted
            mock_creator.assert_called_once_with(
                name="test-group",
                commands=["cmd1", "cmd2", "cmd3"],
                registry=mock_registry,
            )
            assert result == mock_group

    def test_build_group_without_commands(self) -> None:
        """Test build_group with no commands (uses registry)."""
        mock_group = Mock()
        mock_registry = Mock()

        with patch(
            "provide.foundation.cli.click.adapter.create_command_group",
            return_value=mock_group,
        ) as mock_creator:
            result = self.adapter.build_group(
                name="empty-group",
                registry=mock_registry,
            )

            # Verify None is passed for commands
            mock_creator.assert_called_once_with(
                name="empty-group",
                commands=None,
                registry=mock_registry,
            )
            assert result == mock_group

    def test_build_group_with_kwargs(self) -> None:
        """Test build_group forwards additional kwargs."""
        mock_group = Mock()
        mock_registry = Mock()

        with patch(
            "provide.foundation.cli.click.adapter.create_command_group",
            return_value=mock_group,
        ) as mock_creator:
            result = self.adapter.build_group(
                name="custom-group",
                registry=mock_registry,
                help="Custom help text",
                invoke_without_command=True,
                chain=True,
            )

            # Verify kwargs are forwarded
            mock_creator.assert_called_once_with(
                name="custom-group",
                commands=None,
                registry=mock_registry,
                help="Custom help text",
                invoke_without_command=True,
                chain=True,
            )
            assert result == mock_group

    def test_build_group_empty_command_list(self) -> None:
        """Test build_group with empty command list."""
        mock_group = Mock()
        mock_registry = Mock()

        with patch(
            "provide.foundation.cli.click.adapter.create_command_group",
            return_value=mock_group,
        ) as mock_creator:
            result = self.adapter.build_group(
                name="test-group",
                commands=[],  # Empty list
                registry=mock_registry,
            )

            # Empty list is falsy, so command_names should be None
            mock_creator.assert_called_once_with(
                name="test-group",
                commands=None,
                registry=mock_registry,
            )
            assert result == mock_group

    def test_build_group_commands_and_registry_both_none(self) -> None:
        """Test build_group with both commands and registry as None."""
        mock_group = Mock()

        with patch(
            "provide.foundation.cli.click.adapter.create_command_group",
            return_value=mock_group,
        ) as mock_creator:
            result = self.adapter.build_group(name="minimal-group")

            # Verify both are passed as None
            mock_creator.assert_called_once_with(
                name="minimal-group",
                commands=None,
                registry=None,
            )
            assert result == mock_group


class TestClickAdapterEnsureParentGroups(FoundationTestCase):
    """Tests for ClickAdapter.ensure_parent_groups method."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.adapter = ClickAdapter()

    def test_ensure_parent_groups_delegates_to_hierarchy(self) -> None:
        """Test ensure_parent_groups delegates to ensure_parent_groups function."""
        mock_registry = Mock()

        with patch("provide.foundation.cli.click.adapter.ensure_parent_groups") as mock_ensure:
            self.adapter.ensure_parent_groups("db.migrate.up", mock_registry)

            # Verify delegation
            mock_ensure.assert_called_once_with("db.migrate.up", mock_registry)

    def test_ensure_parent_groups_single_level(self) -> None:
        """Test ensure_parent_groups with single-level path."""
        mock_registry = Mock()

        with patch("provide.foundation.cli.click.adapter.ensure_parent_groups") as mock_ensure:
            self.adapter.ensure_parent_groups("db", mock_registry)

            mock_ensure.assert_called_once_with("db", mock_registry)

    def test_ensure_parent_groups_multi_level(self) -> None:
        """Test ensure_parent_groups with multi-level path."""
        mock_registry = Mock()

        with patch("provide.foundation.cli.click.adapter.ensure_parent_groups") as mock_ensure:
            self.adapter.ensure_parent_groups("app.db.migrate.rollback", mock_registry)

            mock_ensure.assert_called_once_with("app.db.migrate.rollback", mock_registry)


class TestClickAdapterIntegration(FoundationTestCase):
    """Integration tests for ClickAdapter."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()
        self.adapter = ClickAdapter()

    def test_adapter_protocol_methods_exist(self) -> None:
        """Test that adapter implements expected protocol methods."""
        assert hasattr(self.adapter, "build_command")
        assert callable(self.adapter.build_command)

        assert hasattr(self.adapter, "build_group")
        assert callable(self.adapter.build_group)

        assert hasattr(self.adapter, "ensure_parent_groups")
        assert callable(self.adapter.ensure_parent_groups)

    def test_adapter_is_stateless(self) -> None:
        """Test that adapter can be used without initialization."""
        # Should work without any setup
        adapter1 = ClickAdapter()
        adapter2 = ClickAdapter()

        # Different instances should behave identically
        mock_func = Mock()
        command_info = CommandInfo(name="test", func=mock_func)

        with patch(
            "provide.foundation.cli.click.adapter.build_click_command_from_info",
            return_value=Mock(),
        ):
            # Both adapters should work independently
            adapter1.build_command(command_info)
            adapter2.build_command(command_info)


__all__ = [
    "TestClickAdapterBuildCommand",
    "TestClickAdapterBuildGroup",
    "TestClickAdapterEnsureParentGroups",
    "TestClickAdapterIntegration",
]

# 🧱🏗️🔚
