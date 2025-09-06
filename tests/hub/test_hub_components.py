"""Tests for component registration functionality."""

import pytest

from provide.foundation.errors import AlreadyExistsError
from provide.foundation.hub.components import (
    discover_components,
)
from provide.foundation.hub.manager import clear_hub, get_hub


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
        """Test discovering components from entry points - stub implementation."""
        # discover_components exists but returns empty dict in current implementation
        discovered = discover_components("provide.components")

        # Current implementation is a stub that returns empty dict
        assert isinstance(discovered, dict)
        assert len(discovered) == 0
