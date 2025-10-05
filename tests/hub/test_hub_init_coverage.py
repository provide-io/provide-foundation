"""Comprehensive coverage tests for hub/__init__.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase


class TestHubInitImports(FoundationTestCase):
    """Test hub module imports and exports."""

    def test_core_imports_available(self) -> None:
        """Test that core hub imports are available."""
        from provide.foundation.hub import (
            ComponentCategory,
            Hub,
            build_click_command,
            clear_hub,
            get_component_registry,
            get_hub,
            register_command,
        )

        # All should be callable or accessible
        assert callable(register_command)
        assert ComponentCategory is not None
        assert callable(get_component_registry)
        assert Hub is not None
        assert callable(clear_hub)
        assert callable(get_hub)
        assert callable(build_click_command)

    def test_all_exports_defined(self) -> None:
        """Test that __all__ exports are properly defined."""
        import provide.foundation.hub as hub_module

        expected_exports = [
            "get_component_registry",
            "ComponentCategory",
            "Hub",
            "clear_hub",
            "get_hub",
            "register_command",
            "build_click_command",
        ]

        assert hasattr(hub_module, "__all__")
        for export in expected_exports:
            assert export in hub_module.__all__
            assert hasattr(hub_module, export)


class TestBuildClickCommandStub(FoundationTestCase):
    """Test build_click_command stub behavior."""

    def test_build_click_command_available(self) -> None:
        """Test that build_click_command is available (real or stub)."""
        from provide.foundation.hub import build_click_command

        # Should be callable (either real function or stub)
        assert callable(build_click_command)

    def test_build_click_command_in_all(self) -> None:
        """Test that build_click_command is in __all__."""
        import provide.foundation.hub as hub_module

        assert "build_click_command" in hub_module.__all__


class TestHubModuleBehavior(FoundationTestCase):
    """Test overall hub module behavior and integration."""

    def test_module_docstring_present(self) -> None:
        """Test that module has comprehensive docstring."""
        import provide.foundation.hub as hub_module

        assert hub_module.__doc__ is not None
        assert len(hub_module.__doc__) > 100
        assert "Hub" in hub_module.__doc__
        assert "Component" in hub_module.__doc__

    def test_lazy_loading_integration(self) -> None:
        """Test integration between lazy loading and normal imports."""
        import provide.foundation.hub as hub_module

        # Test that we can mix normal imports and lazy loading
        hub = hub_module.get_hub()
        assert hub is not None

        # Test lazy loading works alongside normal imports
        try:
            build_click_command = hub_module.build_click_command
            assert callable(build_click_command)
        except ImportError:
            # It's OK if click isn't available, that's what the lazy loading handles
            pass

    def test_all_documented_features_accessible(self) -> None:
        """Test that features mentioned in docstring are accessible."""
        import provide.foundation.hub as hub_module

        # Features mentioned in docstring should be accessible
        assert hasattr(hub_module, "Hub")
        assert hasattr(hub_module, "register_command")

        # Test creating hub instance as shown in docstring
        hub = hub_module.Hub()
        assert hub is not None

        # Test getting component registry
        registry = hub_module.get_component_registry()
        assert registry is not None


# Removed obsolete test classes:
# - TestClickDependencyHandling (tested removed get_click_commands)
# - TestHubLazyLoadingEdgeCases (tested removed __getattr__)
