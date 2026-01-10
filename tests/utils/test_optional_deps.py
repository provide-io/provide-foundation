#
# SPDX-FileCopyrightText: Copyright (c) provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for utils/optional_deps.py module.

Run with: pytest tests/utils/test_optional_deps.py -v"""

from __future__ import annotations

from provide.testkit import FoundationTestCase
from provide.testkit.mocking import MagicMock, patch
import pytest

from provide.foundation.utils.optional_deps import (
    OptionalDependency,
    load_optional_dependency,
)


class TestOptionalDependencyInit(FoundationTestCase):
    """Tests for OptionalDependency initialization."""

    def test_init_creates_instance(self) -> None:
        """Test OptionalDependency initialization."""
        dep = OptionalDependency("click", "cli")

        assert dep.package_name == "click"
        assert dep.feature_name == "cli"
        assert dep._available is None  # Not checked yet

    def test_init_with_different_names(self) -> None:
        """Test initialization with various package/feature names."""
        dep1 = OptionalDependency("cryptography", "crypto")
        dep2 = OptionalDependency("httpx", "http")
        dep3 = OptionalDependency("opentelemetry-api", "telemetry")

        assert dep1.package_name == "cryptography"
        assert dep2.package_name == "httpx"
        assert dep3.package_name == "opentelemetry-api"


class TestOptionalDependencyIsAvailable(FoundationTestCase):
    """Tests for OptionalDependency.is_available() method."""

    def test_is_available_for_installed_package(self) -> None:
        """Test is_available returns True for installed packages."""
        # pytest should always be available in test environment
        dep = OptionalDependency("pytest", "testing")

        assert dep.is_available() is True
        # Check caching works
        assert dep._available is True

    def test_is_available_for_missing_package(self) -> None:
        """Test is_available returns False for missing packages."""
        dep = OptionalDependency("nonexistent_package_12345", "fake")

        assert dep.is_available() is False
        # Check caching works
        assert dep._available is False

    def test_is_available_caches_result(self) -> None:
        """Test that is_available caches the result."""
        dep = OptionalDependency("pytest", "testing")

        # First call
        result1 = dep.is_available()
        # Second call should use cached value
        result2 = dep.is_available()

        assert result1 == result2
        assert dep._available is not None

    def test_is_available_with_import_error(self) -> None:
        """Test is_available handles ImportError correctly."""
        dep = OptionalDependency("missing_module", "feature")

        with patch("builtins.__import__", side_effect=ImportError("Module not found")):
            assert dep.is_available() is False


class TestOptionalDependencyImportPackage(FoundationTestCase):
    """Tests for OptionalDependency.import_package() method."""

    def test_import_package_when_available(self) -> None:
        """Test import_package returns actual module when available."""
        dep = OptionalDependency("sys", "system")

        result = dep.import_package()

        # sys is always available
        import sys

        assert result is sys

    def test_import_package_when_unavailable(self) -> None:
        """Test import_package returns stub when unavailable."""
        dep = OptionalDependency("nonexistent_package", "fake")

        result = dep.import_package()

        # Should be a stub module
        assert result is not None
        # Accessing any attribute should raise an error about the dependency
        with pytest.raises(Exception):
            _ = result.some_attribute

    def test_import_package_uses_is_available(self) -> None:
        """Test import_package calls is_available."""
        dep = OptionalDependency("pytest", "testing")

        with patch.object(dep, "is_available", return_value=True):
            result = dep.import_package()

            assert dep.is_available.called
            assert result is not None


class TestOptionalDependencyImportSymbols(FoundationTestCase):
    """Tests for OptionalDependency.import_symbols() method."""

    def test_import_symbols_when_available(self) -> None:
        """Test import_symbols returns actual symbols when available."""
        dep = OptionalDependency("sys", "system")

        symbols = dep.import_symbols("sys", ["argv", "exit"])

        assert len(symbols) == 2
        import sys

        assert symbols[0] is sys.argv
        assert symbols[1] is sys.exit

    def test_import_symbols_when_unavailable_with_stubs(self) -> None:
        """Test import_symbols returns stubs when module unavailable."""
        dep = OptionalDependency("nonexistent", "fake")

        symbols = dep.import_symbols(
            "nonexistent.module",
            ["ClassName", "function_name"],
            create_stubs=True,
        )

        assert len(symbols) == 2
        # Both should be stubs
        assert symbols[0] is not None
        assert symbols[1] is not None

    def test_import_symbols_without_stubs_raises(self) -> None:
        """Test import_symbols raises ImportError when create_stubs=False."""
        dep = OptionalDependency("nonexistent", "fake")

        with pytest.raises(ImportError):
            dep.import_symbols(
                "nonexistent.module",
                ["ClassName"],
                create_stubs=False,
            )

    def test_import_symbols_class_vs_function_detection(self) -> None:
        """Test import_symbols creates appropriate stubs based on naming."""
        dep = OptionalDependency("nonexistent", "fake")

        symbols = dep.import_symbols(
            "nonexistent.module",
            ["ClassName", "function_name", "AnotherClass", "another_func"],
            create_stubs=True,
        )

        assert len(symbols) == 4
        # All should be stubs (can't easily test the type without invoking them)
        for symbol in symbols:
            assert symbol is not None

    def test_import_symbols_empty_list(self) -> None:
        """Test import_symbols with empty symbol list."""
        dep = OptionalDependency("sys", "system")

        symbols = dep.import_symbols("sys", [])

        assert symbols == []

    def test_import_symbols_single_symbol(self) -> None:
        """Test import_symbols with single symbol."""
        dep = OptionalDependency("sys", "system")

        symbols = dep.import_symbols("sys", ["version"])

        assert len(symbols) == 1
        import sys

        assert symbols[0] is sys.version


class TestLoadOptionalDependency(FoundationTestCase):
    """Tests for load_optional_dependency() convenience function."""

    def test_load_optional_dependency_package_only(self) -> None:
        """Test loading entire package."""
        is_available, imported = load_optional_dependency("sys", "system")

        assert is_available is True
        import sys

        assert imported is sys

    def test_load_optional_dependency_with_symbols(self) -> None:
        """Test loading specific symbols."""
        is_available, symbols = load_optional_dependency(
            "sys",
            "system",
            module_path="sys",
            symbols=["argv", "exit"],
        )

        assert is_available is True
        assert len(symbols) == 2
        import sys

        assert symbols[0] is sys.argv
        assert symbols[1] is sys.exit

    def test_load_optional_dependency_unavailable_package(self) -> None:
        """Test loading unavailable package."""
        is_available, imported = load_optional_dependency(
            "nonexistent_package",
            "fake",
        )

        assert is_available is False
        assert imported is not None  # Should be a stub

    def test_load_optional_dependency_unavailable_symbols(self) -> None:
        """Test loading symbols from unavailable module."""
        is_available, symbols = load_optional_dependency(
            "nonexistent",
            "fake",
            module_path="nonexistent.module",
            symbols=["Symbol1", "symbol2"],
        )

        assert is_available is False
        assert len(symbols) == 2
        # Should be stubs
        for symbol in symbols:
            assert symbol is not None

    def test_load_optional_dependency_creates_dep_instance(self) -> None:
        """Test that load_optional_dependency creates OptionalDependency."""
        with patch("provide.foundation.utils.optional_deps.OptionalDependency") as mock_class:
            mock_instance = MagicMock()
            mock_instance.is_available.return_value = True
            mock_instance.import_package.return_value = MagicMock()
            mock_class.return_value = mock_instance

            load_optional_dependency("test", "feature")

            mock_class.assert_called_once_with("test", "feature")
            mock_instance.is_available.assert_called_once()
            mock_instance.import_package.assert_called_once()


class TestOptionalDependencyEdgeCases(FoundationTestCase):
    """Tests for edge cases in OptionalDependency."""

    def test_repeated_availability_checks(self) -> None:
        """Test that multiple availability checks use cached value."""
        dep = OptionalDependency("pytest", "testing")

        with patch("builtins.__import__") as mock_import:
            # First call
            result1 = dep.is_available()
            # Second call should not call __import__ again
            result2 = dep.is_available()

            assert result1 == result2
            # __import__ should only be called once due to caching
            assert mock_import.call_count <= 1

    def test_import_package_with_import_side_effects(self) -> None:
        """Test import_package handles import side effects."""
        dep = OptionalDependency("sys", "system")

        # Import should work even if called multiple times
        result1 = dep.import_package()
        result2 = dep.import_package()

        assert result1 is result2

    def test_import_symbols_with_nonexistent_attribute(self) -> None:
        """Test import_symbols with non-existent attribute."""
        dep = OptionalDependency("sys", "system")

        # sys module exists but "nonexistent_attr" doesn't
        with pytest.raises(AttributeError):
            dep.import_symbols("sys", ["nonexistent_attr"], create_stubs=False)

    def test_package_name_with_special_characters(self) -> None:
        """Test OptionalDependency with hyphenated package names."""
        # Some packages use hyphens (e.g., opentelemetry-api)
        dep = OptionalDependency("provide-foundation", "foundation")

        assert dep.package_name == "provide-foundation"
        assert dep.feature_name == "foundation"


class TestOptionalDependencyIntegration(FoundationTestCase):
    """Integration tests for OptionalDependency."""

    def test_real_world_usage_click(self) -> None:
        """Test with real-world click dependency."""
        is_available, click = load_optional_dependency("click", "cli")

        # click should be available in test environment
        assert is_available is True
        assert click is not None

    def test_real_world_usage_missing_package(self) -> None:
        """Test with missing package."""
        is_available, pkg = load_optional_dependency(
            "definitely_not_installed_package_xyz",
            "fake",
        )

        assert is_available is False
        assert pkg is not None  # Stub should be returned

    def test_real_world_usage_with_symbols(self) -> None:
        """Test importing specific symbols from real module."""
        is_available, symbols = load_optional_dependency(
            "sys",
            "system",
            module_path="os.path",
            symbols=["join", "exists"],
        )

        assert is_available is True
        assert len(symbols) == 2

        from os.path import exists, join

        assert symbols[0] is join
        assert symbols[1] is exists


class TestOptionalDependencyDocumentation(FoundationTestCase):
    """Tests to verify documentation examples work."""

    def test_example_simple_package_import(self) -> None:
        """Test simple package import example from docstring."""
        click_dep = OptionalDependency("click", "cli")
        click = click_dep.import_package()
        has_click = click_dep.is_available()

        # In test environment, click should be available
        assert has_click is True
        assert click is not None

    def test_example_import_specific_symbols(self) -> None:
        """Test importing specific symbols example from docstring."""
        # Use sys instead of crypto to avoid cryptography dependency
        sys_dep = OptionalDependency("sys", "system")
        argv, exit_func = sys_dep.import_symbols("sys", ["argv", "exit"])

        import sys

        assert argv is sys.argv
        assert exit_func is sys.exit

    def test_example_load_entire_package(self) -> None:
        """Test load entire package example from docstring."""
        has_click, click = load_optional_dependency("click", "cli")

        # Should work in test environment
        assert isinstance(has_click, bool)
        assert click is not None


__all__ = [
    "TestLoadOptionalDependency",
    "TestOptionalDependencyDocumentation",
    "TestOptionalDependencyEdgeCases",
    "TestOptionalDependencyImportPackage",
    "TestOptionalDependencyImportSymbols",
    "TestOptionalDependencyInit",
    "TestOptionalDependencyIntegration",
    "TestOptionalDependencyIsAvailable",
]

# 🧱🏗️🔚
