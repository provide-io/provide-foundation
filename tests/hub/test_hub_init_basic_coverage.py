"""Basic coverage tests for hub __init__ module."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
import pytest


class TestHubInitBasicCoverage(FoundationTestCase):
    """Basic coverage tests for hub __init__ module."""

    def test_hub_init_imports_successfully(self) -> None:
        """Test that hub __init__ module can be imported."""
        import provide.foundation.hub

        assert provide.foundation.hub is not None

    def test_core_imports_available(self) -> None:
        """Test core hub imports are available."""
        from provide.foundation.hub import (
            ComponentCategory,
            Hub,
            clear_hub,
            get_component_registry,
            get_hub,
            register_command,
        )

        assert ComponentCategory is not None
        assert get_component_registry is not None
        assert register_command is not None
        assert Hub is not None
        assert clear_hub is not None
        assert get_hub is not None

    def test_build_click_command_function_exists(self) -> None:
        """Test build_click_command function exists."""
        from provide.foundation.hub import build_click_command

        assert build_click_command is not None
        assert callable(build_click_command)

    def test_build_click_command_with_click_available(self) -> None:
        """Test build_click_command when click is available."""
        try:
            import click  # noqa: F401

            from provide.foundation.hub import build_click_command

            # Should be callable
            assert callable(build_click_command)
        except ImportError:
            pytest.skip("Click not available")

    def test_getattr_build_click_command(self) -> None:
        """Test __getattr__ for build_click_command."""
        try:
            import provide.foundation.hub as hub_module

            # Try to access build_click_command through __getattr__
            build_click_command = hub_module.build_click_command
            assert build_click_command is not None
        except ImportError:
            pytest.skip("Click not available")
        except AttributeError:
            pytest.skip("build_click_command not available")

    def test_getattr_nonexistent_attribute(self) -> None:
        """Test __getattr__ raises AttributeError for nonexistent attributes."""
        import provide.foundation.hub as hub_module

        with pytest.raises(AttributeError, match="has no attribute 'nonexistent'"):
            _ = hub_module.nonexistent

    def test_all_exports_list(self) -> None:
        """Test __all__ exports list."""
        from provide.foundation.hub import __all__

        assert isinstance(__all__, list)
        assert len(__all__) > 0

        # Check some expected exports
        expected_exports = [
            "get_component_registry",
            "ComponentCategory",
            "Hub",
            "clear_hub",
            "get_hub",
            "register_command",
            "build_click_command",
        ]

        for export in expected_exports:
            assert export in __all__

    def test_all_exported_items_importable(self) -> None:
        """Test all items in __all__ can be imported."""
        import provide.foundation.hub as hub_module
        from provide.foundation.hub import __all__

        for item_name in __all__:
            # Should be able to get the item
            item = getattr(hub_module, item_name)
            assert item is not None
