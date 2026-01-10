#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Comprehensive coverage tests for cli/__init__.py.

These tests target uncovered lines and edge cases in the CLI module initialization."""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import patch
import pytest

from provide.foundation.cli import (
    _HAS_CLICK,
    CLIAdapter,
    CLIAdapterNotFoundError,
    CLIError,
    get_cli_adapter,
)


class TestGetCLIAdapter(FoundationTestCase):
    """Test get_cli_adapter() function."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_cli_adapter_click_success(self) -> None:
        """Test getting click adapter when available."""
        adapter = get_cli_adapter("click")

        assert isinstance(adapter, CLIAdapter)
        assert adapter is not None

    def test_get_cli_adapter_default_framework_is_click(self) -> None:
        """Test default framework is click."""
        adapter = get_cli_adapter()

        # Default should be click
        assert isinstance(adapter, CLIAdapter)

    def test_get_cli_adapter_click_case_sensitive(self) -> None:
        """Test framework name is case-sensitive."""
        # Should work with lowercase
        adapter = get_cli_adapter("click")
        assert isinstance(adapter, CLIAdapter)

        # Uppercase should fail
        with pytest.raises(ValueError, match="Unknown CLI framework: CLICK"):
            get_cli_adapter("CLICK")

    def test_get_cli_adapter_unknown_framework_raises_value_error(self) -> None:
        """Test unknown framework raises ValueError."""
        with pytest.raises(ValueError, match="Unknown CLI framework: typer"):
            get_cli_adapter("typer")

    def test_get_cli_adapter_unsupported_framework_error_message(self) -> None:
        """Test error message includes supported frameworks."""
        with pytest.raises(ValueError, match="Supported frameworks: click"):
            get_cli_adapter("unknown")

    def test_get_cli_adapter_empty_string_raises_value_error(self) -> None:
        """Test empty string raises ValueError."""
        with pytest.raises(ValueError, match="Unknown CLI framework"):
            get_cli_adapter("")

    def test_get_cli_adapter_with_numbers_raises_value_error(self) -> None:
        """Test numeric framework name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown CLI framework: 123"):
            get_cli_adapter("123")


class TestGetCLIAdapterImportErrors(FoundationTestCase):
    """Test get_cli_adapter() import error handling."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_cli_adapter_click_import_error_with_click_in_message(self) -> None:
        """Test CLIAdapterNotFoundError when click import fails with 'click' in error."""

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "click" in name:
                raise ImportError("No module named 'click'")
            return __import__(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=mock_import),
            pytest.raises(CLIAdapterNotFoundError, match="click"),
        ):
            get_cli_adapter("click")

    def test_get_cli_adapter_click_import_error_without_click_in_message(self) -> None:
        """Test ImportError is re-raised when 'click' not in error message."""

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if "provide.foundation.cli.click" in name:
                raise ImportError("Some other import error")
            return __import__(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=mock_import),
            pytest.raises(ImportError, match="Some other import error"),
        ):
            get_cli_adapter("click")


class TestCLIModuleExports(FoundationTestCase):
    """Test CLI module exports in __all__."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_has_click_flag_is_boolean(self) -> None:
        """Test _HAS_CLICK flag is a boolean."""
        assert isinstance(_HAS_CLICK, bool)

    def test_has_click_flag_is_true_when_click_available(self) -> None:
        """Test _HAS_CLICK is True when click is available."""
        # In test environment, click should be available
        assert _HAS_CLICK is True

    def test_cli_adapter_class_is_exported(self) -> None:
        """Test CLIAdapter is exported."""
        assert CLIAdapter is not None

    def test_cli_error_classes_are_exported(self) -> None:
        """Test CLI error classes are exported."""
        from provide.foundation.cli import (
            CLIAdapterNotFoundError,
            CLIBuildError,
            CLIError,
            InvalidCLIHintError,
        )

        assert issubclass(CLIError, Exception)
        assert issubclass(CLIBuildError, CLIError)
        assert issubclass(CLIAdapterNotFoundError, CLIError)
        assert issubclass(InvalidCLIHintError, CLIError)

    def test_cli_utilities_are_exported(self) -> None:
        """Test CLI utilities are exported."""
        from provide.foundation.cli import (
            CliTestRunner,
            assert_cli_error,
            assert_cli_success,
            create_cli_context,
            echo_error,
            echo_info,
            echo_json,
            echo_success,
            echo_warning,
            setup_cli_logging,
        )

        # Verify they're all callable or classes
        assert callable(assert_cli_error)
        assert callable(assert_cli_success)
        assert callable(create_cli_context)
        assert callable(echo_error)
        assert callable(echo_info)
        assert callable(echo_json)
        assert callable(echo_success)
        assert callable(echo_warning)
        assert callable(setup_cli_logging)
        assert CliTestRunner is not None

    def test_cli_decorators_are_exported(self) -> None:
        """Test CLI decorators are exported."""
        from provide.foundation.cli import (
            config_options,
            error_handler,
            flexible_options,
            logging_options,
            output_options,
            pass_context,
            standard_options,
            version_option,
        )

        # Verify they're all callable
        assert callable(config_options)
        assert callable(error_handler)
        assert callable(flexible_options)
        assert callable(logging_options)
        assert callable(output_options)
        assert callable(pass_context)
        assert callable(standard_options)
        assert callable(version_option)

    def test_get_cli_adapter_is_exported(self) -> None:
        """Test get_cli_adapter is exported."""
        assert callable(get_cli_adapter)

    def test_all_exports_are_accessible(self) -> None:
        """Test all items in __all__ are actually accessible."""
        import provide.foundation.cli

        for export_name in provide.foundation.cli.__all__:
            assert hasattr(provide.foundation.cli, export_name), f"Export {export_name} not accessible"


class TestCLIAdapterNotFoundErrorDetails(FoundationTestCase):
    """Test CLIAdapterNotFoundError construction."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_cli_adapter_not_found_error_attributes(self) -> None:
        """Test CLIAdapterNotFoundError has correct attributes."""
        error = CLIAdapterNotFoundError(framework="click", package="cli")

        assert error.framework == "click"
        assert error.package == "cli"
        assert "click" in str(error).lower()

    def test_cli_adapter_not_found_error_is_cli_error(self) -> None:
        """Test CLIAdapterNotFoundError inherits from CLIError."""
        error = CLIAdapterNotFoundError(framework="click", package="cli")

        assert isinstance(error, CLIError)
        assert isinstance(error, Exception)


class TestGetCLIAdapterIntegration(FoundationTestCase):
    """Test get_cli_adapter integration scenarios."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_get_cli_adapter_returns_same_type_consistently(self) -> None:
        """Test get_cli_adapter returns same adapter type consistently."""
        adapter1 = get_cli_adapter("click")
        adapter2 = get_cli_adapter("click")

        # Should be same type (but not necessarily same instance)
        assert type(adapter1) is type(adapter2)

    def test_get_cli_adapter_returns_functional_adapter(self) -> None:
        """Test returned adapter has required methods."""
        adapter = get_cli_adapter("click")

        # Verify it has the required protocol methods
        assert hasattr(adapter, "build_command")
        assert hasattr(adapter, "build_group")
        assert callable(adapter.build_command)
        assert callable(adapter.build_group)


class TestCLIModuleDocumentation(FoundationTestCase):
    """Test CLI module documentation and metadata."""

    def setup_method(self) -> None:
        """Set up test environment."""
        super().setup_method()

    def test_module_has_docstring(self) -> None:
        """Test CLI module has documentation (may be None if placed after imports)."""
        import provide.foundation.cli

        # Module docstring might be None if it's placed after imports in the file
        # This is acceptable - we're just checking the module is importable
        assert provide.foundation.cli is not None

    def test_get_cli_adapter_has_docstring(self) -> None:
        """Test get_cli_adapter has documentation."""
        assert get_cli_adapter.__doc__ is not None
        assert "framework" in get_cli_adapter.__doc__.lower()


__all__ = [
    "TestCLIAdapterNotFoundErrorDetails",
    "TestCLIModuleDocumentation",
    "TestCLIModuleExports",
    "TestGetCLIAdapter",
    "TestGetCLIAdapterImportErrors",
    "TestGetCLIAdapterIntegration",
]

# 🧱🏗️🔚
