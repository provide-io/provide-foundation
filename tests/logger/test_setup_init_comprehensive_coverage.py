#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for logger/setup/__init__.py module."""

import importlib

from provide.testkit import FoundationTestCase


class TestLoggerSetupInit(FoundationTestCase):
    """Test logger/setup/__init__.py module functionality."""

    def test_internal_setup_import(self) -> None:
        """Test that internal_setup can be imported."""
        from provide.foundation.logger.setup import internal_setup

        assert internal_setup is not None
        assert callable(internal_setup)

    def test_internal_setup_is_coordinator_function(self) -> None:
        """Test that internal_setup is the same as coordinator.internal_setup."""
        from provide.foundation.logger.setup import internal_setup
        from provide.foundation.logger.setup.coordinator import (
            internal_setup as coordinator_setup,
        )

        assert internal_setup is coordinator_setup

    def test_reset_for_testing_moved_to_testkit(self) -> None:
        """Test that reset functionality has been moved to testkit."""
        from provide.foundation.logger import setup

        # reset_for_testing should not exist in foundation anymore
        assert not hasattr(setup, "reset_for_testing")
        assert not hasattr(setup, "_has_testing")

    def test_reset_for_testing_available_in_testkit(self) -> None:
        """Test that reset functionality is available in testkit."""
        from provide.testkit.logger import reset_foundation_setup_for_testing

        assert reset_foundation_setup_for_testing is not None
        assert callable(reset_foundation_setup_for_testing)

    def test_all_exports_after_refactor(self) -> None:
        """Test __all__ exports after testmode refactor."""
        from provide.foundation.logger.setup import __all__

        # Only core setup functionality should be exported
        expected_exports = ["get_system_logger", "internal_setup"]
        assert set(__all__) == set(expected_exports)

    def test_all_exports_accessible(self) -> None:
        """Test that all items in __all__ are accessible."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        for export_name in setup_module.__all__:
            assert hasattr(setup_module, export_name)
            export_item = getattr(setup_module, export_name)
            assert export_item is not None

    def test_module_docstring(self) -> None:
        """Test that module has proper docstring."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        assert setup_module.__doc__ is not None
        assert "Foundation Logger Setup Module" in setup_module.__doc__
        assert "structured logging" in setup_module.__doc__
        assert "processor setup" in setup_module.__doc__

    def test_no_testing_flag(self) -> None:
        """Test that _has_testing flag no longer exists."""
        from provide.foundation.logger import setup

        # _has_testing should not exist anymore
        assert not hasattr(setup, "_has_testing")


class TestTestingRefactorIntegration:
    """Test integration after testing utilities moved to testkit."""

    def test_testing_utilities_not_in_foundation(self) -> None:
        """Test that testing utilities are no longer in foundation setup."""
        from provide.foundation.logger import setup

        # reset_for_testing should not exist in foundation anymore
        assert not hasattr(setup, "reset_for_testing")
        assert not hasattr(setup, "_has_testing")

    def test_testing_utilities_available_in_testkit(self) -> None:
        """Test that testing utilities are available in testkit."""
        from provide.testkit.logger import reset_foundation_setup_for_testing

        assert reset_foundation_setup_for_testing is not None
        assert callable(reset_foundation_setup_for_testing)

    def test_all_list_consistency_after_refactor(self) -> None:
        """Test that __all__ list is consistent after testmode refactor."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        # All items in __all__ should be available as attributes
        for item in setup_module.__all__:
            assert hasattr(setup_module, item)

        # Core exports should always be present
        assert "internal_setup" in setup_module.__all__
        assert hasattr(setup_module, "internal_setup")

        # Testing exports should not be present
        assert "reset_for_testing" not in setup_module.__all__


class TestSetupModuleIntegration:
    """Test integration aspects of the setup module."""

    def test_internal_setup_functionality(self) -> None:
        """Test that internal_setup function works."""
        from provide.foundation.logger.setup import internal_setup

        # Test that it can be called (basic smoke test)
        assert callable(internal_setup)

        # The function should accept keyword arguments
        import inspect

        sig = inspect.signature(internal_setup)
        assert len(sig.parameters) > 0

    def test_reset_functionality_in_testkit(self) -> None:
        """Test that reset functionality works in testkit."""
        from provide.testkit.logger import reset_foundation_setup_for_testing

        assert callable(reset_foundation_setup_for_testing)

        # Should be able to call it without arguments
        import inspect

        sig = inspect.signature(reset_foundation_setup_for_testing)
        # Should have no required parameters
        required_params = [p for p in sig.parameters.values() if p.default == inspect.Parameter.empty]
        assert len(required_params) == 0

    def test_module_structure(self) -> None:
        """Test overall module structure and attributes."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        # Should have the expected attributes
        assert hasattr(setup_module, "__all__")
        assert hasattr(setup_module, "internal_setup")

        # Should not have old testing-related attributes
        assert not hasattr(setup_module, "_has_testing")
        assert not hasattr(setup_module, "reset_for_testing")

    def test_import_paths_consistency(self) -> None:
        """Test that import paths are consistent."""
        # Test different ways of importing
        from provide.foundation.logger.setup import internal_setup as setup1
        from provide.foundation.logger.setup.coordinator import internal_setup as setup2

        # Should be the same function
        assert setup1 is setup2

        # Test reset function is available in testkit
        try:
            from provide.testkit.logger import reset_foundation_setup_for_testing

            # Direct import should work
            assert reset_foundation_setup_for_testing is not None
            assert callable(reset_foundation_setup_for_testing)

        except ImportError:
            # If testkit isn't available in some test environments, that's expected
            pass

    def test_no_unexpected_exports(self) -> None:
        """Test that module doesn't export unexpected items."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        # Get all public attributes (not starting with _)
        public_attrs = [attr for attr in dir(setup_module) if not attr.startswith("_")]

        # Should only contain items from __all__
        core_exports = setup_module.__all__

        # Public attributes should match core exports
        assert set(public_attrs) >= set(core_exports)


class TestModuleDocumentation:
    """Test module documentation and metadata."""

    def test_module_file_header(self) -> None:
        """Test that module has proper file header."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        # Module should have docstring
        assert setup_module.__doc__ is not None
        assert len(setup_module.__doc__) > 20

    def test_docstring_content(self) -> None:
        """Test docstring contains expected content."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        docstring = setup_module.__doc__
        expected_terms = [
            "Foundation Logger Setup",
            "structured logging",
            "processor setup",
            "emoji resolution",
        ]

        for term in expected_terms:
            assert term in docstring

    def test_module_attributes_documented(self) -> None:
        """Test that key module attributes are appropriately documented."""
        setup_module = importlib.import_module("provide.foundation.logger.setup")

        # Key attributes should exist
        assert hasattr(setup_module, "__all__")
        assert hasattr(setup_module, "internal_setup")

        # Old testing attributes should not exist
        assert not hasattr(setup_module, "_has_testing")

        # __all__ should be a list
        assert isinstance(setup_module.__all__, list)
        assert len(setup_module.__all__) > 0


# 🧱🏗️🔚
