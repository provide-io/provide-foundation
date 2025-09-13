"""Tests for component registration functionality."""


from provide.foundation.hub.components import (
    discover_components,
)
from provide.foundation.hub.manager import clear_hub

# Legacy component registration tests removed - replaced by registry-based architecture
#
# The original tests in this file were designed for a decorator-based component
# registration system (@register_component) and BaseComponent class that no longer
# exist in the current registry-based hub architecture.
#
# The current system uses:
# - Registry.register() for direct component registration
# - ComponentCategory for categorizing components
# - No BaseComponent base class requirement
# - Entry point discovery through discover_components()


class TestComponentDiscovery:
    """Test component discovery functionality that still exists."""

    def setup_method(self) -> None:
        """Clear the hub before each test."""
        clear_hub()

    def test_discover_components_from_entry_points(self, monkeypatch) -> None:
        """Test discovering components from entry points - real implementation."""
        # Test with a non-existent group - should return empty dict gracefully
        discovered = discover_components("non.existent.group")
        assert isinstance(discovered, dict)
        assert len(discovered) == 0

    def test_discover_components_with_mock_entry_points(self, monkeypatch) -> None:
        """Test component discovery with mocked entry points."""
        from unittest.mock import Mock
        import importlib.metadata as metadata

        # Create a mock entry point
        mock_entry_point = Mock()
        mock_entry_point.name = "test_component"
        mock_entry_point.module = "test.module"
        mock_component_class = Mock()
        mock_entry_point.load.return_value = mock_component_class

        # Create mock entry points result
        mock_entry_points = Mock()
        mock_entry_points.select.return_value = [mock_entry_point]

        # Mock the metadata.entry_points() function
        monkeypatch.setattr(metadata, "entry_points", lambda: mock_entry_points)

        # Test discovery
        discovered = discover_components("test.components")

        # Verify the component was discovered
        assert isinstance(discovered, dict)
        assert "test_component" in discovered
        assert discovered["test_component"] is mock_component_class

    def test_discover_components_handles_load_errors(self, monkeypatch) -> None:
        """Test that component discovery handles loading errors gracefully."""
        from unittest.mock import Mock
        import importlib.metadata as metadata

        # Create a mock entry point that fails to load
        mock_entry_point = Mock()
        mock_entry_point.name = "broken_component"
        mock_entry_point.module = "broken.module"
        mock_entry_point.load.side_effect = ImportError("Module not found")

        # Create mock entry points result
        mock_entry_points = Mock()
        mock_entry_points.select.return_value = [mock_entry_point]

        # Mock the metadata.entry_points() function
        monkeypatch.setattr(metadata, "entry_points", lambda: mock_entry_points)

        # Test discovery - should not raise, should return empty dict
        discovered = discover_components("test.components")

        # Verify graceful error handling
        assert isinstance(discovered, dict)
        assert len(discovered) == 0

    def test_discover_components_registers_in_hub(self, monkeypatch) -> None:
        """Test that discovered components are registered in the hub registry."""
        from unittest.mock import Mock
        import importlib.metadata as metadata
        from provide.foundation.hub.components import get_component_registry

        # Create a mock entry point
        mock_entry_point = Mock()
        mock_entry_point.name = "registered_component"
        mock_entry_point.module = "test.module"
        mock_component_class = Mock()
        mock_entry_point.load.return_value = mock_component_class

        # Create mock entry points result
        mock_entry_points = Mock()
        mock_entry_points.select.return_value = [mock_entry_point]

        # Mock the metadata.entry_points() function
        monkeypatch.setattr(metadata, "entry_points", lambda: mock_entry_points)

        # Discover components
        discovered = discover_components("test.components", dimension="test_dimension")

        # Verify the component was discovered
        assert "registered_component" in discovered

        # Verify the component was registered in the hub
        registry = get_component_registry()
        registered_component = registry.get("registered_component", "test_dimension")
        assert registered_component is mock_component_class

        # Verify metadata was set correctly
        entry = registry.get_entry("registered_component", "test_dimension")
        assert entry is not None
        assert entry.metadata["entry_point"] == "registered_component"
        assert entry.metadata["module"] == "test.module"
        assert entry.metadata["discovered"] is True
