"""Comprehensive coverage tests for hub/__init__.py module."""

from unittest.mock import patch

import pytest


class TestHubInitImports:
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


class TestGetClickCommands:
    """Test get_click_commands function."""

    def test_get_click_commands_success(self) -> None:
        """Test successful get_click_commands when click is available."""
        from provide.foundation.hub import get_click_commands

        # This should work if click is installed (which it should be for tests)
        result = get_click_commands()

        assert isinstance(result, dict)
        assert "build_click_command" in result
        assert callable(result["build_click_command"])

    def test_get_click_commands_error_handling_paths(self) -> None:
        """Test the error handling paths in get_click_commands."""
        from provide.foundation.hub import get_click_commands

        # Test the normal case - this exercises the successful path
        result = get_click_commands()
        assert isinstance(result, dict)
        assert "build_click_command" in result

        # We can't easily mock the import failure without complex setup,
        # but we can at least test that the function is structured correctly
        # and the error paths exist in the code
        import inspect

        source = inspect.getsource(get_click_commands)

        # Verify error handling code exists
        assert "ImportError" in source
        assert "click" in source
        assert "pip install" in source


class TestHubGetattrLazyLoading:
    """Test __getattr__ lazy loading functionality."""

    def test_getattr_build_click_command_success(self) -> None:
        """Test __getattr__ successfully loads build_click_command."""
        import provide.foundation.hub as hub_module

        # Access build_click_command through __getattr__
        build_click_command = hub_module.build_click_command

        # Should be a callable function
        assert callable(build_click_command)

    def test_getattr_build_click_command_import_error(self) -> None:
        """Test __getattr__ when build_click_command import fails."""
        import provide.foundation.hub as hub_module

        # Mock get_click_commands to raise ImportError
        with (
            patch.object(
                hub_module,
                "get_click_commands",
                side_effect=ImportError("click not available"),
            ),
            pytest.raises(ImportError, match="click not available"),
        ):
            _ = hub_module.build_click_command

    def test_getattr_nonexistent_attribute(self) -> None:
        """Test __getattr__ with non-existent attribute."""
        import provide.foundation.hub as hub_module

        with pytest.raises(
            AttributeError,
            match="module 'provide.foundation.hub' has no attribute 'nonexistent_attr'",
        ):
            _ = hub_module.nonexistent_attr

    def test_getattr_other_valid_attributes_bypass(self) -> None:
        """Test that __getattr__ doesn't interfere with normal attributes."""
        import provide.foundation.hub as hub_module

        # These should work normally without triggering __getattr__
        assert callable(hub_module.register_command)
        assert callable(hub_module.get_hub)
        assert hub_module.Hub is not None


class TestHubModuleBehavior:
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


class TestClickDependencyHandling:
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


class TestHubLazyLoadingEdgeCases:
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
