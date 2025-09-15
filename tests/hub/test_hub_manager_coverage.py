"""Additional tests for Hub manager to improve code coverage."""

from unittest.mock import Mock, patch

import click

from provide.foundation.hub.manager import Hub


class TestHubManagerCoverage:
    """Test Hub manager functionality for improved coverage."""

    def test_get_component_returns_none_for_missing(self):
        """Test get_component returns None for non-existent component."""
        hub = Hub()
        assert hub.get_component("nonexistent") is None

    def test_list_components_with_dimension_filter(self):
        """Test list_components with dimension filter."""
        hub = Hub()

        # Add a component with a custom dimension
        class TestComponent:
            pass

        hub.add_component(TestComponent, "test", dimension="custom")

        # Test filtering by dimension
        custom_components = hub.list_components(dimension="custom")
        assert "test" in custom_components

        # Test that it doesn't appear in other dimensions
        default_components = hub.list_components(dimension="component")
        assert "test" not in default_components

    def test_list_components_excludes_commands(self):
        """Test that list_components excludes command dimension."""
        hub = Hub()

        # Add a component and a command
        class TestComponent:
            pass

        @click.command()
        def test_cmd():
            pass

        hub.add_component(TestComponent, "component")
        hub.add_command(test_cmd, "test_cmd")

        # List all components should exclude commands
        components = hub.list_components()
        assert "component" in components
        assert "test_cmd" not in components

    def test_discover_components_with_entry_points(self):
        """Test component discovery from entry points."""
        hub = Hub()

        # Mock the _discover_components function
        mock_components = {
            "discovered_comp": Mock,
        }

        with patch(
            "provide.foundation.hub.components.discover_components",
            return_value=mock_components,
        ):
            result = hub.discover_components("test_group")

            # Check that components were discovered
            assert result == mock_components

    def test_add_cli_group_imports_commands(self):
        """Test that add_cli_group imports commands from a click group."""
        hub = Hub()

        # Create a click group with commands
        @click.group()
        def test_group():
            pass

        @test_group.command()
        def sub_cmd():
            pass

        # Add the group to hub (this should import its commands)
        hub.add_cli_group(test_group)

        # Check that the command was imported (Click changes underscores to hyphens)
        assert hub.get_command("sub") is not None

    def test_initialize_components_with_initialize_method(self):
        """Test initialize() calls initialize on components that support it."""
        hub = Hub()

        # Create a component with initialize method
        class ComponentWithInit:
            initialized = False

            @classmethod
            def initialize(cls):
                cls.initialized = True

        # Create a component without initialize method
        class ComponentWithoutInit:
            pass

        hub.add_component(ComponentWithInit, "with_init")
        hub.add_component(ComponentWithoutInit, "without_init")

        # Initialize all components
        hub.initialize()

        # Check that only the component with initialize was called
        assert ComponentWithInit.initialized is True

    def test_initialize_handles_component_initialization_errors(self):
        """Test initialize() handles errors during component initialization."""
        hub = Hub()

        # Create a component that raises an error during initialization
        class FailingComponent:
            @classmethod
            def initialize(cls):
                raise RuntimeError("Initialization failed")

        hub.add_component(FailingComponent, "failing")

        # Should not raise an error, but handle it gracefully
        hub.initialize()  # Should not raise

    def test_cleanup_components_with_cleanup_method(self):
        """Test cleanup() calls cleanup on components that support it."""
        hub = Hub()

        # Create a component with cleanup method
        class ComponentWithCleanup:
            cleaned_up = False

            @classmethod
            def cleanup(cls):
                cls.cleaned_up = True

        hub.add_component(ComponentWithCleanup, "with_cleanup")

        # Cleanup all components
        hub.cleanup()

        # Check that cleanup was called
        assert ComponentWithCleanup.cleaned_up is True

    def test_cleanup_handles_component_cleanup_errors(self):
        """Test cleanup() handles errors during component cleanup."""
        hub = Hub()

        # Create a component that raises an error during cleanup
        class FailingCleanupComponent:
            @classmethod
            def cleanup(cls):
                raise RuntimeError("Cleanup failed")

        hub.add_component(FailingCleanupComponent, "failing_cleanup")

        # Should not raise an error, but handle it gracefully
        hub.cleanup()  # Should not raise

    def test_clear_components_and_commands(self):
        """Test clearing all components and commands."""
        hub = Hub()

        # Add some components and commands
        class TestComponent:
            pass

        @click.command()
        def test_cmd():
            pass

        hub.add_component(TestComponent, "comp")
        hub.add_command(test_cmd, "cmd")

        # Clear everything
        hub.clear()

        # Check that everything was cleared
        assert hub.get_component("comp") is None
        assert hub.get_command("cmd") is None
        assert len(hub.list_components()) == 0
        assert len(hub.list_commands()) == 0

    def test_context_manager_cleanup(self):
        """Test Hub as context manager calls cleanup on exit."""

        class ComponentWithCleanup:
            cleaned_up = False

            @classmethod
            def cleanup(cls):
                cls.cleaned_up = True

        # Use Hub as context manager
        with Hub() as hub:
            hub.add_component(ComponentWithCleanup, "comp")

        # Check that cleanup was called when exiting context
        assert ComponentWithCleanup.cleaned_up is True
