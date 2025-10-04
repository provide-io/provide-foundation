"""Comprehensive coverage tests for hub/__init__.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest


class TestHubInitImports(FoundationTestCase):
    """Test hub module imports and exports."""

    def test_core_imports_available(self) -> None:
        """Test that core hub imports are available."""
        from provide.foundation.hub import (
            ComponentCategory,
            Hub,
            clear_hub,
            get_click_commands,
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
        assert callable(get_click_commands)

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
            "get_click_commands",
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


class TestClickDependencyHandling(FoundationTestCase):
    """Test handling of optional click dependency."""

    def test_module_works_without_click_features(self) -> None:
        """Test that core hub functionality works even if click features fail."""
        import provide.foundation.hub as hub_module

        # Core features should always work
        hub = hub_module.Hub()
        assert hub is not None

        registry = hub_module.get_component_registry()
        assert registry is not None

        assert callable(hub_module.register_command)
        assert callable(hub_module.get_hub)
        assert callable(hub_module.clear_hub)

    def test_click_features_lazy_loading_error_handling(self) -> None:
        """Test error handling in click features lazy loading."""
        import provide.foundation.hub as hub_module

        # Mock the get_click_commands to fail
        with patch.object(hub_module, "get_click_commands") as mock_get_commands:
            mock_get_commands.side_effect = ImportError("Mocked click unavailable")

            # Accessing build_click_command should raise the ImportError
            with pytest.raises(ImportError, match="Mocked click unavailable"):
                _ = hub_module.build_click_command

    def test_import_error_detection_logic_exists(self) -> None:
        """Test that ImportError detection logic exists in the code."""
        import inspect

        import provide.foundation.hub as hub_module

        # Check that the get_click_commands function has the right structure
        source = inspect.getsource(hub_module.get_click_commands)

        # Verify the error detection and handling logic is present
        assert 'if "click" in str(e)' in source
        assert "pip install" in source
        assert "provide-foundation[cli]" in source


class TestHubLazyLoadingEdgeCases(FoundationTestCase):
    """Test edge cases in lazy loading functionality."""

    def test_multiple_getattr_calls_consistency(self) -> None:
        """Test that multiple calls to __getattr__ are consistent."""
        import provide.foundation.hub as hub_module

        try:
            # Multiple accesses should return the same thing
            cmd1 = hub_module.build_click_command
            cmd2 = hub_module.build_click_command

            # Should be the same function
            assert cmd1 is cmd2
        except ImportError:
            # Expected if click is not available
            pass

    def test_getattr_with_various_attribute_names(self) -> None:
        """Test __getattr__ behavior with various attribute names."""
        import provide.foundation.hub as hub_module

        # Test the specific handled attribute
        test_cases = [
            ("build_click_command", True),  # Should be handled specially
            ("other_command", False),  # Should raise AttributeError
            (
                "get_click_commands",
                False,
            ),  # This is a regular attribute, not lazy loaded
            ("__version__", False),  # Standard Python attribute
        ]

        for attr_name, should_be_special in test_cases:
            if should_be_special:
                try:
                    attr = getattr(hub_module, attr_name)
                    assert callable(attr)
                except ImportError:
                    # Expected if dependencies aren't available
                    pass
            elif attr_name == "get_click_commands":
                # This should work as normal attribute
                assert callable(getattr(hub_module, attr_name))
            else:
                # These should raise AttributeError
                with pytest.raises(AttributeError):
                    _ = getattr(hub_module, attr_name)
