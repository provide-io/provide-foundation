"""Coverage tests for foundation __init__.py module."""

import sys
import pytest
from unittest.mock import patch, MagicMock


class TestFoundationInit:
    """Test foundation __init__.py module coverage."""

    def setup_method(self):
        """Reset module state before each test."""
        import sys

        # Clear CLI module from cache to ensure fresh imports
        cli_modules = [
            name
            for name in sys.modules.keys()
            if name.startswith("provide.foundation.cli")
        ]
        self.saved_cli_modules = {}
        for module_name in cli_modules:
            self.saved_cli_modules[module_name] = sys.modules[module_name]
            del sys.modules[module_name]
            
        # Also clear the main foundation module to reset any cached __getattr__ state
        foundation_modules = [
            name
            for name in sys.modules.keys() 
            if name == "provide.foundation"
        ]
        self.saved_foundation_modules = {}
        for module_name in foundation_modules:
            self.saved_foundation_modules[module_name] = sys.modules[module_name]
            del sys.modules[module_name]

    def teardown_method(self):
        """Restore module state after each test."""
        import sys

        # Restore CLI modules
        for module_name, module in self.saved_cli_modules.items():
            sys.modules[module_name] = module
            
        # Restore foundation modules
        for module_name, module in self.saved_foundation_modules.items():
            sys.modules[module_name] = module

    def test_console_imports_available(self):
        """Test console imports when available."""
        import provide.foundation

        # Test that console functions are available if click is installed
        if hasattr(provide.foundation, "perr"):
            assert provide.foundation.perr is not None
            assert provide.foundation.pin is not None
            assert provide.foundation.pout is not None

    def test_console_imports_always_available(self):
        """Test console imports are always available."""
        # Console functions should always exist (they handle click availability internally)
        import provide.foundation

        # Console functions should always be available and callable
        assert provide.foundation.perr is not None
        assert provide.foundation.pin is not None
        assert provide.foundation.pout is not None
        assert callable(provide.foundation.perr)
        assert callable(provide.foundation.pin)
        assert callable(provide.foundation.pout)

    def test_aaa_getattr_cli_click_missing(self):
        """Test __getattr__ CLI import with missing click dependency."""
        import provide.foundation
        import sys

        # Clear any existing CLI module from cache
        cli_module_key = "provide.foundation.cli"
        if cli_module_key in sys.modules:
            del sys.modules[cli_module_key]

        def mock_import_func(name, *args, **kwargs):
            if name == "provide.foundation.cli":
                raise ImportError("No module named 'click'")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_func):
            with pytest.raises(
                ImportError, match="CLI features require optional dependencies"
            ):
                _ = provide.foundation.cli

    def test_aaa_getattr_cli_other_import_error(self):
        """Test __getattr__ CLI import with other ImportError."""
        import provide.foundation
        import sys

        # Clear any existing CLI module from cache
        cli_module_key = "provide.foundation.cli"
        if cli_module_key in sys.modules:
            del sys.modules[cli_module_key]

        def mock_import_func(name, *args, **kwargs):
            if name == "provide.foundation.cli":
                raise ImportError("Some other error")
            return __import__(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import_func):
            with pytest.raises(ImportError, match="Some other error"):
                _ = provide.foundation.cli

    def test_getattr_cli_success(self):
        """Test __getattr__ for successful CLI import."""
        import provide.foundation

        # Try to access cli attribute - this should work if click is available
        try:
            cli = provide.foundation.cli
            assert cli is not None
        except ImportError:
            # Expected if click is not available
            pass

    def test_getattr_invalid_attribute(self):
        """Test __getattr__ with invalid attribute name."""
        import provide.foundation

        with pytest.raises(AttributeError, match="has no attribute 'nonexistent'"):
            _ = provide.foundation.nonexistent

    def test_all_exports_list(self):
        """Test __all__ exports list."""
        import provide.foundation

        assert hasattr(provide.foundation, "__all__")
        assert isinstance(provide.foundation.__all__, list)
        assert len(provide.foundation.__all__) > 0

        # Test some key exports are in __all__
        expected_exports = [
            "logger",
            "setup_telemetry",
            "FoundationError",
            "config",
            "__version__",
        ]

        for export in expected_exports:
            assert export in provide.foundation.__all__

    def test_conditional_console_exports(self):
        """Test conditional console exports in __all__."""
        import provide.foundation

        # The console exports should be conditionally included
        console_exports = ["perr", "pin", "pout"]

        # Console functions should always be available and in __all__
        for export in console_exports:
            assert export in provide.foundation.__all__

    def test_core_imports_available(self):
        """Test that core imports are available."""
        import provide.foundation

        # Test core modules are accessible
        assert hasattr(provide.foundation, "config")
        assert hasattr(provide.foundation, "errors")
        assert hasattr(provide.foundation, "platform")
        assert hasattr(provide.foundation, "process")

        # Test core classes/functions
        assert hasattr(provide.foundation, "logger")
        assert hasattr(provide.foundation, "setup_telemetry")
        assert hasattr(provide.foundation, "FoundationError")
        assert hasattr(provide.foundation, "__version__")

    def test_eventset_exports(self):
        """Test event set-related exports."""
        import provide.foundation

        # Test event set exports (replacement for emoji system)
        eventset_exports = [
            "EventSet",
            "EventMapping",
            "FieldMapping",
        ]

        for export in eventset_exports:
            assert hasattr(provide.foundation, export), f"Missing export: {export}"

    def test_hub_exports(self):
        """Test hub and registry exports."""
        import provide.foundation

        hub_exports = [
            "Hub",
            "get_hub",
            "clear_hub",
            "Registry",
            "RegistryEntry",
            "ComponentCategory",
            "get_component_registry",
        ]

        for export in hub_exports:
            assert hasattr(provide.foundation, export), f"Missing hub export: {export}"

    def test_error_handling_exports(self):
        """Test error handling exports."""
        import provide.foundation

        error_exports = [
            "FoundationError",
            "error_boundary",
            "retry_on_error",
            "with_error_handling",
        ]

        for export in error_exports:
            assert hasattr(provide.foundation, export), (
                f"Missing error export: {export}"
            )

    def test_utility_exports(self):
        """Test utility exports."""
        import provide.foundation

        utility_exports = [
            "timed_block",
            "TokenBucketRateLimiter",
        ]

        for export in utility_exports:
            assert hasattr(provide.foundation, export), (
                f"Missing utility export: {export}"
            )


class TestModuleAttributes:
    """Test module attributes and special cases."""

    def test_version_import(self):
        """Test version import."""
        import provide.foundation

        assert hasattr(provide.foundation, "__version__")
        assert isinstance(provide.foundation.__version__, str)
        assert len(provide.foundation.__version__) > 0

    def test_console_functions_available(self):
        """Test console functions are available."""
        import provide.foundation

        # Console functions should always be available
        assert hasattr(provide.foundation, "perr")
        assert hasattr(provide.foundation, "pin")
        assert hasattr(provide.foundation, "pout")

    def test_type_exports(self):
        """Test type exports."""
        import provide.foundation

        type_exports = [
            "ConsoleFormatterStr",
            "LogLevelStr",
        ]

        for export in type_exports:
            assert hasattr(provide.foundation, export), f"Missing type export: {export}"

    def test_config_exports(self):
        """Test configuration exports."""
        import provide.foundation

        config_exports = [
            "LoggingConfig",
            "TelemetryConfig",
        ]

        for export in config_exports:
            assert hasattr(provide.foundation, export), (
                f"Missing config export: {export}"
            )
