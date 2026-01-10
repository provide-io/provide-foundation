#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Tests for the tool registry system.

Tests registration, discovery, and retrieval of tool managers
through the hub-based registry infrastructure."""

from __future__ import annotations

from pathlib import Path

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import Mock, patch
import pytest

from provide.foundation.config import BaseConfig
from provide.foundation.tools.base import BaseToolManager
from provide.foundation.tools.registry import (
    ToolRegistry,
    get_tool_manager,
    get_tool_registry,
    register_tool_manager,
)


class MockToolManager(BaseToolManager):
    """Mock tool manager for testing."""

    tool_name = "mocktool"
    executable_name = "mocktool"
    supported_platforms = ["darwin", "linux"]

    def __init__(self, config: BaseConfig) -> None:
        # Create a minimal tools directory for testing
        super().__init__(config)
        self.tools_dir = Path("/tmp/test_tools")

    def get_download_info(self, version: str) -> tuple[str, str | None]:
        """Get download URL and checksum."""
        return f"https://example.com/mocktool-{version}.tar.gz", "abc123"

    def get_install_dir(self, version: str):
        """Get installation directory."""
        return self.tools_dir / self.tool_name / version

    def get_available_versions(self) -> list[str]:
        """Get available versions."""
        return ["1.0.0", "1.1.0", "2.0.0"]

    def get_metadata(self) -> dict[str, str]:
        """Get tool metadata."""
        return {
            "name": self.tool_name,
            "executable": self.executable_name,
            "platforms": ",".join(self.supported_platforms),
        }


class AnotherMockToolManager(BaseToolManager):
    """Another mock tool manager for testing."""

    tool_name = "anothertool"
    executable_name = "anothertool"
    supported_platforms = ["windows"]

    def __init__(self, config: BaseConfig) -> None:
        super().__init__(config)
        self.tools_dir = Path("/tmp/test_tools")

    def get_download_info(self, version: str) -> tuple[str, str | None]:
        """Get download URL and checksum."""
        return f"https://example.com/anothertool-{version}.zip", None

    def get_install_dir(self, version: str):
        """Get installation directory."""
        return self.tools_dir / self.tool_name / version

    def get_available_versions(self) -> list[str]:
        """Get available versions."""
        return ["1.0.0", "2.0.0"]

    def get_metadata(self) -> dict[str, str]:
        """Get tool metadata."""
        return {
            "name": self.tool_name,
            "executable": self.executable_name,
            "platforms": ",".join(self.supported_platforms),
        }


@pytest.fixture
def config():
    """Create a base config for testing."""
    return BaseConfig()


@pytest.fixture
def mock_hub():
    """Create a mock hub with registry."""
    hub = Mock()
    registry = Mock()

    # Set up registry mock methods
    registry.register = Mock()
    registry.get = Mock()
    registry.get_entry = Mock()
    registry.list_dimension = Mock()

    hub._component_registry = registry
    return hub


@pytest.fixture
def registry(mock_hub):
    """Create a tool registry with mocked hub."""
    with patch("provide.foundation.tools.registry.get_hub", return_value=mock_hub):
        with patch.object(ToolRegistry, "_discover_tools"):
            return ToolRegistry()


class TestToolRegistry(FoundationTestCase):
    """Tests for ToolRegistry class."""

    def test_init(self, mock_hub) -> None:
        """Test registry initialization."""
        with patch("provide.foundation.tools.registry.get_hub", return_value=mock_hub) as patch_get_hub:
            with patch.object(ToolRegistry, "_discover_tools") as patch_discover:
                registry = ToolRegistry()

                assert registry.hub == mock_hub
                patch_get_hub.assert_called_once()
                patch_discover.assert_called_once()

    def test_register_tool_manager(self, registry) -> None:
        """Test registering a tool manager."""
        registry.register_tool_manager("mocktool", MockToolManager)

        # Verify registration call
        registry.hub._component_registry.register.assert_called_once_with(
            name="mocktool",
            value=MockToolManager,
            dimension=ToolRegistry.DIMENSION,
            metadata={
                "tool_name": "mocktool",
                "executable": "mocktool",
                "platforms": ["darwin", "linux"],
            },
            aliases=None,
            replace=True,
        )

    def test_register_tool_manager_with_aliases(self, registry) -> None:
        """Test registering a tool manager with aliases."""
        aliases = ["mt", "mock"]
        registry.register_tool_manager("mocktool", MockToolManager, aliases=aliases)

        # Verify registration with aliases
        registry.hub._component_registry.register.assert_called_once_with(
            name="mocktool",
            value=MockToolManager,
            dimension=ToolRegistry.DIMENSION,
            metadata={
                "tool_name": "mocktool",
                "executable": "mocktool",
                "platforms": ["darwin", "linux"],
            },
            aliases=aliases,
            replace=True,
        )

    def test_get_tool_manager_class(self, registry) -> None:
        """Test retrieving a tool manager class."""
        registry.hub._component_registry.get.return_value = MockToolManager

        result = registry.get_tool_manager_class("mocktool")

        assert result == MockToolManager
        registry.hub._component_registry.get.assert_called_once_with(
            "mocktool",
            dimension=ToolRegistry.DIMENSION,
        )

    def test_get_tool_manager_class_not_found(self, registry) -> None:
        """Test retrieving a non-existent tool manager."""
        registry.hub._component_registry.get.return_value = None

        result = registry.get_tool_manager_class("nonexistent")

        assert result is None
        registry.hub._component_registry.get.assert_called_once_with(
            "nonexistent",
            dimension=ToolRegistry.DIMENSION,
        )

    def test_create_tool_manager(self, registry, config) -> None:
        """Test creating a tool manager instance."""
        registry.hub._component_registry.get.return_value = MockToolManager

        result = registry.create_tool_manager("mocktool", config)

        assert isinstance(result, MockToolManager)
        assert result.config == config

    def test_create_tool_manager_not_found(self, registry, config) -> None:
        """Test creating a non-existent tool manager."""
        registry.hub._component_registry.get.return_value = None

        result = registry.create_tool_manager("nonexistent", config)

        assert result is None

    def test_list_tools(self, registry) -> None:
        """Test listing all registered tools."""
        # Mock registry entries
        mock_entry1 = Mock()
        mock_entry1.metadata = {"tool_name": "tool1", "executable": "tool1"}

        mock_entry2 = Mock()
        mock_entry2.metadata = {"tool_name": "tool2", "executable": "tool2"}

        registry.hub._component_registry.list_dimension.return_value = [
            ("tool1", mock_entry1),
            ("tool2", mock_entry2),
        ]

        result = registry.list_tools()

        assert len(result) == 2
        assert result[0] == ("tool1", {"tool_name": "tool1", "executable": "tool1"})
        assert result[1] == ("tool2", {"tool_name": "tool2", "executable": "tool2"})

    def test_list_tools_no_metadata(self, registry) -> None:
        """Test listing tools when entry has no metadata."""
        mock_entry = Mock(spec=[])  # No metadata attribute

        registry.hub._component_registry.list_dimension.return_value = [("tool1", mock_entry)]

        result = registry.list_tools()

        assert len(result) == 1
        assert result[0] == ("tool1", {})

    def test_get_tool_info(self, registry) -> None:
        """Test getting information about a specific tool."""
        mock_entry = Mock()
        mock_entry.metadata = {
            "tool_name": "mocktool",
            "executable": "mocktool",
            "platforms": ["darwin", "linux"],
        }

        registry.hub._component_registry.get_entry.return_value = mock_entry

        result = registry.get_tool_info("mocktool")

        assert result == {
            "tool_name": "mocktool",
            "executable": "mocktool",
            "platforms": ["darwin", "linux"],
        }
        registry.hub._component_registry.get_entry.assert_called_once_with(
            "mocktool",
            dimension=ToolRegistry.DIMENSION,
        )

    def test_get_tool_info_not_found(self, registry) -> None:
        """Test getting info for non-existent tool."""
        registry.hub._component_registry.get_entry.return_value = None

        result = registry.get_tool_info("nonexistent")

        assert result is None

    def test_get_tool_info_no_metadata(self, registry) -> None:
        """Test getting info when entry has no metadata."""
        mock_entry = Mock(spec=[])  # No metadata attribute
        registry.hub._component_registry.get_entry.return_value = mock_entry

        result = registry.get_tool_info("tool")

        assert result is None

    def test_is_tool_registered(self, registry) -> None:
        """Test checking if a tool is registered."""
        registry.hub._component_registry.get.return_value = MockToolManager

        assert registry.is_tool_registered("mocktool") is True

        registry.hub._component_registry.get.return_value = None
        assert registry.is_tool_registered("nonexistent") is False


class TestDiscoverTools(FoundationTestCase):
    """Tests for tool discovery via entry points."""

    def test_discover_tools_python_311_plus(self, mock_hub) -> None:
        """Test tool discovery on Python 3.11+."""
        # Mock entry points
        mock_ep = Mock()
        mock_ep.name = "discovered_tool"
        mock_ep.load.return_value = MockToolManager

        mock_eps = Mock()
        mock_eps.select.return_value = [mock_ep]

        with patch("provide.foundation.tools.registry.get_hub", return_value=mock_hub):
            with patch("importlib.metadata.entry_points", return_value=mock_eps) as patch_entry_points:
                ToolRegistry()

                # Verify discovery
                patch_entry_points.assert_called_once()
                mock_eps.select.assert_called_once_with(group="provide.foundation.tools")
                mock_ep.load.assert_called_once()

                # Verify registration
                mock_hub._component_registry.register.assert_called_with(
                    name="discovered_tool",
                    value=MockToolManager,
                    dimension=ToolRegistry.DIMENSION,
                    metadata={
                        "tool_name": "mocktool",
                        "executable": "mocktool",
                        "platforms": ["darwin", "linux"],
                    },
                    aliases=None,
                    replace=True,
                )

    def test_discover_tools_load_error(self, mock_hub) -> None:
        """Test handling of tool load errors during discovery."""
        # Mock entry point that fails to load
        mock_ep = Mock()
        mock_ep.name = "broken_tool"
        mock_ep.load.side_effect = ImportError("Cannot import tool")

        mock_eps = Mock()
        mock_eps.select.return_value = [mock_ep]

        with patch("provide.foundation.tools.registry.get_hub", return_value=mock_hub):
            with patch("importlib.metadata.entry_points", return_value=mock_eps):
                # Should not crash, just log warning
                registry = ToolRegistry()
                assert registry is not None  # Successful construction despite error

    def test_discover_tools_no_entry_points(self, mock_hub) -> None:
        """Test when entry points are not available."""
        with (
            patch("provide.foundation.tools.registry.get_hub", return_value=mock_hub),
            patch(
                "importlib.metadata.entry_points",
                side_effect=AttributeError("No entry_points"),
            ),
        ):
            # Should not crash, just log debug message
            registry = ToolRegistry()
            assert registry is not None  # Successful construction despite error


class TestGlobalFunctions(FoundationTestCase):
    """Tests for global registry functions."""

    def test_get_tool_registry_singleton(self) -> None:
        """Test that get_tool_registry returns a singleton."""
        with patch("provide.foundation.tools.registry.get_hub"):
            with patch.object(ToolRegistry, "_discover_tools"):
                registry1 = get_tool_registry()
                registry2 = get_tool_registry()
                assert registry1 is registry2

    def test_register_tool_manager_global(self) -> None:
        """Test global register_tool_manager function."""
        mock_registry = Mock()
        with patch(
            "provide.foundation.tools.registry.get_tool_registry",
            return_value=mock_registry,
        ) as patch_get_registry:
            register_tool_manager("tool", MockToolManager, ["alias1", "alias2"])

            patch_get_registry.assert_called_once()
            mock_registry.register_tool_manager.assert_called_once_with(
                "tool",
                MockToolManager,
                ["alias1", "alias2"],
            )

    def test_get_tool_manager_global(self, config) -> None:
        """Test global get_tool_manager function."""
        mock_registry = Mock()
        mock_tool_manager = MockToolManager(config)
        mock_registry.create_tool_manager.return_value = mock_tool_manager

        with patch(
            "provide.foundation.tools.registry.get_tool_registry",
            return_value=mock_registry,
        ) as patch_get_registry:
            result = get_tool_manager("tool", config)

            assert isinstance(result, MockToolManager)
            patch_get_registry.assert_called_once()
            mock_registry.create_tool_manager.assert_called_once_with("tool", config)


class TestMultipleToolManagers(FoundationTestCase):
    """Tests for handling multiple tool managers."""

    def test_register_multiple_tools(self, registry) -> None:
        """Test registering multiple different tools."""
        registry.register_tool_manager("tool1", MockToolManager)
        registry.register_tool_manager("tool2", AnotherMockToolManager)

        assert registry.hub._component_registry.register.call_count == 2

        # Verify both registrations
        calls = registry.hub._component_registry.register.call_args_list

        assert calls[0][1]["name"] == "tool1"
        assert calls[0][1]["value"] == MockToolManager
        assert calls[0][1]["metadata"]["tool_name"] == "mocktool"

        assert calls[1][1]["name"] == "tool2"
        assert calls[1][1]["value"] == AnotherMockToolManager
        assert calls[1][1]["metadata"]["tool_name"] == "anothertool"

    def test_replace_existing_tool(self, registry) -> None:
        """Test that re-registration replaces existing tool."""
        registry.register_tool_manager("tool", MockToolManager)
        registry.register_tool_manager("tool", AnotherMockToolManager)

        # Both calls should have replace=True
        calls = registry.hub._component_registry.register.call_args_list
        assert all(call[1]["replace"] is True for call in calls)


class TestRegistryDimension(FoundationTestCase):
    """Tests for registry dimension management."""

    def test_dimension_constant(self) -> None:
        """Test that the dimension constant is set correctly."""
        assert ToolRegistry.DIMENSION == "tool_manager"

    def test_all_operations_use_correct_dimension(self, registry) -> None:
        """Test that all registry operations use the correct dimension."""
        # Register a tool
        registry.register_tool_manager("test", MockToolManager)

        # Get a tool
        registry.get_tool_manager_class("test")

        # Get tool info
        registry.get_tool_info("test")

        # Verify all calls used the correct dimension
        dimension_calls = (
            [call for call in registry.hub._component_registry.register.call_args_list]
            + [call for call in registry.hub._component_registry.get.call_args_list]
            + [call for call in registry.hub._component_registry.get_entry.call_args_list]
        )

        for call in dimension_calls:
            if "dimension" in call[1]:
                assert call[1]["dimension"] == ToolRegistry.DIMENSION


# 🧱🏗️🔚
