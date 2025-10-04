"""Comprehensive coverage tests for hub/commands.py module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest


class TestHubCommandsImports(FoundationTestCase):
    """Test hub commands module imports and exports."""

    def test_core_imports_available(self) -> None:
        """Test that core command imports are always available."""
        from provide.foundation.hub.commands import (
            CommandInfo,
            get_command_registry,
            register_command,
        )

        # Core functionality should always be available
        assert callable(register_command)
        assert CommandInfo is not None
        assert callable(get_command_registry)

    def test_all_exports_defined(self) -> None:
        """Test that __all__ exports are properly defined."""
        import provide.foundation.hub.commands as commands_module

        expected_exports = [
            "CommandInfo",
            "build_click_command",
            "create_command_group",
            "get_command_registry",
            "register_command",
        ]

        assert hasattr(commands_module, "__all__")
        for export in expected_exports:
            assert export in commands_module.__all__


class TestLazyLoadingFeatures(FoundationTestCase):
    """Test lazy loading of click-dependent features."""

    def test_build_click_command_success(self) -> None:
        """Test successful lazy loading of build_click_command."""
        from provide.foundation.hub.commands import build_click_command

        # Should successfully import and be callable
        assert callable(build_click_command)

    def test_create_command_group_success(self) -> None:
        """Test successful lazy loading of create_command_group."""
        from provide.foundation.hub.commands import create_command_group

        # Should successfully import and be callable
        assert callable(create_command_group)

    def test_getattr_build_click_command(self) -> None:
        """Test __getattr__ for build_click_command."""
        import provide.foundation.hub.commands as commands_module

        # Access through getattr should work
        build_command = commands_module.build_click_command
        assert callable(build_command)

    def test_getattr_create_command_group(self) -> None:
        """Test __getattr__ for create_command_group."""
        import provide.foundation.hub.commands as commands_module

        # Access through getattr should work
        create_group = commands_module.create_command_group
        assert callable(create_group)

    def test_getattr_nonexistent_attribute(self) -> None:
        """Test __getattr__ with non-existent attribute."""
        import provide.foundation.hub.commands as commands_module

        with pytest.raises(
            AttributeError,
            match="module 'provide.foundation.hub.commands' has no attribute 'nonexistent'",
        ):
            _ = commands_module.nonexistent

    def test_getattr_normal_attributes_bypass(self) -> None:
        """Test that __getattr__ doesn't interfere with normal attributes."""
        import provide.foundation.hub.commands as commands_module

        # These should work normally without triggering __getattr__
        assert callable(commands_module.register_command)
        assert commands_module.CommandInfo is not None
        assert callable(commands_module.get_command_registry)


class TestGetattrLogic(FoundationTestCase):
    """Test __getattr__ logic comprehensively."""

    def test_getattr_handles_both_click_features(self) -> None:
        """Test that __getattr__ handles both click features properly."""
        import provide.foundation.hub.commands as commands_module

        # Both should be accessible
        build_cmd = commands_module.build_click_command
        create_grp = commands_module.create_command_group

        assert callable(build_cmd)
        assert callable(create_grp)

    def test_getattr_branch_coverage_build_click_command(self) -> None:
        """Test specific branch for build_click_command in __getattr__."""
        # This tests the specific condition on line 21-22
        import provide.foundation.hub.commands as commands_module

        # Directly access to trigger the name == "build_click_command" branch
        result = commands_module.build_click_command
        assert callable(result)

    def test_getattr_branch_coverage_create_command_group(self) -> None:
        """Test specific branch for create_command_group in __getattr__."""
        # This tests the specific condition on line 23-24
        import provide.foundation.hub.commands as commands_module

        # Directly access to trigger the name == "create_command_group" branch
        result = commands_module.create_command_group
        assert callable(result)

    def test_getattr_multiple_accesses_consistent(self) -> None:
        """Test that multiple accesses to same attribute are consistent."""
        import provide.foundation.hub.commands as commands_module

        # Multiple accesses should return the same function
        build1 = commands_module.build_click_command
        build2 = commands_module.build_click_command

        assert build1 is build2


class TestModuleBehavior(FoundationTestCase):
    """Test overall module behavior and integration."""

    def test_module_docstring_present(self) -> None:
        """Test that module has appropriate docstring."""
        import provide.foundation.hub.commands as commands_module

        assert commands_module.__doc__ is not None
        assert len(commands_module.__doc__) > 10
        assert "Command" in commands_module.__doc__

    def test_core_functionality_without_click_features(self) -> None:
        """Test that core functionality works independent of click features."""
        from provide.foundation.hub.commands import (
            CommandInfo,
            get_command_registry,
            register_command,
        )

        # Core functionality should always work
        registry = get_command_registry()
        assert registry is not None

        assert callable(register_command)
        assert CommandInfo is not None

    def test_lazy_loading_error_doesnt_break_core(self) -> None:
        """Test that lazy loading errors don't affect core functionality."""
        from provide.foundation.hub.commands import (
            get_command_registry,
            register_command,
        )

        # Mock to simulate click import failure
        with patch("builtins.__import__") as mock_import:

            def import_side_effect(name, *args, **kwargs):
                if name == "provide.foundation.cli.click.builder":
                    raise ImportError("click not available")
                return __import__(name, *args, **kwargs)

            mock_import.side_effect = import_side_effect

            # Core functionality should still work
            registry = get_command_registry()
            assert registry is not None
            assert callable(register_command)

    def test_all_listed_features_accessible(self) -> None:
        """Test that all features listed in __all__ are accessible."""
        import provide.foundation.hub.commands as commands_module

        for feature_name in commands_module.__all__:
            # Should be able to access without errors (though click features might fail import)
            try:
                feature = getattr(commands_module, feature_name)
                assert feature is not None
            except ImportError:
                # Expected for click features if click isn't available
                assert feature_name in ("build_click_command", "create_command_group")




# Removed obsolete test classes:
# - TestClickDependencyHandling (tested __getattr__ error handling)
# - TestErrorMessages (tested __getattr__ error messages)
